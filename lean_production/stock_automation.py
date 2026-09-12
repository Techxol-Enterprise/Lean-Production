import frappe
from frappe.utils import flt
from erpnext.stock.get_item_details import get_conversion_factor


class BOMMaterialList(list):
    """
    Custom list subclass that supports both list iteration and dict-like access
    (e.g. details['items'] or details.get('items')), ensuring 100% interoperability
    across both client scripts (where it serializes as JSON array) and python scripts.
    """
    @property
    def items(self):
        return self

    def get(self, key, default=None):
        if key == "items":
            return self
        return default

    def __getitem__(self, item):
        if item == "items":
            return self
        return super().__getitem__(item)


def get_bom_items(bom_no, target_qty):
    """
    Reads the BOM and scales the raw materials based on the target produced quantity.
    Returns a list of items with dynamically calculated quantities.
    """
    bom = frappe.get_doc("BOM", bom_no)
    if flt(bom.quantity) <= 0:
        frappe.throw(frappe._("BOM {0} has invalid base quantity: {1}").format(bom_no, bom.quantity))
    if not bom.is_active or bom.docstatus != 1:
        frappe.throw(frappe._("BOM {0} must be submitted and active.").format(bom_no))

    items = []
    ratio = flt(target_qty) / flt(bom.quantity)

    # Batch-fetch missing stock_uom to prevent N+1 database queries
    missing_stock_uoms = [row.item_code for row in bom.items if not getattr(row, "stock_uom", None)]
    stock_uom_map = {}
    if missing_stock_uoms:
        stock_uom_map = {
            d.name: d.stock_uom
            for d in frappe.get_all("Item", filters={"name": ["in", list(set(missing_stock_uoms))]}, fields=["name", "stock_uom"])
        }

    for row in bom.items:
        if flt(row.qty) <= 0:
            continue

        stock_uom = getattr(row, "stock_uom", None) or stock_uom_map.get(row.item_code) or frappe.db.get_value("Item", row.item_code, "stock_uom")
        conv = flt(row.conversion_factor)
        # If conversion factor is missing, zero, or defaults to 1.0 while UOMs differ, resolve dynamically
        if not conv or (row.uom != stock_uom and conv == 1.0):
            conv_data = get_conversion_factor(row.item_code, row.uom)
            conv = flt(conv_data.get("conversion_factor")) or 1.0

        items.append({
            "item_code": row.item_code,
            "qty": flt(row.qty) * ratio,
            "uom": row.uom,
            "stock_uom": stock_uom,
            "conversion_factor": conv
        })
    return items


@frappe.whitelist()
def get_item_available_stock(item_code, warehouse):
    """
    Whitelisted API returning the real-time available stock (actual_qty) from Bin.
    Used by Client Scripts when source_warehouse is updated in child table.
    """
    if not item_code or not warehouse:
        return 0.0

    frappe.has_permission("Item", "read", throw=True)
    stock = frappe.db.get_value("Bin", {"item_code": item_code, "warehouse": warehouse}, "actual_qty")
    if stock is not None:
        return flt(stock)

    from erpnext.stock.utils import get_stock_balance
    return flt(get_stock_balance(item_code, warehouse))


