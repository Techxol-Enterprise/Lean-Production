import frappe

def run():
    # 1. Create the Workspace Sidebar
    if not frappe.db.exists("Workspace Sidebar", "Lean Production"):
        sidebar = frappe.get_doc({
            "doctype": "Workspace Sidebar",
            "name": "Lean Production",
            "title": "Lean Production",
            "header_icon": "droplet",
            "module": "Lean Production",
            "app": "lean_production",
            "standard": 1,
            "items": [
                {
                    "label": "Home",
                    "type": "Link",
                    "link_type": "Workspace",
                    "link_to": "Lean Production",
                    "icon": "home"
                }
            ]
        })
        sidebar.insert(ignore_permissions=True)
        print("Workspace Sidebar created!")
    
    # 2. Fix the Desktop Icon
    if frappe.db.exists("Desktop Icon", "Lean Production"):
        doc = frappe.get_doc("Desktop Icon", "Lean Production")
        doc.link_type = "Workspace Sidebar"
        doc.link_to = "Lean Production"
        doc.icon = "droplet"
        doc.save(ignore_permissions=True)
        print("Desktop Icon updated!")
    frappe.db.commit()

