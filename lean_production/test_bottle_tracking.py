import frappe

def run_test():
    if not frappe.db.exists("Customer Group", "Commercial"):
        frappe.get_doc({"doctype": "Customer Group", "customer_group_name": "Commercial"}).insert(ignore_permissions=True)
    if not frappe.db.exists("Territory", "Local"):
        frappe.get_doc({"doctype": "Territory", "territory_name": "Local"}).insert(ignore_permissions=True)

    if not frappe.db.exists("Customer", "Test Customer"):
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": "Test Customer",
            "customer_group": "Commercial",
            "territory": "Local",
            "customer_type": "Company"
        })
        customer.insert(ignore_permissions=True)
    
    item = frappe.get_all("Item", limit=1)
    
    si = frappe.new_doc("Sales Invoice")
    si.customer = "Test Customer"
    si.append("items", {
        "item_code": item[0].name,
        "qty": 1,
        "rate": 100
    })
    si.full_bottles_delivered = 5
    si.empty_bottles_received = 3
    si.set_missing_values()
    si.insert()
    si.submit()
    
    ledgers = frappe.get_all("Customer Bottle Ledger", filters={"voucher_no": si.name})
    if ledgers:
        print(f"Test Passed: Created ledger {ledgers[0].name}")
    else:
        print("Test Failed: No ledger created.")
        
    si.cancel()
    
    ledgers = frappe.get_all("Customer Bottle Ledger", filters={"voucher_no": si.name})
    if not ledgers:
        print("Test Passed: Cancelled ledger.")
    else:
        print("Test Failed: Ledger not cancelled.")
