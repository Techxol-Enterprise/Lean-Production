import frappe
def fix_currency():
    for nc in frappe.get_all("Number Card", filters={"module":"Lean Production"}):
        frappe.db.set_value("Number Card", nc.name, "currency", None)
    frappe.db.commit()
    print("Currency cleared.")
fix_currency()
