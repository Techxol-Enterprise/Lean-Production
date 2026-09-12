import frappe

def run():
    doc = frappe.get_doc("DocType", "Customer Bottle Ledger")
    
    # Check if System Manager is already there
    has_perm = False
    for perm in doc.permissions:
        if perm.role == "System Manager":
            has_perm = True
            break
            
    if not has_perm:
        doc.append("permissions", {
            "role": "System Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "export": 1,
            "report": 1,
            "share": 1
        })
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Permissions added to Customer Bottle Ledger")
    else:
        print("Already has perms")
