import frappe

def run():
    if not frappe.db.exists("Desktop Icon", "Lean Production"):
        doc = frappe.get_doc({
            "doctype": "Desktop Icon",
            "name": "Lean Production",
            "label": "Lean Production",
            "icon_type": "Link",
            "link_type": "Workspace Sidebar",
            "link_to": "Lean Production",
            "icon": "droplet",
            "app": "lean_production",
            "standard": 1,
            "hidden": 0,
        })
        doc.insert(ignore_permissions=True)
        print("Desktop Icon created!")
    else:
        print("Already exists")
    frappe.db.commit()
