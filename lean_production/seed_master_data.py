import frappe
from frappe.utils import today, nowtime, flt

def create_item_groups():
    groups = [
        "Raw Water", "Resins & Preforms", "Packaging Materials", 
        "Chemicals & Minerals", "Bulk Purified Water", "Empty Bottles", "Finished Goods"
    ]
    for g in groups:
        if not frappe.db.exists("Item Group", g):
            doc = frappe.new_doc("Item Group")
            doc.item_group_name = g
            doc.parent_item_group = "All Item Groups"
            doc.is_group = 0
            doc.insert(ignore_permissions=True)
            print(f"Created Item Group: {g}")

def create_uoms():
    for u in ["Litre", "Kg", "Nos", "Pack", "Unit", "Gram"]:
        if not frappe.db.exists("UOM", u):
            doc = frappe.new_doc("UOM")
            doc.uom_name = u
            doc.insert(ignore_permissions=True)
            print(f"Created UOM: {u}")

def create_uom_conversions():
    conversions = [
        {"from_uom": "Kg", "to_uom": "Gram", "value": 1000.0},
        {"from_uom": "Gram", "to_uom": "Kg", "value": 0.001}
    ]
    for c in conversions:
        if not frappe.db.exists("UOM Conversion Factor", {"from_uom": c["from_uom"], "to_uom": c["to_uom"]}):
            doc = frappe.new_doc("UOM Conversion Factor")
            doc.from_uom = c["from_uom"]
            doc.to_uom = c["to_uom"]
            doc.value = c["value"]
            doc.category = "Mass"
            doc.insert(ignore_permissions=True)
            print(f"Created UOM Conversion: {c['from_uom']} -> {c['to_uom']}")

def create_item(item_code, item_name, uom, item_group, is_stock=1, is_sales=0, is_purchase=1, uom_convs=None, valuation_rate=0.0):
    if not frappe.db.exists("Item", item_code):
        doc = frappe.new_doc("Item")
        doc.item_code = item_code
        doc.item_name = item_name
        doc.stock_uom = uom
        doc.item_group = item_group
        doc.is_stock_item = is_stock
        doc.is_sales_item = is_sales
        doc.is_purchase_item = is_purchase
        if valuation_rate:
            doc.valuation_rate = valuation_rate
        
        if uom_convs:
            for conv in uom_convs:
                doc.append("uoms", {
                    "uom": conv["uom"],
                    "conversion_factor": conv["factor"]
                })
        
        doc.insert(ignore_permissions=True)
        print(f"Created Item: {item_code}")
    else:
        doc = frappe.get_doc("Item", item_code)
        changed = False
        if doc.stock_uom != uom:
            doc.stock_uom = uom
            changed = True
        if doc.item_name != item_name:
            doc.item_name = item_name
            changed = True
        if valuation_rate and doc.valuation_rate != valuation_rate:
            doc.valuation_rate = valuation_rate
            changed = True
        if changed:
            doc.save(ignore_permissions=True)

        if uom_convs:
            existing_uoms = {d.uom: d for d in doc.uoms}
            uom_changed = False
            for conv in uom_convs:
                if conv["uom"] in existing_uoms:
                    row = existing_uoms[conv["uom"]]
                    if abs(flt(row.conversion_factor) - flt(conv["factor"])) > 1e-6:
                        row.conversion_factor = conv["factor"]
                        uom_changed = True
                else:
                    doc.append("uoms", {
                        "uom": conv["uom"],
                        "conversion_factor": conv["factor"]
                    })
                    uom_changed = True
            if uom_changed:
                doc.save(ignore_permissions=True)
        print(f"Verified/Updated Item: {item_code} (stock_uom: {doc.stock_uom})")

def create_bom(item_code, qty, items):
    # Check if an active BOM already exists for this item
    existing_boms = frappe.get_all("BOM", filters={"item": item_code, "is_active": 1, "docstatus": 1})
    if existing_boms:
        active_bom = frappe.get_doc("BOM", existing_boms[0].name)
        active_items_map = {d.item_code: (flt(d.qty), d.uom) for d in active_bom.items}
        mismatch = False
        if len(active_bom.items) != len(items) or abs(flt(active_bom.quantity) - flt(qty)) > 1e-4:
            mismatch = True
        else:
            for req in items:
                cur = active_items_map.get(req["item_code"])
                if not cur or cur[1] != req["uom"] or abs(cur[0] - flt(req["qty"])) > 1e-4:
                    mismatch = True
                    break

        if not mismatch:
            print(f"Active BOM already matches requirements for {item_code}: {active_bom.name}")
            return active_bom.name

        print(f"Active BOM for {item_code} has outdated items or UOMs. Recreating...")
        # Cancel dependent FG BOMs if needed before cancelling this BOM
        dependent_boms = list(set(frappe.get_all("BOM Item", filters={"item_code": item_code, "docstatus": 1}, pluck="parent")))
        for fg_bom in dependent_boms:
            if frappe.db.exists("BOM", fg_bom):
                fg_doc = frappe.get_doc("BOM", fg_bom)
                if fg_doc.docstatus == 1:
                    fg_doc.cancel()
                    print(f"Cancelled dependent BOM: {fg_bom}")
                frappe.delete_doc("BOM", fg_bom, force=True)

        active_bom.cancel()
        frappe.delete_doc("BOM", active_bom.name, force=True)
    
    doc = frappe.new_doc("BOM")
    doc.item = item_code
    doc.quantity = qty
    doc.is_active = 1
    doc.is_default = 1
    doc.with_operations = 0
    
    for row in items:
        doc.append("items", {
            "item_code": row["item_code"],
            "qty": row["qty"],
            "uom": row["uom"]
        })
        
    doc.insert(ignore_permissions=True)
    doc.submit()
    print(f"Created and Submitted BOM for: {item_code} ({doc.name})")
    return doc.name

