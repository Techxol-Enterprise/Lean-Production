import frappe

def rollback():
    # 1. Delete all seeded data
    frappe.db.sql("DELETE FROM `tabWater Purification Entry` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabBlow Molding Entry` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabFilling Entry` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabCustomer Bottle Ledger` WHERE name >= 100000") # My manual integer seed
    frappe.db.sql("DELETE FROM `tabDelivery Note` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabPayment Entry` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabSales Invoice` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabSales Invoice Item` WHERE parent LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabGL Entry` WHERE name LIKE 'SEED-%'")
    print("Deleted all seeded data.")

    # 2. Delete all Lean Production Dashboard Charts and Number Cards
    charts = frappe.get_all("Dashboard Chart", filters={"module": "Lean Production"})
    for chart in charts:
        frappe.delete_doc("Dashboard Chart", chart.name, ignore_permissions=True, force=1)
        
    cards = frappe.get_all("Number Card", filters={"module": "Lean Production"})
    for card in cards:
        frappe.delete_doc("Number Card", card.name, ignore_permissions=True, force=1)
    
    frappe.db.commit()
    print("Deleted modified Dashboard Charts and Number Cards.")

rollback()
