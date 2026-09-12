import frappe

def fix_aggregate_fields():
    mapping = {
        "Blow Molding Quality (Good vs Scrap)": "good_qty",
        "Bottle Ledger Movement": "full_bottles_delivered",
        "Cash & Bank Balances": "debit",
        "Daily Filling Output": "good_qty",
        "Daily Water Purification Trend": "good_qty",
        "Delivery OTIF Trend": "total",
        "Monthly Indirect Expenses": "debit",
        "Monthly Production by Product": "good_qty",
        "Monthly Sales by Product": "qty",
        "Payments vs Receivables": "paid_amount"
    }

    for chart_name, field in mapping.items():
        if frappe.db.exists("Dashboard Chart", chart_name):
            doc = frappe.get_doc("Dashboard Chart", chart_name)
            doc.aggregate_function_based_on = field
            doc.chart_type = "Sum"
            doc.save(ignore_permissions=True)

    frappe.db.commit()
    print("Aggregate fields fixed.")

fix_aggregate_fields()
