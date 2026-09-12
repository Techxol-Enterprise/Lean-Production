import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_doctype():
    if frappe.db.exists("DocType", "Customer Bottle Ledger"):
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Customer Bottle Ledger",
        "module": "Lean Production",
        "custom": 0,
        "istable": 0,
        "naming_rule": "Autoincrement",
        "autoname": "autoincrement",
        "fields": [
            {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "options": "Customer", "reqd": 1, "in_list_view": 1},
            {"fieldname": "posting_date", "label": "Posting Date", "fieldtype": "Date", "reqd": 1, "in_list_view": 1},
            {"fieldname": "voucher_type", "label": "Voucher Type", "fieldtype": "Data", "read_only": 1},
            {"fieldname": "voucher_no", "label": "Voucher No", "fieldtype": "Data", "read_only": 1, "in_list_view": 1},
            {"fieldname": "full_bottles_delivered", "label": "Full Bottles Delivered", "fieldtype": "Int", "in_list_view": 1},
            {"fieldname": "empty_bottles_received", "label": "Empty Bottles Received", "fieldtype": "Int", "in_list_view": 1}
        ]
    })
    doc.insert()
    
def add_custom_fields():
    create_custom_field("Sales Invoice", {
        "fieldname": "bottle_tracking_section",
        "label": "Bottle Tracking (19L)",
        "fieldtype": "Section Break",
        "insert_after": "items"
    })
    create_custom_field("Sales Invoice", {
        "fieldname": "full_bottles_delivered",
        "label": "Full Bottles Delivered (19L)",
        "fieldtype": "Int",
        "insert_after": "bottle_tracking_section"
    })
    create_custom_field("Sales Invoice", {
        "fieldname": "empty_bottles_received",
        "label": "Empty Bottles Received (19L)",
        "fieldtype": "Int",
        "insert_after": "full_bottles_delivered"
    })

def setup():
    create_doctype()
    add_custom_fields()
    frappe.db.commit()
    print("Doctype and Custom Fields created.")
