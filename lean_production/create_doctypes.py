import sys
import os
import frappe

def create_doctype(name, module, fields):
    if frappe.db.exists("DocType", name):
        print(f"DocType {name} already exists.")
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": name,
        "module": module,
        "custom": 1,
        "istable": 0,
        "naming_rule": "Expression",
        "autoname": f"format:{{{{YY}}}}-{{{{MM}}}}-{{{{DD}}}}-{{{{###}}}}",
        "fields": fields,
        "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1}],
        "is_submittable": 1
    })
    doc.insert(ignore_permissions=True)
    print(f"Created {name}")

def main():
    frappe.init(site="Wateena", sites_path="sites")
    frappe.connect()

    # Water Purification Entry
    create_doctype("Water Purification Entry", "Lean Production", [
        {"fieldname": "company", "fieldtype": "Link", "options": "Company", "label": "Company", "reqd": 1},
        {"fieldname": "posting_date", "fieldtype": "Date", "label": "Posting Date", "reqd": 1, "default": "Today"},
        {"fieldname": "shift", "fieldtype": "Select", "label": "Shift", "options": "Morning\nEvening\nNight"},
        {"fieldname": "mineral_water_item", "fieldtype": "Link", "options": "Item", "label": "Mineral Water Item (Bulk)", "reqd": 1},
        {"fieldname": "bom_no", "fieldtype": "Link", "options": "BOM", "label": "BOM No", "reqd": 1},
        {"fieldname": "litres_purified", "fieldtype": "Float", "label": "Litres Purified", "reqd": 1},
        {"fieldname": "source_warehouse", "fieldtype": "Link", "options": "Warehouse", "label": "Source Warehouse (Raw)", "reqd": 1},
        {"fieldname": "target_warehouse", "fieldtype": "Link", "options": "Warehouse", "label": "Target Warehouse (Bulk Tank)", "reqd": 1},
        {"fieldname": "qc_status", "fieldtype": "Select", "label": "QC Status", "options": "Pass\nFail", "reqd": 1},
        {"fieldname": "stock_entry", "fieldtype": "Link", "options": "Stock Entry", "label": "Linked Stock Entry", "read_only": 1, "no_copy": 1}
    ])

    # Blow Molding Entry
    create_doctype("Blow Molding Entry", "Lean Production", [
        {"fieldname": "company", "fieldtype": "Link", "options": "Company", "label": "Company", "reqd": 1},
        {"fieldname": "posting_date", "fieldtype": "Date", "label": "Posting Date", "reqd": 1, "default": "Today"},
        {"fieldname": "shift", "fieldtype": "Select", "label": "Shift", "options": "Morning\nEvening\nNight"},
        {"fieldname": "bottle_item", "fieldtype": "Link", "options": "Item", "label": "Empty Bottle Item", "reqd": 1},
        {"fieldname": "bom_no", "fieldtype": "Link", "options": "BOM", "label": "BOM No", "reqd": 1},
        {"fieldname": "bottles_produced_qty", "fieldtype": "Float", "label": "Bottles Produced (Qty)", "reqd": 1},
        {"fieldname": "source_warehouse", "fieldtype": "Link", "options": "Warehouse", "label": "Source Warehouse (Preforms)", "reqd": 1},
        {"fieldname": "target_warehouse", "fieldtype": "Link", "options": "Warehouse", "label": "Target Warehouse (Intermediate Bottles)", "reqd": 1},
        {"fieldname": "stock_entry", "fieldtype": "Link", "options": "Stock Entry", "label": "Linked Stock Entry", "read_only": 1, "no_copy": 1}
    ])

    # Filling Entry
    create_doctype("Filling Entry", "Lean Production", [
        {"fieldname": "company", "fieldtype": "Link", "options": "Company", "label": "Company", "reqd": 1},
        {"fieldname": "posting_date", "fieldtype": "Date", "label": "Posting Date", "reqd": 1, "default": "Today"},
        {"fieldname": "shift", "fieldtype": "Select", "label": "Shift", "options": "Morning\nEvening\nNight"},
        {"fieldname": "finished_good_item", "fieldtype": "Link", "options": "Item", "label": "Finished Good Item (Carton)", "reqd": 1},
        {"fieldname": "bom_no", "fieldtype": "Link", "options": "BOM", "label": "BOM No", "reqd": 1},
        {"fieldname": "cartons_produced", "fieldtype": "Float", "label": "Cartons Produced", "reqd": 1},
        {"fieldname": "water_warehouse", "fieldtype": "Link", "options": "Warehouse", "label": "Water Warehouse (Bulk Tank)", "reqd": 1},
        {"fieldname": "bottle_warehouse", "fieldtype": "Link", "options": "Warehouse", "label": "Bottle Warehouse (Intermediate)", "reqd": 1},
        {"fieldname": "packaging_warehouse", "fieldtype": "Link", "options": "Warehouse", "label": "Packaging Warehouse (Caps/Labels/Shrink)", "reqd": 1},
        {"fieldname": "fg_warehouse", "fieldtype": "Link", "options": "Warehouse", "label": "Finished Goods Warehouse", "reqd": 1},
        {"fieldname": "stock_entry", "fieldtype": "Link", "options": "Stock Entry", "label": "Linked Stock Entry", "read_only": 1, "no_copy": 1}
    ])

    frappe.db.commit()

main()
