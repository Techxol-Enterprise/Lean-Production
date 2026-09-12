import frappe
import json

def remove_shortcuts():
    ws = frappe.get_doc("Workspace", "Lean Production")
    
    # Clear shortcuts child table
    ws.set("shortcuts", [])
    
    # Parse content blocks
    content_blocks = json.loads(ws.content)
    
    # Remove shortcut headers and shortcut widgets
    filtered_blocks = []
    remove_ids = {
        "hdr_mfg_shortcuts", "sc_water", "sc_blow", "sc_fill",
        "hdr_bottle_shortcuts", "sc_ledger", "sc_report"
    }
    
    for block in content_blocks:
        b_id = block.get("id")
        b_type = block.get("type")
        b_text = block.get("data", {}).get("text", "")
        
        if b_id in remove_ids:
            continue
        if b_type == "shortcut":
            continue
        if "Manufacturing" in b_text or "Bottle Tracking" in b_text:
            continue
            
        filtered_blocks.append(block)
        
    ws.content = json.dumps(filtered_blocks)
    ws.save(ignore_permissions=True)
    frappe.db.commit()
    
    # Also update the file on disk to persist standard workspace definition
    import os
    filepath = "/Users/pirated/Frappe/bench15dev/frappe-bench/apps/lean_production/lean_production/lean_production/workspace/lean_production/lean_production.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        data["shortcuts"] = []
        data["content"] = json.dumps(filtered_blocks)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=1)
            
    print(f"Successfully removed shortcuts section. Remaining blocks: {len(filtered_blocks)}")

if __name__ == "__main__":
    remove_shortcuts()