def seed_opening_stock(company=None, warehouse=None):
    # Ensure allow_negative_stock is enabled in Stock Settings
    frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 1)

    company = company or frappe.db.get_single_value("Global Defaults", "default_company") or frappe.db.get_value("Company", {}, "name") or "Wateena"
    if not warehouse:
        warehouse = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name")
        if not warehouse:
            abbr = frappe.db.get_value("Company", company, "abbr") or "W"
            warehouse = f"Stores - {abbr}"

    stock_items = [
        {"item_code": "RM-WATER", "qty": 50000.0, "uom": "Litre", "basic_rate": 0.05},
        {"item_code": "MIN-SODIUM", "qty": 100.0, "uom": "Kg", "basic_rate": 10.0},
        {"item_code": "MIN-MAGNESIUM", "qty": 100.0, "uom": "Kg", "basic_rate": 15.0},
        {"item_code": "MIN-CALCIUM", "qty": 100.0, "uom": "Kg", "basic_rate": 12.0},
        {"item_code": "CHEM-ANTISCALE", "qty": 50.0, "uom": "Kg", "basic_rate": 25.0},
        {"item_code": "RM-PREFORM-15G", "qty": 1000.0, "uom": "Kg", "basic_rate": 5.0},
        {"item_code": "RM-PREFORM-30G", "qty": 1000.0, "uom": "Kg", "basic_rate": 6.0},
        {"item_code": "RM-CAP-28MM", "qty": 50000.0, "uom": "Nos", "basic_rate": 0.1},
        {"item_code": "RM-LBL-0.5L", "qty": 50000.0, "uom": "Nos", "basic_rate": 0.05},
        {"item_code": "RM-LBL-1.5L", "qty": 50000.0, "uom": "Nos", "basic_rate": 0.08},
        {"item_code": "RM-WRAP-12X", "qty": 1000.0, "uom": "Unit", "basic_rate": 1.0},
        {"item_code": "RM-WRAP-06X", "qty": 1000.0, "uom": "Unit", "basic_rate": 0.8},
    ]

    needed_items = []
    for item in stock_items:
        qty_in_wh = frappe.db.get_value("Bin", {"warehouse": warehouse, "item_code": item["item_code"]}, "actual_qty") or 0.0
        if qty_in_wh <= 10.0:
            needed_items.append(item)

    if not needed_items:
        print("Opening stock already sufficiently exists for all items.")
        return

    se = frappe.new_doc("Stock Entry")
    se.purpose = "Material Receipt"
    se.stock_entry_type = "Material Receipt"
    se.company = company
    se.to_warehouse = warehouse
    se.posting_date = today()
    se.posting_time = nowtime()

    for item in needed_items:
        se.append("items", {
            "item_code": item["item_code"],
            "t_warehouse": warehouse,
            "qty": item["qty"],
            "uom": item["uom"],
            "basic_rate": item["basic_rate"],
            "allow_zero_valuation_rate": 1
        })

    se.insert(ignore_permissions=True)
    se.submit()
    print(f"Seeded opening stock with Stock Entry: {se.name}")