@frappe.whitelist()
def get_bom_material_details(item_code=None, bom_no=None, total_qty=1.0, company=None):
    """
    Whitelisted API for Client Scripts to dynamically explode BOM items,
    calculate required quantities based on total_qty (good + scrap),
    resolve default source warehouses, and fetch real-time available stock in one atomic call.
    """
    if not item_code and not bom_no:
        frappe.throw(frappe._("Either item_code or bom_no must be provided."))

    frappe.has_permission("BOM", "read", throw=True)
    frappe.has_permission("Item", "read", throw=True)

    if not bom_no:
        bom_no = frappe.db.get_value("BOM", {"item": item_code, "is_active": 1, "is_default": 1, "docstatus": 1}, "name")
        if not bom_no:
            bom_no = frappe.db.get_value("BOM", {"item": item_code, "is_active": 1, "docstatus": 1}, "name")
        if not bom_no:
            frappe.throw(frappe._("No active, submitted BOM found for item {0}").format(item_code))

    bom = frappe.get_doc("BOM", bom_no)
    if flt(bom.quantity) <= 0:
        frappe.throw(frappe._("BOM {0} base quantity must be positive.").format(bom_no))

    total_qty = flt(total_qty)
    company = company or frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    stores_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"
    fg_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"

    rm_codes = [d.item_code for d in bom.items]
    items_meta = {
        d.name: d for d in frappe.get_all(
            "Item",
            filters={"name": ["in", list(set(rm_codes))]},
            fields=["name", "item_name", "item_group", "stock_uom"]
        )
    }
    item_defaults = {
        d.parent: d.default_warehouse
        for d in frappe.get_all(
            "Item Default",
            filters={"parent": ["in", list(set(rm_codes))], "company": company},
            fields=["parent", "default_warehouse"]
        )
    }

    ratio = total_qty / flt(bom.quantity)
    result_items = BOMMaterialList()

    for row in bom.items:
        if flt(row.qty) <= 0:
            continue
        meta = items_meta.get(row.item_code) or {}
        item_group = meta.get("item_group") or ""
        stock_uom = getattr(row, "stock_uom", None) or meta.get("stock_uom") or row.uom
        conv = flt(row.conversion_factor)
        if not conv or (row.uom != stock_uom and conv == 1.0):
            conv_data = get_conversion_factor(row.item_code, row.uom)
            conv = flt(conv_data.get("conversion_factor")) or 1.0

        # Warehouse resolution hierarchy
        item_def_wh = item_defaults.get(row.item_code)
        if getattr(row, "source_warehouse", None):
            src_wh = row.source_warehouse
        elif item_group == "Bulk Purified Water" or row.item_code == "INT-BULK-WATER":
            src_wh = fg_wh
        elif item_def_wh:
            src_wh = item_def_wh
        else:
            src_wh = stores_wh

        req_qty = flt(row.qty) * ratio
        actual_stock = get_item_available_stock(row.item_code, src_wh)

        result_items.append({
            "item_code": row.item_code,
            "item_name": meta.get("item_name") or row.item_code,
            "uom": row.uom,
            "stock_uom": stock_uom,
            "conversion_factor": conv,
            "bom_qty": flt(row.qty),
            "ratio_per_unit": flt(row.qty) / flt(bom.quantity),
            "required_qty": req_qty,
            "source_warehouse": src_wh,
            "available_stock": actual_stock
        })

    return result_items


