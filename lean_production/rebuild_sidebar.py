import frappe

def run():
    sidebar = frappe.get_doc("Workspace Sidebar", "Lean Production")
    
    # Clear existing items
    sidebar.set("items", [])
    
    # 1. Dashboard (Points to the workspace we built)
    sidebar.append("items", {
        "label": "Dashboard",
        "type": "Link",
        "link_type": "Workspace",
        "link_to": "Lean Production",
        "icon": "chart",
        "child": 0,
        "indent": 0
    })
    
    # 2. Manufacturing Entries Section
    sidebar.append("items", {
        "label": "Manufacturing",
        "type": "Section Break",
        "icon": "factory",
        "child": 0,
        "indent": 1
    })
    sidebar.append("items", {
        "label": "Water Purification Entry",
        "type": "Link",
        "link_type": "DocType",
        "link_to": "Water Purification Entry",
        "child": 1,
        "indent": 0
    })
    sidebar.append("items", {
        "label": "Blow Molding Entry",
        "type": "Link",
        "link_type": "DocType",
        "link_to": "Blow Molding Entry",
        "child": 1,
        "indent": 0
    })
    sidebar.append("items", {
        "label": "Filling Entry",
        "type": "Link",
        "link_type": "DocType",
        "link_to": "Filling Entry",
        "child": 1,
        "indent": 0
    })
    
    # 3. Bottle Tracking Section
    sidebar.append("items", {
        "label": "Bottle Tracking",
        "type": "Section Break",
        "icon": "box",
        "child": 0,
        "indent": 1
    })
    sidebar.append("items", {
        "label": "Customer Bottle Ledger",
        "type": "Link",
        "link_type": "DocType",
        "link_to": "Customer Bottle Ledger",
        "child": 1,
        "indent": 0
    })
    
    # 4. Reports Section
    sidebar.append("items", {
        "label": "Reports",
        "type": "Section Break",
        "icon": "pie-chart",
        "child": 0,
        "indent": 1
    })
    sidebar.append("items", {
        "label": "Bottles with Customers",
        "type": "Link",
        "link_type": "Report",
        "link_to": "Bottles with Customers",
        "child": 1,
        "indent": 0
    })
    
    # 5. Help Section
    sidebar.append("items", {
        "label": "Help & Manuals",
        "type": "Section Break",
        "icon": "book-open",
        "child": 0,
        "indent": 1
    })
    sidebar.append("items", {
        "label": "User Manual",
        "type": "Link",
        "link_type": "Page",
        "link_to": "lean-production-manu",
        "child": 1,
        "indent": 0
    })
    
    sidebar.save(ignore_permissions=True)
    frappe.db.commit()
    print("Sidebar rebuilt!")