def main(site=None, company=None):
    if not getattr(frappe.local, "site", None):
        site = site or "Wateena"
        frappe.init(site=site, sites_path="sites")
        frappe.connect()

    company = company or frappe.db.get_single_value("Global Defaults", "default_company") or frappe.db.get_value("Company", {}, "name") or "Wateena"

    create_item_groups()
    create_uoms()
    create_uom_conversions()

    # Create Items
    # Raw Materials
    create_item("RM-WATER", "Raw Untreated Water", "Litre", "Raw Water", is_purchase=0, valuation_rate=0.05)
    create_item("RM-PREFORM-15G", "PET Preform - 15g (for 500ml)", "Kg", "Resins & Preforms", valuation_rate=5.0)
    create_item("RM-PREFORM-30G", "PET Preform - 30g (for 1.5L)", "Kg", "Resins & Preforms", valuation_rate=6.0)
    create_item("RM-CAP-28MM", "28mm Standard Plastic Cap", "Nos", "Packaging Materials", valuation_rate=0.1)
    create_item("RM-LBL-0.5L", "Shrink Label - 500ml", "Nos", "Packaging Materials", valuation_rate=0.05)
    create_item("RM-LBL-1.5L", "Shrink Label - 1.5L", "Nos", "Packaging Materials", valuation_rate=0.08)
    create_item("RM-WRAP-12X", "Shrink Wrap Film (12-pack)", "Unit", "Packaging Materials", valuation_rate=1.0)
    create_item("RM-WRAP-06X", "Shrink Wrap Film (6-pack)", "Unit", "Packaging Materials", valuation_rate=0.8)

    # Chemicals & Minerals in dry weights: stock_uom = "Kg", UOM conversion to "Gram" = 0.001
    chem_conv = [{"uom": "Gram", "factor": 0.001}]
    create_item("MIN-SODIUM", "Sodium Mineral Salt", "Kg", "Chemicals & Minerals", uom_convs=chem_conv, valuation_rate=10.0)
    create_item("MIN-MAGNESIUM", "Magnesium Mineral Salt", "Kg", "Chemicals & Minerals", uom_convs=chem_conv, valuation_rate=15.0)
    create_item("MIN-CALCIUM", "Calcium Mineral Salt", "Kg", "Chemicals & Minerals", uom_convs=chem_conv, valuation_rate=12.0)
    create_item("CHEM-ANTISCALE", "RO Antiscalant Powder", "Kg", "Chemicals & Minerals", uom_convs=chem_conv, valuation_rate=25.0)

    # Intermediate
    create_item("INT-BULK-WATER", "Purified Mineral Water (Bulk)", "Litre", "Bulk Purified Water", is_purchase=0, valuation_rate=0.1)
    create_item("INT-BTL-0.5L", "Empty PET Bottle - 500ml", "Nos", "Empty Bottles", is_purchase=0, valuation_rate=0.1)
    create_item("INT-BTL-1.5L", "Empty PET Bottle - 1.5L", "Nos", "Empty Bottles", is_purchase=0, valuation_rate=0.2)

    # Finished Goods
    create_item("FG-WATER-0.5L-12", "Bottled Water - 500ml x 12 Pack", "Pack", "Finished Goods", is_sales=1, is_purchase=0, valuation_rate=3.0)
    create_item("FG-WATER-1.5L-06", "Bottled Water - 1.5L x 6 Pack", "Pack", "Finished Goods", is_sales=1, is_purchase=0, valuation_rate=3.0)

    frappe.db.commit()
    
    # Create BOMs
    # Stage 1: INT-BULK-WATER consuming dry active-ingredient weights per 500L batch in Grams
    create_bom("INT-BULK-WATER", 500, [
        {"item_code": "RM-WATER", "qty": 600, "uom": "Litre"},
        {"item_code": "MIN-CALCIUM", "qty": 100, "uom": "Gram"},
        {"item_code": "MIN-MAGNESIUM", "qty": 50, "uom": "Gram"},
        {"item_code": "MIN-SODIUM", "qty": 50, "uom": "Gram"},
        {"item_code": "CHEM-ANTISCALE", "qty": 2, "uom": "Gram"}
    ])

    create_bom("INT-BTL-0.5L", 1000, [
        {"item_code": "RM-PREFORM-15G", "qty": 15, "uom": "Kg"}
    ])

    create_bom("INT-BTL-1.5L", 1000, [
        {"item_code": "RM-PREFORM-30G", "qty": 30, "uom": "Kg"}
    ])

    create_bom("FG-WATER-0.5L-12", 1, [
        {"item_code": "INT-BULK-WATER", "qty": 6, "uom": "Litre"},
        {"item_code": "INT-BTL-0.5L", "qty": 12, "uom": "Nos"},
        {"item_code": "RM-CAP-28MM", "qty": 12, "uom": "Nos"},
        {"item_code": "RM-LBL-0.5L", "qty": 12, "uom": "Nos"},
        {"item_code": "RM-WRAP-12X", "qty": 1, "uom": "Unit"}
    ])

    create_bom("FG-WATER-1.5L-06", 1, [
        {"item_code": "INT-BULK-WATER", "qty": 9, "uom": "Litre"},
        {"item_code": "INT-BTL-1.5L", "qty": 6, "uom": "Nos"},
        {"item_code": "RM-CAP-28MM", "qty": 6, "uom": "Nos"},
        {"item_code": "RM-LBL-1.5L", "qty": 6, "uom": "Nos"},
        {"item_code": "RM-WRAP-06X", "qty": 1, "uom": "Unit"}
    ])

    # Seed opening inventory
    seed_opening_stock(company=company)

    frappe.db.commit()
    print("Master data and opening stock successfully seeded.")

if __name__ == "__main__":
    main()
