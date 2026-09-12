import frappe

def fix_filters():
    charts = ["Monthly Indirect Expenses", "Cash & Bank Balances"]
    for chart in charts:
        if frappe.db.exists("Dashboard Chart", chart):
            doc = frappe.get_doc("Dashboard Chart", chart)
            doc.filters_json = "[]"
            doc.save(ignore_permissions=True)
            print(f"Fixed filters for {chart}")
            
    frappe.db.commit()

fix_filters()
