import frappe
def clear_ws():
    ws = frappe.get_doc("Workspace", "Lean Production")
    ws.charts = []
    ws.number_cards = []
    ws.shortcuts = []
    ws.content = "[]"
    ws.save(ignore_permissions=True)
    frappe.db.commit()
