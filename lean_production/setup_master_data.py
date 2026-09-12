import frappe

def setup():
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        company = frappe.get_all("Company")[0].name

    # 1. Create Liability Account
    account_name = "Customer Bottle Deposits"
    parent_account = frappe.db.get_value("Account", {"account_type": "Payable", "company": company, "is_group": 1})
    if not parent_account:
        parent_account = frappe.db.get_value("Account", {"root_type": "Liability", "is_group": 1, "company": company})

    account_id = f"{account_name} - {frappe.db.get_value('Company', company, 'abbr')}"
    if not frappe.db.exists("Account", account_id):
        acc = frappe.get_doc({
            "doctype": "Account",
            "account_name": account_name,
            "parent_account": parent_account,
            "is_group": 0,
            "company": company,
            "account_type": "Payable"
        })
        acc.insert(ignore_permissions=True)
        print(f"Created Account: {acc.name}")
    else:
        print(f"Account exists: {account_id}")

    # 2. Create Security Deposit Item
    item_code = "19L-BOTTLE-DEPOSIT"
    if not frappe.db.exists("Item", item_code):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": "19L Bottle Security Deposit",
            "item_group": "Services",
            "is_stock_item": 0,
            "is_fixed_asset": 0,
            "include_item_in_manufacturing": 0,
            "stock_uom": "Nos",
        })
        item.append("item_defaults", {
            "company": company,
            "income_account": account_id
        })
        item.insert(ignore_permissions=True)
        print(f"Created Item: {item.name}")
    else:
        print(f"Item exists: {item_code}")

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
        print(f"Created Item Price: {price.price_list_rate} for {item_code}")
    else:
        print("Item Price exists or no selling price list found")

    frappe.db.commit()
    print("Master Data Setup Complete.")
