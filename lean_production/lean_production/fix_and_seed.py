import frappe
from frappe.utils import nowdate, add_days

def fix_and_seed():
    # 1. Fix Invalid Filters on GL Entry Charts
    try:
        chart1 = frappe.get_doc("Dashboard Chart", "Monthly Indirect Expenses")
        chart1.filters_json = "[]"
        chart1.save(ignore_permissions=True)
        
        chart2 = frappe.get_doc("Dashboard Chart", "Cash & Bank Balances")
        chart2.filters_json = "[]"
        chart2.save(ignore_permissions=True)
        
        frappe.db.commit()
        print("Fixed invalid filters.")
    except Exception as e:
        print("Error fixing charts:", e)

    # 2. Seed Data
    try:
        # We need a company
        company = frappe.db.get_value("Company", {}, "name")
        if not company:
            company = "Test Company"
            
        today = nowdate()
        
        # We will insert ignoring links and mandatory fields to bypass complex validations for testing
        
        # Water Purification
        if not frappe.db.exists("Water Purification Entry", {"posting_date": today}):
            doc = frappe.new_doc("Water Purification Entry")
            doc.company = company
            doc.posting_date = today
            doc.good_qty = 5000
            doc.scrap_qty = 100
            doc.flags.ignore_links = True
            doc.flags.ignore_mandatory = True
            doc.insert()
            try:
                doc.submit()
            except AttributeError:
                pass

        # Blow Molding
        if not frappe.db.exists("Blow Molding Entry", {"posting_date": today}):
            doc = frappe.new_doc("Blow Molding Entry")
            doc.company = company
            doc.posting_date = today
            doc.good_qty = 4000
            doc.scrap_qty = 50
            doc.flags.ignore_links = True
            doc.flags.ignore_mandatory = True
            doc.insert()
            try:
                doc.submit()
            except AttributeError:
                pass

        # Filling
        if not frappe.db.exists("Filling Entry", {"posting_date": today}):
            doc = frappe.new_doc("Filling Entry")
            doc.company = company
            doc.posting_date = today
            doc.good_qty = 3500
            doc.scrap_qty = 15
            doc.flags.ignore_links = True
            doc.flags.ignore_mandatory = True
            doc.insert()
            try:
                doc.submit()
            except AttributeError:
                pass
                
        frappe.db.commit()
        print("Test data seeded successfully.")
    except Exception as e:
        print("Error seeding data:", e)

fix_and_seed()
