import frappe
import json

def remove_shortcuts():
    workspace = frappe.get_doc("Workspace", "Lean Production")
    
    # 1. Clear the shortcuts child table
    workspace.set("shortcuts", [])
    
    # 2. Parse current content and remove shortcut blocks and specific headers
    if workspace.content:
        content = json.loads(workspace.content)
        filtered_content = []
        for block in content:
            if block.get("type") == "shortcut":
                continue
            if block.get("id") in ["header_production", "header_bottles"]:
                continue
            filtered_content.append(block)
            
        workspace.content = json.dumps(filtered_content)
        
    workspace.save(ignore_permissions=True)
    frappe.db.commit()
    print("Shortcuts removed successfully.")

remove_shortcuts()
