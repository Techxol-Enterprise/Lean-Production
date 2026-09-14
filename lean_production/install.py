import frappe
from lean_production.setup_item_groups import setup_lean_item_groups

def after_install():
    # 0. Provision and align Lean Production Item Group hierarchy
    setup_lean_item_groups()

    # Attempt to find the default company or the first company
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        companies = frappe.get_all("Company", limit=1)
        if companies:
            company = companies[0].name
        else:
            return # Cannot setup without a company

    # 1. Create Liability Account
    account_name = "Customer Bottle Deposits"
    parent_account = frappe.db.get_value("Account", {"account_type": "Payable", "company": company, "is_group": 1})
    if not parent_account:
        parent_account = frappe.db.get_value("Account", {"root_type": "Liability", "is_group": 1, "company": company})

    if parent_account:
        account_id = f"{account_name} - {frappe.db.get_value('Company', company, 'abbr')}"
        if not frappe.db.exists("Account", account_id):
            acc = frappe.get_doc({
                "doctype": "Account",
                "account_name": account_name,
                "parent_account": parent_account,
                "is_group": 0,
                "company": company,
                "account_type": ""
            })
            acc.insert(ignore_permissions=True)

    # 2. Create Security Deposit Item
    item_code = "19L-BOTTLE-DEPOSIT"
    if not frappe.db.exists("Item", item_code):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": "19L Bottle Security Deposit",
            "item_group": "Services" if frappe.db.exists("Item Group", "Services") else "All Item Groups",
            "is_stock_item": 0,
            "is_fixed_asset": 0,
            "include_item_in_manufacturing": 0,
            "stock_uom": "Nos",
        })
        if parent_account:
            item.append("item_defaults", {
                "company": company,
                "income_account": account_id
            })
        item.insert(ignore_permissions=True)

    # 3. Create Item Price (2000 Rs)
    price_list = frappe.db.get_value("Price List", {"selling": 1})
    if price_list and not frappe.db.exists("Item Price", {"item_code": item_code, "price_list": price_list}):
        price = frappe.get_doc({
            "doctype": "Item Price",
            "item_code": item_code,
            "price_list": price_list,
            "price_list_rate": 2000
        })
        price.insert(ignore_permissions=True)
