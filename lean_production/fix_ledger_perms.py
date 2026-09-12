import frappe

def run():
    doc = frappe.get_doc("DocType", "Customer Bottle Ledger")
    
    modified = False
    for perm in doc.permissions:
        if perm.role == "System Manager":
            perm.create = 0
            perm.write = 0
            perm.delete = 0
            modified = True
            
    if modified:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Permissions locked down to Read-Only")
    else:
        print("Role not found")
