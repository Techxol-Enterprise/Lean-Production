import frappe
from frappe.utils import add_days, nowdate, now
import random

def seed_full_data():
    today = nowdate()
    now_str = now()
    company = frappe.db.get_value("Company", {}, "name") or "Test Company"
    
    print("Starting full data seed...")

    # Clear existing test data to avoid duplicates or clutter
    frappe.db.sql("DELETE FROM `tabWater Purification Entry` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabBlow Molding Entry` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabFilling Entry` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabCustomer Bottle Ledger` WHERE name >= 100000")
    frappe.db.sql("DELETE FROM `tabDelivery Note` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabPayment Entry` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabSales Invoice` WHERE name LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabSales Invoice Item` WHERE parent LIKE 'SEED-%'")
    frappe.db.sql("DELETE FROM `tabGL Entry` WHERE name LIKE 'SEED-%'")

    for i in range(180, -1, -1):
        p_date = add_days(today, -i)
        
        # Water
        frappe.db.sql("""
            INSERT INTO `tabWater Purification Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, good_qty, scrap_qty, qc_status)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s, %s, 'Pass')
        """, (f'SEED-WP-{i}', now_str, now_str, company, p_date, random.randint(10000, 15000), random.randint(100, 500)))

        # Blow Molding
        frappe.db.sql("""
            INSERT INTO `tabBlow Molding Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, good_qty, scrap_qty)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s, %s)
        """, (f'SEED-BM-{i}', now_str, now_str, company, p_date, random.randint(9000, 14000), random.randint(50, 200)))

        # Filling
        frappe.db.sql("""
            INSERT INTO `tabFilling Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, good_qty, scrap_qty)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s, %s)
        """, (f'SEED-FE-{i}', now_str, now_str, company, p_date, random.randint(8000, 13000), random.randint(20, 100)))

        # Bottle Ledger
        frappe.db.sql("""
            INSERT INTO `tabCustomer Bottle Ledger` 
            (name, creation, modified, modified_by, owner, docstatus, idx, posting_date, full_bottles_delivered, empty_bottles_received)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s)
        """, (i + 100000, now_str, now_str, p_date, random.randint(400, 800), random.randint(350, 750)))

        # Delivery Note
        frappe.db.sql("""
            INSERT INTO `tabDelivery Note` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, total)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s)
        """, (f'SEED-DN-{i}', now_str, now_str, company, p_date, random.randint(50000, 150000)))

        # Payment Entry
        frappe.db.sql("""
            INSERT INTO `tabPayment Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, paid_amount)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s)
        """, (f'SEED-PE-{i}', now_str, now_str, company, p_date, random.randint(40000, 120000)))

        # Sales Invoice
        si_name = f'SEED-SI-{i}'
        frappe.db.sql("""
            INSERT INTO `tabSales Invoice` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s)
        """, (si_name, now_str, now_str, company, p_date))

        # Sales Invoice Item
        frappe.db.sql("""
            INSERT INTO `tabSales Invoice Item` 
            (name, creation, modified, modified_by, owner, docstatus, idx, parent, parenttype, parentfield, qty)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, 'Sales Invoice', 'items', %s)
        """, (f'SEED-SII-{i}', now_str, now_str, si_name, random.randint(400, 800)))

        # GL Entry - Expense
        frappe.db.sql("""
            INSERT INTO `tabGL Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, account, debit)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'Indirect Expenses - TC', %s)
        """, (f'SEED-GLE-EXP-{i}', now_str, now_str, company, p_date, random.randint(10000, 30000)))

        # GL Entry - Cash
        frappe.db.sql("""
            INSERT INTO `tabGL Entry` 
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, account, debit)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'Cash - TC', %s)
        """, (f'SEED-GLE-CSH-{i}', now_str, now_str, company, p_date, random.randint(20000, 60000)))

    frappe.db.commit()
    print("Full data seed completed successfully.")

seed_full_data()
