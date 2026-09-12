import frappe
import json

def fix_all():
    # 1. Number Cards: Change 'creation' to 'posting_date' in filters_json, and clear currency
    number_cards = frappe.get_all("Number Card", filters={"module": "Lean Production"}, fields=["name", "filters_json"])
    for nc in number_cards:
        doc = frappe.get_doc("Number Card", nc.name)
        doc.currency = None
        if doc.filters_json:
            try:
                filters = json.loads(doc.filters_json)
                for f in filters:
                    if len(f) == 4 and f[1] == "creation":
                        f[1] = "posting_date"
                doc.filters_json = json.dumps(filters)
            except Exception:
                pass
        doc.save(ignore_permissions=True)

    # 2. Dashboard Charts: clear currency
    charts = frappe.get_all("Dashboard Chart", filters={"module": "Lean Production"})
    for chart in charts:
        doc = frappe.get_doc("Dashboard Chart", chart.name)
        # We might want to keep currency for Payments and Cash, but let's clear it from quantities
        if doc.value_based_on in ["good_qty", "qty", "scrap_qty", "full_bottles_delivered", "empty_bottles_received"]:
            doc.currency = None
        else:
            # For financial charts, keep it or clear it? The user complained "some of them are quantities ... in rs".
            # It's better to clear it for the quantity ones, and leave it for the amount ones.
            pass
        doc.save(ignore_permissions=True)

    frappe.db.commit()
    print("Formatting and filters fixed.")

fix_all()
