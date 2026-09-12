import frappe
from frappe.utils import add_days, today, now, flt
import random

def seed_demo_data():
    current_date = today()
    now_str = now()
    company = "Wateena"

    print("=== [1/6] Seeding Workstations ===")
    workstations = [
        {"workstation_name": "RO Membrane Skid 1", "production_capacity": 2000},
        {"workstation_name": "Ozonation & UV Station", "production_capacity": 2500},
        {"workstation_name": "Pre-Treatment Sand/Carbon Filter", "production_capacity": 3000},
    ]
    for ws_data in workstations:
        w_name = ws_data["workstation_name"]
        if not frappe.db.exists("Workstation", w_name):
            doc = frappe.new_doc("Workstation")
            doc.workstation_name = w_name
            doc.production_capacity = ws_data["production_capacity"]
            doc.insert(ignore_permissions=True)
            print(f"  + Workstation created: {w_name}")

    print("=== [2/6] Seeding Inventory Bins (FG & RM Stock) ===")
    frappe.db.sql("DELETE FROM `tabBin` WHERE item_code LIKE 'FG-%' OR item_code LIKE 'RM-%'")
    bins = [
        {"item_code": "FG-WATER-0.5L-12", "warehouse": "Finished Goods - W", "qty": 2850, "uom": "Carton"},
        {"item_code": "FG-WATER-1.5L-06", "warehouse": "Finished Goods - W", "qty": 1640, "uom": "Carton"},
        {"item_code": "RM-PREFORM-15G", "warehouse": "Stores - W", "qty": 35000, "uom": "Nos"},
        {"item_code": "RM-PREFORM-30G", "warehouse": "Stores - W", "qty": 22000, "uom": "Nos"},
        {"item_code": "RM-CAP-28MM", "warehouse": "Stores - W", "qty": 45000, "uom": "Nos"},
        {"item_code": "RM-LBL-0.5L", "warehouse": "Stores - W", "qty": 32000, "uom": "Nos"},
        {"item_code": "RM-LBL-1.5L", "warehouse": "Stores - W", "qty": 20000, "uom": "Nos"},
        {"item_code": "RM-WATER", "warehouse": "Stores - W", "qty": 50000, "uom": "Litre"},
        {"item_code": "RM-WRAP-12X", "warehouse": "Stores - W", "qty": 4200, "uom": "Roll"},
    ]
    for b in bins:
        frappe.db.sql("""
            INSERT INTO `tabBin`
            (name, creation, modified, modified_by, owner, docstatus, idx, item_code, warehouse, actual_qty, stock_uom, company, valuation_rate, stock_value)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 0, 0, %s, %s, %s, %s, %s, 10.0, %s)
        """, (f"{b['item_code']}-{b['warehouse']}", now_str, now_str, b["item_code"], b["warehouse"], b["qty"], b["uom"], company, b["qty"] * 10.0))
    print(f"  + Seeded {len(bins)} inventory bins for FG and RM items.")

    print("=== [3/6] Cleaning Previous Demo Transactions ===")
    frappe.db.sql("DELETE FROM `tabWater Purification Entry` WHERE name LIKE 'DEMO-%'")
    frappe.db.sql("DELETE FROM `tabBlow Molding Entry` WHERE name LIKE 'DEMO-%'")
    frappe.db.sql("DELETE FROM `tabFilling Entry` WHERE name LIKE 'DEMO-%'")
    frappe.db.sql("DELETE FROM `tabCustomer Bottle Ledger` WHERE voucher_no LIKE 'DEMO-%'")
    frappe.db.sql("DELETE FROM `tabDelivery Note` WHERE name LIKE 'DEMO-%'")
    frappe.db.sql("DELETE FROM `tabSales Invoice` WHERE name LIKE 'DEMO-%'")
    frappe.db.sql("DELETE FROM `tabSales Invoice Item` WHERE parent LIKE 'DEMO-%'")
    frappe.db.sql("DELETE FROM `tabGL Entry` WHERE name LIKE 'DEMO-%'")

    print("=== [4/6] Seeding 180 Days of Historical Trends ===")
    customers = ["VIP Office B", "Household A", "Techxol Solutions Office", "Test Customer"]
    ws_names = ["RO Membrane Skid 1", "Ozonation & UV Station", "Pre-Treatment Sand/Carbon Filter"]

    for i in range(180, 0, -1):
        p_date = add_days(current_date, -i)
        
        # Water Purification (Daily trend, QC status, and Workstation group-by)
        qc_status = "Pass" if random.random() > 0.05 else "Fail"
        ws_choice = random.choice(ws_names)
        water_good = random.randint(8000, 14000)
        water_scrap = random.randint(50, 250)
        frappe.db.sql("""
            INSERT INTO `tabWater Purification Entry`
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, mineral_water_item, bom_no, target_warehouse, good_qty, scrap_qty, qc_status, workstation)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'INT-BULK-WATER', 'BOM-INT-BULK-WATER-001', 'Bulk Tanks - W', %s, %s, %s, %s)
        """, (f"DEMO-WP-{i}", p_date, p_date, company, p_date, water_good, water_scrap, qc_status, ws_choice))

        # Blow Molding Entry
        bm_good = random.randint(5000, 9500)
        bm_scrap = random.randint(30, 120)
        frappe.db.sql("""
            INSERT INTO `tabBlow Molding Entry`
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, bottle_item, bom_no, target_warehouse, good_qty, scrap_qty)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'INT-BTL-0.5L', 'BOM-INT-BTL-0.5L-001', 'Stores - W', %s, %s)
        """, (f"DEMO-BM-{i}", p_date, p_date, company, p_date, bm_good, bm_scrap))

        # Filling Entry
        fe_good = random.randint(4000, 8500)
        fe_scrap = random.randint(15, 60)
        fg_item = random.choice(["FG-WATER-0.5L-12", "FG-WATER-1.5L-06"])
        frappe.db.sql("""
            INSERT INTO `tabFilling Entry`
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, finished_good_item, bom_no, fg_warehouse, good_qty, scrap_qty)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s, 'BOM-FG-WATER-0.5L-12-001', 'Finished Goods - W', %s, %s)
        """, (f"DEMO-FE-{i}", p_date, p_date, company, p_date, fg_item, fe_good, fe_scrap))

        # Customer Bottle Ledger (every 2-3 days)
        if i % 2 == 0:
            cust = random.choice(customers)
            deliv = random.randint(20, 65)
            recv = random.randint(15, 60)
            frappe.db.sql("""
                INSERT INTO `tabCustomer Bottle Ledger`
                (name, creation, modified, modified_by, owner, docstatus, idx, company, customer, posting_date, voucher_type, voucher_no, full_bottles_delivered, empty_bottles_received)
                VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s, 'Sales Invoice', %s, %s, %s)
            """, (i + 1000, p_date, p_date, company, cust, p_date, f"DEMO-SI-{i}", deliv, recv))

        # Delivery Note (for Delivery OTIF Trend)
        frappe.db.sql("""
            INSERT INTO `tabDelivery Note`
            (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, total_qty)
            VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s)
        """, (f"DEMO-DN-{i}", p_date, p_date, company, p_date, random.randint(150, 450)))

        # Sales Invoice & Sales Invoice Item
        if i % 3 == 0:
            si_name = f"DEMO-SI-{i}"
            cust = random.choice(customers)
            grand_total = random.randint(25000, 85000)
            outstanding = random.randint(0, grand_total // 2)
            frappe.db.sql("""
                INSERT INTO `tabSales Invoice`
                (name, creation, modified, modified_by, owner, docstatus, idx, company, customer, posting_date, grand_total, outstanding_amount)
                VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, %s, %s, %s)
            """, (si_name, p_date, p_date, company, cust, p_date, grand_total, outstanding))

            frappe.db.sql("""
                INSERT INTO `tabSales Invoice Item`
                (name, creation, modified, modified_by, owner, docstatus, idx, parent, parenttype, parentfield, item_code, qty, rate, amount)
                VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, 'Sales Invoice', 'items', %s, %s, 150.0, %s)
            """, (f"DEMO-SII-{i}", p_date, p_date, si_name, fg_item, random.randint(100, 400), grand_total))

        # GL Entries (Cash & Indirect Expenses)
        if i % 5 == 0:
            frappe.db.sql("""
                INSERT INTO `tabGL Entry`
                (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, account, debit)
                VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'Cash - W', %s)
            """, (f"DEMO-GLE-CSH-{i}", p_date, p_date, company, p_date, random.randint(30000, 90000)))

            frappe.db.sql("""
                INSERT INTO `tabGL Entry`
                (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, account, debit)
                VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'Indirect Expenses - W', %s)
            """, (f"DEMO-GLE-EXP-{i}", p_date, p_date, company, p_date, random.randint(15000, 45000)))

    print("=== [5/6] Seeding Today's Production & Month-to-Date Records ===")
    # Today's Water Purification
    frappe.db.sql("""
        INSERT INTO `tabWater Purification Entry`
        (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, mineral_water_item, bom_no, target_warehouse, good_qty, scrap_qty, qc_status, workstation)
        VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'INT-BULK-WATER', 'BOM-INT-BULK-WATER-001', 'Bulk Tanks - W', 9500, 120, 'Pass', 'RO Membrane Skid 1')
    """, ("DEMO-WP-TODAY", now_str, now_str, company, current_date))

    # Today's Blow Molding
    frappe.db.sql("""
        INSERT INTO `tabBlow Molding Entry`
        (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, bottle_item, bom_no, target_warehouse, good_qty, scrap_qty)
        VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'INT-BTL-0.5L', 'BOM-INT-BTL-0.5L-001', 'Stores - W', 6400, 50)
    """, ("DEMO-BM-TODAY", now_str, now_str, company, current_date))

    # Today's Filling Entry (yields FPY = 5800 / (5800 + 20) = 99.66%)
    frappe.db.sql("""
        INSERT INTO `tabFilling Entry`
        (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, finished_good_item, bom_no, fg_warehouse, good_qty, scrap_qty)
        VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 'FG-WATER-0.5L-12', 'BOM-FG-WATER-0.5L-12-001', 'Finished Goods - W', 5800, 20)
    """, ("DEMO-FE-TODAY", now_str, now_str, company, current_date))

    # Today's Bottle Movement
    frappe.db.sql("""
        INSERT INTO `tabCustomer Bottle Ledger`
        (name, creation, modified, modified_by, owner, docstatus, idx, company, customer, posting_date, voucher_type, voucher_no, full_bottles_delivered, empty_bottles_received)
        VALUES (99999, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, 'VIP Office B', %s, 'Sales Invoice', 'DEMO-SI-TODAY', 85, 75)
    """, (now_str, now_str, company, current_date))

    # Today's Delivery Note
    frappe.db.sql("""
        INSERT INTO `tabDelivery Note`
        (name, creation, modified, modified_by, owner, docstatus, idx, company, posting_date, total_qty)
        VALUES (%s, %s, %s, 'Administrator', 'Administrator', 1, 0, %s, %s, 320)
    """, ("DEMO-DN-TODAY", now_str, now_str, company, current_date))

    frappe.db.commit()
    print("=== [6/6] Demo Data Seeded & Committed Successfully! ===")

if __name__ == "__main__":
    seed_demo_data()
