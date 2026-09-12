import frappe
from frappe.desk.doctype.dashboard_chart.dashboard_chart import get as get_chart_data

def inspect_all():
    print("=== CHECKING TABLE ROW COUNTS ===")
    tables = [
        "Water Purification Entry",
        "Blow Molding Entry",
        "Filling Entry",
        "Customer Bottle Ledger",
        "Lean Material Consumption",
        "Sales Invoice",
        "Delivery Note",
        "Stock Entry",
        "GL Entry"
    ]
    for t in tables:
        count = frappe.db.count(t)
        print(f"Table '{t}': {count} rows")

    print("\n=== CHECKING CHART OUTPUTS ===")
    charts = [
        "Daily Water Purification Trend",
        "Blow Molding Quality (Good vs Scrap)",
        "Daily Filling Output",
        "Monthly Production by Product",
        "Purification QC Status",
        "Downtime Root Cause Analysis",
        "Bottle Ledger Movement",
        "Monthly Sales by Product",
        "Cash & Bank Balances",
        "Monthly Indirect Expenses",
        "Payments vs Receivables",
        "Delivery OTIF Trend"
    ]
    for c in charts:
        data = get_chart_data(chart_name=c)
        datasets = data.get("datasets", [])
        values = []
        if datasets:
            values = [v for v in datasets[0].get("values", []) if v != 0]
        print(f"Chart '{c}': nonzero count={len(values)}, values={values[:5]}")

if __name__ == "__main__":
    inspect_all()