def create_manufacture_stock_entry(doc, method):
    """
    Hooked into on_submit for Water Purification, Blow Molding, and Filling Entry.
    Consumes raw materials from Lean Material Consumption child table (or fallback BOM explosion),
    absorbs scrap cost into finished goods unit valuation, and yields Good Qty into target warehouse.
    """
    # 1. Concurrency guard: lock row and verify if Stock Entry already exists and is submitted
    if doc.name:
        Doc = frappe.qb.DocType(doc.doctype)
        locked = (
            frappe.qb.from_(Doc)
            .select(Doc.stock_entry)
            .where(Doc.name == doc.name)
            .for_update()
        ).run(as_dict=True)
        db_se = locked[0].stock_entry if locked else None
    else:
        db_se = None

    existing_se_name = getattr(doc, "stock_entry", None) or db_se or frappe.db.get_value(doc.doctype, doc.name, "stock_entry")
    if existing_se_name and frappe.db.exists("Stock Entry", existing_se_name):
        existing_se = frappe.get_doc("Stock Entry", existing_se_name)
        if existing_se.docstatus == 1:
            doc.stock_entry = existing_se.name
            return

    # 2. Assert BOM exists, is active, and is submitted
    if not doc.bom_no or not frappe.db.exists("BOM", doc.bom_no):
        frappe.throw(frappe._("A valid, submitted BOM is required to generate manufacturing stock."))

    bom_doc = frappe.get_doc("BOM", doc.bom_no)
    if not bom_doc.is_active or bom_doc.docstatus != 1:
        frappe.throw(frappe._("BOM {0} must be submitted and active.").format(doc.bom_no))

    # 3. Determine Finished Good Item, Target Warehouse, and Legacy Qty
    if doc.doctype == "Water Purification Entry":
        if doc.qc_status != "Pass":
            frappe.throw(
                frappe._("Cannot submit Water Purification Entry: QC Status is '{0}'. Only batches with QC Status 'Pass' can post production stock.").format(doc.qc_status)
            )
        fg_item = doc.mineral_water_item
        target_wh = doc.target_warehouse
        legacy_qty = getattr(doc, "litres_purified", 0)

    elif doc.doctype == "Blow Molding Entry":
        fg_item = doc.bottle_item
        target_wh = doc.target_warehouse
        legacy_qty = getattr(doc, "bottles_produced_qty", 0)

    elif doc.doctype == "Filling Entry":
        fg_item = doc.finished_good_item
        target_wh = getattr(doc, "fg_warehouse", None) or getattr(doc, "target_warehouse", None)
        legacy_qty = getattr(doc, "cartons_produced", 0)

    else:
        frappe.throw(frappe._("Unsupported DocType: {0}").format(doc.doctype))

    if bom_doc.item != fg_item:
        frappe.throw(
            frappe._("BOM {0} produces item '{1}', which does not match entry item '{2}'.").format(
                doc.bom_no, bom_doc.item, fg_item
            )
        )

    # 4. Resolve Good Qty and Scrap Qty
    good_qty = flt(getattr(doc, "good_qty", None))
    if good_qty <= 0:
        good_qty = flt(legacy_qty)
    if good_qty <= 0:
        if doc.doctype == "Water Purification Entry":
            frappe.throw(frappe._("Litres Purified must be greater than zero."))
        elif doc.doctype == "Blow Molding Entry":
            frappe.throw(frappe._("Bottles Produced Qty must be greater than zero."))
        elif doc.doctype == "Filling Entry":
            frappe.throw(frappe._("Cartons Produced must be greater than zero."))
        else:
            frappe.throw(frappe._("Good Qty must be greater than zero."))

    scrap_qty = flt(getattr(doc, "scrap_qty", 0))

    # 5. Initialize Stock Entry
    se = frappe.new_doc("Stock Entry")
    se.purpose = "Manufacture"
    se.company = doc.company
    se.posting_date = doc.posting_date
    se.posting_time = getattr(doc, "posting_time", None) or frappe.utils.nowtime()
    se.from_bom = 1
    se.bom_no = doc.bom_no
    se.to_warehouse = target_wh

    # Enforce 9-decimal precision to prevent sub-milligram/dry-weight underflow
    if not hasattr(se, "_precision"):
        se._precision = frappe._dict()
    se._precision["items"] = frappe._dict(transfer_qty=9, qty=9)

    # 6. Consume Materials from Child Table (or fallback BOM explosion)
    consumption_rows = getattr(doc, "materials", None) or getattr(doc, "material_consumption", None) or []

    if consumption_rows:
        for row in consumption_rows:
            req_qty = flt(row.get("required_qty") if isinstance(row, dict) else getattr(row, "required_qty", 0))
            if req_qty <= 0:
                continue

            item_code = row.get("item_code") if isinstance(row, dict) else getattr(row, "item_code", None)
            src_wh = row.get("source_warehouse") if isinstance(row, dict) else getattr(row, "source_warehouse", None)
            uom = row.get("uom") if isinstance(row, dict) else getattr(row, "uom", None)

            if not src_wh:
                frappe.throw(frappe._("Source Warehouse is required for item {0} in Material Consumption.").format(item_code))

            stock_uom = frappe.db.get_value("Item", item_code, "stock_uom") or uom
            conv = 1.0
            if uom and stock_uom and uom != stock_uom:
                conv_data = get_conversion_factor(item_code, uom)
                conv = flt(conv_data.get("conversion_factor")) or 1.0

            transfer_qty = req_qty * conv
            se.append("items", {
                "item_code": item_code,
                "s_warehouse": src_wh,
                "qty": req_qty,
                "uom": uom or stock_uom,
                "stock_uom": stock_uom,
                "conversion_factor": conv,
                "transfer_qty": transfer_qty,
                "allow_zero_valuation_rate": 1
            })
    else:
        # Fallback to BOM explosion for backward compatibility
        total_batch_qty = good_qty + scrap_qty
        rm_items = get_bom_items(doc.bom_no, total_batch_qty)

        # Batch-fetch item groups if needed
        rm_item_codes = list({rm["item_code"] for rm in rm_items})
        item_groups = {
            d.name: d.item_group
            for d in frappe.get_all("Item", filters={"name": ["in", rm_item_codes]}, fields=["name", "item_group"])
        }

        for rm in rm_items:
            # Determine source warehouse based on DocType and legacy warehouse fields
            if doc.doctype in ["Water Purification Entry", "Blow Molding Entry"]:
                s_wh = getattr(doc, "source_warehouse", None)
                if not s_wh:
                    abbr = frappe.db.get_value("Company", doc.company, "abbr") or "W"
                    s_wh = frappe.db.get_value("Warehouse", {"company": doc.company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"
            elif doc.doctype == "Filling Entry":
                item_group = item_groups.get(rm["item_code"]) or frappe.db.get_value("Item", rm["item_code"], "item_group")
                s_wh = getattr(doc, "packaging_warehouse", None)
                if item_group == "Bulk Purified Water" or rm["item_code"] == "INT-BULK-WATER":
                    s_wh = getattr(doc, "water_warehouse", None) or s_wh
                elif item_group == "Empty Bottles" or rm["item_code"].startswith("INT-BTL"):
                    s_wh = getattr(doc, "bottle_warehouse", None) or s_wh

                if not s_wh:
                    abbr = frappe.db.get_value("Company", doc.company, "abbr") or "W"
                    if item_group == "Bulk Purified Water" or rm["item_code"] == "INT-BULK-WATER":
                        s_wh = frappe.db.get_value("Warehouse", {"company": doc.company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"
                    else:
                        s_wh = frappe.db.get_value("Warehouse", {"company": doc.company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"

            stock_uom = rm["stock_uom"]
            conv = rm["conversion_factor"]
            transfer_qty = flt(rm["qty"]) * conv
            se.append("items", {
                "item_code": rm["item_code"],
                "s_warehouse": s_wh,
                "qty": rm["qty"],
                "uom": rm["uom"],
                "stock_uom": stock_uom,
                "conversion_factor": conv,
                "transfer_qty": transfer_qty,
                "allow_zero_valuation_rate": 1
            })

    # 7. Append Finished Good row (STRICTLY Good Qty)
    fg_uom = frappe.db.get_value("Item", fg_item, "stock_uom")
    fg_batch = None
    if getattr(doc, "batch_no", None):
        has_batch = frappe.db.get_value("Item", fg_item, "has_batch_no")
        if has_batch:
            if not frappe.db.exists("Batch", {"item": fg_item, "batch_id": doc.batch_no}):
                b_doc = frappe.new_doc("Batch")
                b_doc.batch_id = doc.batch_no
                b_doc.item = fg_item
                b_doc.insert(ignore_permissions=True)
            fg_batch = doc.batch_no

    se.append("items", {
        "item_code": fg_item,
        "t_warehouse": target_wh,
        "qty": good_qty,
        "uom": fg_uom,
        "stock_uom": fg_uom,
        "conversion_factor": 1.0,
        "transfer_qty": good_qty,
        "allow_zero_valuation_rate": 0,
        "is_finished_item": 1,
        "batch_no": fg_batch
    })

    # 8. Set Remarks with MES Metadata
    remarks = [f"{doc.doctype}: {doc.name}"]
    if good_qty:
        remarks.append(f"Good Qty: {good_qty}")
    if scrap_qty > 0:
        remarks.append(f"Scrap Qty: {scrap_qty}")
    if getattr(doc, "batch_no", None):
        remarks.append(f"Batch No: {doc.batch_no}")
    if getattr(doc, "workstation", None):
        remarks.append(f"Workstation: {doc.workstation}")
    if getattr(doc, "operator", None):
        remarks.append(f"Operator: {doc.operator}")
    se.remarks = " | ".join(remarks)

    # 9. Set completed qty and submit
    se.fg_completed_qty = good_qty
    se.set_stock_entry_type()
    se.insert(ignore_permissions=True)
    se.submit()

    doc.stock_entry = se.name
    frappe.db.set_value(doc.doctype, doc.name, "stock_entry", se.name, update_modified=False)
    frappe.msgprint(f"Stock Entry {se.name} dynamically generated from BOM {doc.bom_no}.")


def cancel_linked_stock_entry(doc, method):
    """
    Hooked into on_cancel for Water Purification, Blow Molding, and Filling Entry.
    Cancels the linked Stock Entry automatically.
    """
    stock_entry_id = getattr(doc, "stock_entry", None) or frappe.db.get_value(doc.doctype, doc.name, "stock_entry")
    if stock_entry_id and frappe.db.exists("Stock Entry", stock_entry_id):
        se = frappe.get_doc("Stock Entry", stock_entry_id)
        if se.docstatus == 1:
            se.cancel()
            frappe.msgprint(f"Linked Stock Entry {se.name} cancelled automatically.")

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def item_group_query(doctype, txt, searchfield, start, page_len, filters):
    from erpnext.setup.doctype.item_group.item_group import get_child_item_groups
    
    conditions = []
    
    item_group = filters.get("item_group") if filters else None
    
    if item_group:
        # Get all child item groups recursively
        child_groups = get_child_item_groups(item_group)
        child_groups.append(item_group)
        
        # Format for SQL IN clause
        group_list = ", ".join([frappe.db.escape(g) for g in child_groups])
        conditions.append(f"tabItem.item_group IN ({group_list})")
        
    conditions.append("tabItem.disabled = 0")
    conditions.append("tabItem.is_stock_item = 1")
    
    if txt:
        conditions.append(f"(tabItem.name LIKE {frappe.db.escape('%'+txt+'%')} OR tabItem.item_name LIKE {frappe.db.escape('%'+txt+'%')})")
        
    where_clause = " AND ".join(conditions)
    
    return frappe.db.sql(f"""
        SELECT tabItem.name, tabItem.item_name, tabItem.description
        FROM tabItem
        WHERE {where_clause}
        ORDER BY tabItem.name
        LIMIT %(start)s, %(page_len)s
    """, {
        "start": start,
        "page_len": page_len
    })
