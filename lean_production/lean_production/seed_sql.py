import frappe
from frappe.utils import nowdate, now

def seed_sql():
    today = nowdate()
    now_str = now()
    company = frappe.db.get_value("Company", {}, "name") or "Test Company"
    
    # 1. Water Purification Entry
    if not frappe.db.sql("SELECT name FROM `tabWater Purification Entry` WHERE posting_date = %s", (today,)):
        frappe.db.sql("""
            INSERT INTO `tabWater Purification Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, good_qty, scrap_qty, qc_status)
            VALUES
            ('WP-TEST-001', %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 15000, 200, 'Pass')
        """, (now_str, now_str, company, today))
        
    # 2. Blow Molding Entry
    if not frappe.db.sql("SELECT name FROM `tabBlow Molding Entry` WHERE posting_date = %s", (today,)):
        frappe.db.sql("""
            INSERT INTO `tabBlow Molding Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, good_qty, scrap_qty)
            VALUES
            ('BM-TEST-001', %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 14500, 150)
        """, (now_str, now_str, company, today))

    # 3. Filling Entry
    if not frappe.db.sql("SELECT name FROM `tabFilling Entry` WHERE posting_date = %s", (today,)):
        frappe.db.sql("""
            INSERT INTO `tabFilling Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, good_qty, scrap_qty)
            VALUES
            ('FE-TEST-001', %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 14000, 50)
        """, (now_str, now_str, company, today))
        


    frappe.db.commit()
    print("Seeded test data successfully via SQL.")

seed_sql()
