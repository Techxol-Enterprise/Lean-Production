import frappe

def run():
    sidebar = frappe.get_doc("Workspace Sidebar", "Lean Production")
    for item in sidebar.items:
        if item.icon == "pie-chart":
            item.icon = "chart-pie"
    sidebar.save(ignore_permissions=True)
    frappe.db.commit()
    print("Icon fixed")
