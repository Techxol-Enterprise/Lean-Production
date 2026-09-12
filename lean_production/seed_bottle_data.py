import frappe

def create_item(item_code, item_name, is_stock, rate):
    if not frappe.db.exists("Item", item_code):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": item_name,
            "item_group": "Products" if is_stock else "Services",
            "is_stock_item": 1 if is_stock else 0,
            "stock_uom": "Nos"
        })
        item.insert(ignore_permissions=True)
    
    price_list = frappe.db.get_value("Price List", {"selling": 1})
    if price_list and not frappe.db.exists("Item Price", {"item_code": item_code, "price_list": price_list}):
        price = frappe.get_doc({
            "doctype": "Item Price",
            "item_code": item_code,
            "price_list": price_list,
            "price_list_rate": rate
        })
        price.insert(ignore_permissions=True)

def create_customer(name):
    if not frappe.db.exists("Customer", name):
        frappe.get_doc({
            "doctype": "Customer",
            "customer_name": name,
            "customer_group": "Commercial",
            "territory": "Local",
            "customer_type": "Company"
        }).insert(ignore_permissions=True)

def create_invoice(customer, qty_full, qty_empty, is_new=False, is_vip=False):
    si = frappe.new_doc("Sales Invoice")
    si.customer = customer
    
    # Refill item
    si.append("items", {
        "item_code": "19L-REFILL",
        "qty": qty_full,
        "rate": 150
    })
    
    if is_new:
        deposit_row = si.append("items", {
            "item_code": "19L-BOTTLE-DEPOSIT",
            "qty": qty_full,
            "rate": 2000
        })
        if is_vip:
            deposit_row.discount_percentage = 100
            
    si.full_bottles_delivered = qty_full
    si.empty_bottles_received = qty_empty
    si.set_missing_values()
    si.insert(ignore_permissions=True)
    si.submit()
    print(f"Submitted Invoice {si.name} for {customer}: +{qty_full} -{qty_empty}")

def run():
    if not frappe.db.exists("Customer Group", "Commercial"):
        frappe.get_doc({"doctype": "Customer Group", "customer_group_name": "Commercial"}).insert(ignore_permissions=True)
    if not frappe.db.exists("Territory", "Local"):
        frappe.get_doc({"doctype": "Territory", "territory_name": "Local"}).insert(ignore_permissions=True)

    create_item("19L-REFILL", "19L Mineral Water (Refill)", True, 150)
    
    create_customer("Techxol Solutions Office")
    create_customer("Household A")
    create_customer("VIP Office B")

    print("Seeding invoices...")
    
    # Techxol gets 5 bottles initially (Deposit)
    create_invoice("Techxol Solutions Office", 5, 0, is_new=True)
    # Next day, Techxol returns 3 empty and takes 3 full
    create_invoice("Techxol Solutions Office", 3, 3)
    
    # Household gets 2 bottles initially (Deposit)
    create_invoice("Household A", 2, 0, is_new=True)
    # Household returns 0 empty but wants 1 more full
    create_invoice("Household A", 1, 0)
    
    # VIP gets 10 bottles initially (Waived)
    create_invoice("VIP Office B", 10, 0, is_new=True, is_vip=True)
    
    frappe.db.commit()
    print("Seeding Complete!")

