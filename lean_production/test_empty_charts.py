import frappe
from frappe.desk.doctype.dashboard_chart.dashboard_chart import get as get_chart_data

def test_empty_charts():
    charts = frappe.get_all("Dashboard Chart", filters={"module": "Lean Production"}, pluck="name")
    for c in charts:
        try:
            res = get_chart_data(chart_name=c)
            print(f"Chart '{c}': returned type={type(res).__name__}, content={res}")
        except Exception as e:
            print(f"Chart '{c}': EXCEPTION {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_empty_charts()
