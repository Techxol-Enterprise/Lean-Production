import frappe
from frappe.utils import flt, today, nowtime


def run_mes_filling_test():
    """
    Automated acceptance criteria test script for Lean Production MES Filling Entry:
    Programmatically creates a Filling Entry with 100 Good Qty and 5 Scrap Qty,
    populates the Lean Material Consumption child table, submits it, and asserts:
    1. The linked Stock Entry (Manufacture) was created and submitted (docstatus == 1).
    2. Finished Goods yield is strictly 100.0 (fg_completed_qty == 100.0).
    3. Finished Goods row has qty == 100.0, target_warehouse == fg_wh.
    4. Raw materials consumed full 105 units worth:
       - 630L bulk water (INT-BULK-WATER) from Finished Goods - W
       - 1260 bottles (INT-BTL-0.5L) from Stores - W
       - 1260 caps (RM-CAP-28MM) from Stores - W
       - 1260 labels (RM-LBL-0.5L) from Stores - W
       - 105 shrink wrap (RM-WRAP-12X) from Stores - W
    5. Line-item warehouses preserved from child table rows.
    6. Incoming valuation equals outgoing valuation with scrap cost absorbed into FG unit valuation.
    7. Canceling Filling Entry cleanly cancels linked Stock Entry.
    8. Prints "PASS" to console on success.
    """
    if not getattr(frappe.local, "site", None):
        frappe.init(site="Wateena", sites_path="sites")
        frappe.connect()

    frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 1)

    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    stores_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"
    fg_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"

    fg_item = "FG-WATER-0.5L-12"
    bom_no = frappe.db.get_value("BOM", {"item": fg_item, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active submitted BOM for {fg_item} must exist"

    good_qty = 100.0
    scrap_qty = 5.0
    total_batch_qty = good_qty + scrap_qty  # 105.0

    fe = frappe.get_doc({
        "doctype": "Filling Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "finished_good_item": fg_item,
        "bom_no": bom_no,
        "good_qty": good_qty,
        "scrap_qty": scrap_qty,
        "cartons_produced": good_qty,
        "fg_warehouse": fg_wh,
        "batch_no": "BATCH-2026-09-001"
    })

    # Call get_bom_material_details to explode materials dynamically
    from lean_production.stock_automation import get_bom_material_details
    bom_materials = get_bom_material_details(
        item_code=fg_item,
        bom_no=bom_no,
        total_qty=total_batch_qty,
        company=company
    )

    for item in bom_materials:
        fe.append("materials", {
            "item_code": item["item_code"],
            "required_qty": item["required_qty"],
            "uom": item["uom"],
            "source_warehouse": item["source_warehouse"],
            "available_stock": item["available_stock"]
        })

    fe.insert(ignore_permissions=True)
    fe.submit()

    stock_entry_id = fe.stock_entry or frappe.db.get_value("Filling Entry", fe.name, "stock_entry")
    assert stock_entry_id, f"Filling Entry {fe.name} must have a linked Stock Entry"

    se = frappe.get_doc("Stock Entry", stock_entry_id)
    assert se.docstatus == 1, f"Stock Entry {se.name} must be submitted (docstatus=1)"
    assert se.purpose == "Manufacture", f"Stock Entry purpose must be Manufacture, got {se.purpose}"
    assert se.from_bom == 1, "Stock Entry must be linked from BOM"

    # ASSERTION 1: Finished Goods completed qty strictly matches good_qty (100)
    assert flt(se.fg_completed_qty) == good_qty, f"fg_completed_qty must be {good_qty}, got {se.fg_completed_qty}"

    # ASSERTION 2: Exactly 1 Finished Item row yielding 100 units into FG Warehouse
    fg_items = [d for d in se.items if d.is_finished_item]
    assert len(fg_items) == 1, f"Expected 1 FG row, found {len(fg_items)}"
    fg_row = fg_items[0]
    assert fg_row.item_code == fg_item, f"Finished item must be {fg_item}, got {fg_row.item_code}"
    assert flt(fg_row.qty) == good_qty, f"Finished item qty must be {good_qty}, got {fg_row.qty}"
    assert fg_row.t_warehouse == fg_wh, f"Target warehouse must be {fg_wh}, got {fg_row.t_warehouse}"

    # ASSERTION 3: Consumed Raw Materials correctly absorbed scrap (total 105 units consumed)
    rm_items = {d.item_code: d for d in se.items if not d.is_finished_item}
    expected_consumptions = {
        "INT-BULK-WATER": (630.0, fg_wh),
        "INT-BTL-0.5L": (1260.0, stores_wh),
        "RM-CAP-28MM": (1260.0, stores_wh),
        "RM-LBL-0.5L": (1260.0, stores_wh),
        "RM-WRAP-12X": (105.0, stores_wh),
    }

    for item_code, (expected_qty, expected_wh) in expected_consumptions.items():
        assert item_code in rm_items, f"Raw material {item_code} was not consumed in Stock Entry"
        row = rm_items[item_code]
        assert abs(flt(row.qty) - expected_qty) < 1e-4, (
            f"Item {item_code} consumed qty must be {expected_qty} (absorbing scrap), got {row.qty}"
        )
        assert row.s_warehouse == expected_wh, (
            f"Item {item_code} source warehouse must be {expected_wh}, got {row.s_warehouse}"
        )

    # ASSERTION 4: Cost Capitalization & Valuation Integrity (zero value loss)
    assert flt(se.total_incoming_value) > 0, "Total incoming value must be positive"
    assert flt(se.total_outgoing_value) > 0, "Total outgoing value must be positive"
    assert abs(flt(se.total_incoming_value) - flt(se.total_outgoing_value)) < 1e-4, (
        f"Incoming value ({se.total_incoming_value}) must match outgoing value ({se.total_outgoing_value})"
    )
    assert abs(flt(se.value_difference)) < 1e-4, f"Value difference must be 0, got {se.value_difference}"
    assert flt(fg_row.valuation_rate) > 0, "Finished good valuation rate must be positive"

    # ASSERTION 5: MES Metadata recorded in Remarks
    assert "BATCH-2026-09-001" in (se.remarks or ""), "Batch No must be recorded in remarks"
    assert "Good Qty: 100.0" in (se.remarks or "") or "Good Qty: 100" in (se.remarks or ""), "Good Qty must be recorded in remarks"
    assert "Scrap Qty: 5.0" in (se.remarks or "") or "Scrap Qty: 5" in (se.remarks or ""), "Scrap Qty must be recorded in remarks"

    # ASSERTION 6: Automatic Two-Way Cancellation Integrity
    fe.cancel()
    se.reload()
    assert se.docstatus == 2, f"Stock Entry {se.name} must be cancelled automatically upon Filling Entry cancellation"

    frappe.db.commit()
    print("PASS")
    return "PASS"


def run_mes_purification_test():
    """
    Automated acceptance criteria test script for Lean Production MES Water Purification Entry:
    Creates Water Purification Entry with 500L Good Qty and 25L Scrap Qty (total 525L consumed).
    """
    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    stores_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"
    fg_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"

    item_code = "INT-BULK-WATER"
    bom_no = frappe.db.get_value("BOM", {"item": item_code, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active submitted BOM for {item_code} must exist"

    good_qty = 500.0
    scrap_qty = 25.0
    total_qty = good_qty + scrap_qty  # 525.0

    wpe = frappe.get_doc({
        "doctype": "Water Purification Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "mineral_water_item": item_code,
        "bom_no": bom_no,
        "good_qty": good_qty,
        "scrap_qty": scrap_qty,
        "target_warehouse": fg_wh,
        "qc_status": "Pass",
        "batch_no": "BATCH-WP-001"
    })

    from lean_production.stock_automation import get_bom_material_details
    bom_materials = get_bom_material_details(
        item_code=item_code,
        bom_no=bom_no,
        total_qty=total_qty,
        company=company
    )

    for it in bom_materials:
        wpe.append("materials", {
            "item_code": it["item_code"],
            "required_qty": it["required_qty"],
            "uom": it["uom"],
            "source_warehouse": stores_wh,
            "available_stock": it["available_stock"]
        })

    wpe.insert(ignore_permissions=True)
    wpe.submit()

    se = frappe.get_doc("Stock Entry", wpe.stock_entry)
    assert se.docstatus == 1
    assert flt(se.fg_completed_qty) == 500.0
    fg_row = next(d for d in se.items if d.is_finished_item)
    assert flt(fg_row.qty) == 500.0
    assert abs(flt(se.total_incoming_value) - flt(se.total_outgoing_value)) < 1e-4

    wpe.cancel()
    se.reload()
    assert se.docstatus == 2
    frappe.db.commit()


def run_mes_blow_molding_test():
    """
    Automated acceptance criteria test script for Lean Production MES Blow Molding Entry:
    Creates Blow Molding Entry with 1000 Good Qty and 50 Scrap Qty (total 1050 consumed).
    """
    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    stores_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"

    item_code = "INT-BTL-0.5L"
    bom_no = frappe.db.get_value("BOM", {"item": item_code, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active submitted BOM for {item_code} must exist"

    good_qty = 1000.0
    scrap_qty = 50.0
    total_qty = good_qty + scrap_qty  # 1050.0

    bme = frappe.get_doc({
        "doctype": "Blow Molding Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "bottle_item": item_code,
        "bom_no": bom_no,
        "good_qty": good_qty,
        "scrap_qty": scrap_qty,
        "target_warehouse": stores_wh,
        "batch_no": "BATCH-BM-001"
    })

    from lean_production.stock_automation import get_bom_material_details
    bom_materials = get_bom_material_details(
        item_code=item_code,
        bom_no=bom_no,
        total_qty=total_qty,
        company=company
    )

    for it in bom_materials:
        bme.append("materials", {
            "item_code": it["item_code"],
            "required_qty": it["required_qty"],
            "uom": it["uom"],
            "source_warehouse": stores_wh,
            "available_stock": it["available_stock"]
        })

    bme.insert(ignore_permissions=True)
    bme.submit()

    se = frappe.get_doc("Stock Entry", bme.stock_entry)
    assert se.docstatus == 1
    assert flt(se.fg_completed_qty) == 1000.0
    fg_row = next(d for d in se.items if d.is_finished_item)
    assert flt(fg_row.qty) == 1000.0
    assert abs(flt(se.total_incoming_value) - flt(se.total_outgoing_value)) < 1e-4

    bme.cancel()
    se.reload()
    assert se.docstatus == 2
    frappe.db.commit()


def main():
    res = run_mes_filling_test()
    run_mes_purification_test()
    run_mes_blow_molding_test()
    return res


if __name__ == "__main__":
    main()
