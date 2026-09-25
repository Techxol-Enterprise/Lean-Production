import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

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
    custom_fields = {
        "Sales Invoice": [
            {
                "fieldname": "bottle_tracking_section",
                "label": "Bottle Tracking (19L)",
                "fieldtype": "Section Break",
                "insert_after": "items",
            },
            {
                "fieldname": "full_bottles_delivered",
                "label": "Full Bottles Delivered (19L)",
                "fieldtype": "Int",
                "insert_after": "bottle_tracking_section",
            },
            {
                "fieldname": "empty_bottles_received",
                "label": "Empty Bottles Received (19L)",
                "fieldtype": "Int",
                "insert_after": "full_bottles_delivered",
            },
        ]
    }
    create_custom_fields(custom_fields, update=True)
    frappe.clear_cache(doctype="Sales Invoice")
    print("Bottle Tracking Custom Fields verified/created on Sales Invoice.")

def configure_deposit_account():
    companies = frappe.get_all("Company", pluck="name")
    if not companies:
        print("No companies found.")
        return

    account_name = "Customer Bottle Deposits"
    item_code = "19L-BOTTLE-DEPOSIT"

    for company in companies:
        abbr = frappe.db.get_value("Company", company, "abbr")
        account_id = f"{account_name} - {abbr}"

        # 1. Find suitable parent liability account
        parent_account = frappe.db.get_value("Account", {"account_name": ["in", ["Current Liabilities", "Other Current Liabilities"]], "company": company, "is_group": 1})
        if not parent_account:
            parent_account = frappe.db.get_value("Account", {"root_type": "Liability", "is_group": 1, "company": company})

        if not parent_account:
            print(f"Could not find group Liability account for {company}")
            continue

        # 2. Create or update Account
        if not frappe.db.exists("Account", account_id):
            acc = frappe.get_doc({
                "doctype": "Account",
                "account_name": account_name,
                "parent_account": parent_account,
                "is_group": 0,
                "company": company,
                "root_type": "Liability",
                "account_type": ""
            })
            acc.insert(ignore_permissions=True)
            print(f"Created Account: {account_id}")
        else:
            acc = frappe.get_doc("Account", account_id)
            if acc.account_type != "":
                acc.account_type = ""
                acc.save(ignore_permissions=True)
                print(f"Updated Account {account_id} account_type to blank.")

        # 3. Configure 19L-BOTTLE-DEPOSIT item default
        if frappe.db.exists("Item", item_code):
            item = frappe.get_doc("Item", item_code)
            matched = False
            for row in item.item_defaults:
                if row.company == company:
                    row.income_account = account_id
                    matched = True
                    break
            
            if not matched:
                item.append("item_defaults", {
                    "company": company,
                    "income_account": account_id
                })

            item.is_stock_item = 0
            item.save(ignore_permissions=True)
            print(f"Configured Item Default for {item_code} on {company}: income_account = {account_id}")
        else:
            print(f"Item {item_code} does not exist yet for {company}.")

    frappe.db.commit()

def setup():
    create_doctype()
    add_custom_fields()
    configure_deposit_account()
    frappe.db.commit()
    print("Bottle Tracking Setup Complete (DocType, Fields, and Deposit Accounts).")
