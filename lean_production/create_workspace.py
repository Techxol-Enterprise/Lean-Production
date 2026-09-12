import frappe
import json

def run():
    if not frappe.db.exists("Workspace", "Lean Production"):
        doc = frappe.get_doc({
            "doctype": "Workspace",
            "name": "Lean Production",
            "label": "Lean Production",
            "title": "Lean Production",
            "module": "Lean Production",
            "app": "lean_production",
            "type": "Workspace",
            "icon": "drop",  # or 'droplet', 'tint'
            "indicator_color": "blue",
            "public": 1,
            "content": json.dumps([
                {"id": "header_production", "type": "header", "data": {"text": "<span class=\"h4\"><b>Manufacturing</b></span>", "col": 12}},
                {"id": "shortcut_water", "type": "shortcut", "data": {"shortcut_name": "Water Purification Entry", "col": 4}},
                {"id": "shortcut_blow", "type": "shortcut", "data": {"shortcut_name": "Blow Molding Entry", "col": 4}},
                {"id": "shortcut_fill", "type": "shortcut", "data": {"shortcut_name": "Filling Entry", "col": 4}},
                {"id": "header_bottles", "type": "header", "data": {"text": "<span class=\"h4\"><b>Bottle Tracking</b></span>", "col": 12}},
                {"id": "shortcut_ledger", "type": "shortcut", "data": {"shortcut_name": "Customer Bottle Ledger", "col": 4}},
                {"id": "shortcut_report", "type": "shortcut", "data": {"shortcut_name": "Bottles with Customers", "col": 4}},
            ])
        })
        doc.insert(ignore_permissions=True)
        print("Workspace created")
    else:
        print("Workspace already exists")
    frappe.db.commit()

