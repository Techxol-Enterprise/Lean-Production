import frappe

LEAN_MANAGER_ROLE = "Lean Production Manager"

DOCTYPES_FULL_ACCESS = [
    "Water Purification Entry",
    "Blow Molding Entry",
    "Filling Entry"
]

DOCTYPES_READ_ACCESS = [
    "Customer Bottle Ledger"
]


def setup_lean_roles():
    """
    Provisions the 'Lean Production Manager' role, configures permissions across
    all Lean Production DocTypes, pages, reports, and assigns the role to Administrator.
    """
    # 1. Create or ensure Role exists
    if not frappe.db.exists("Role", LEAN_MANAGER_ROLE):
        doc = frappe.new_doc("Role")
        doc.role_name = LEAN_MANAGER_ROLE
        doc.desk_access = 1
        doc.is_custom = 0
        doc.insert(ignore_permissions=True)
        frappe.logger("lean_production").info(f"Created Role: {LEAN_MANAGER_ROLE}")
        print(f"Created Role: {LEAN_MANAGER_ROLE}")
    else:
        role_doc = frappe.get_doc("Role", LEAN_MANAGER_ROLE)
        if not role_doc.desk_access:
            role_doc.desk_access = 1
            role_doc.save(ignore_permissions=True)

    # 2. Grant full permissions on transactional MES DocTypes
    for dt in DOCTYPES_FULL_ACCESS:
        grant_permission(dt, LEAN_MANAGER_ROLE, {
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1,
            "report": 1,
            "export": 1,
            "print": 1,
            "email": 1,
            "share": 1
        })

    # 3. Grant read/reporting permissions on Ledger
    for dt in DOCTYPES_READ_ACCESS:
        grant_permission(dt, LEAN_MANAGER_ROLE, {
            "read": 1,
            "write": 0,
            "create": 0,
            "delete": 0,
            "submit": 0,
            "cancel": 0,
            "amend": 0,
            "report": 1,
            "export": 1,
            "print": 1,
            "email": 1,
            "share": 1
        })

    # 4. Assign role to Administrator user for immediate access
    if frappe.db.exists("User", "Administrator"):
        admin = frappe.get_doc("User", "Administrator")
        has_role = any(r.role == LEAN_MANAGER_ROLE for r in admin.roles)
        if not has_role:
            admin.append("roles", {"role": LEAN_MANAGER_ROLE})
            admin.save(ignore_permissions=True)
            print(f"Assigned {LEAN_MANAGER_ROLE} to Administrator")

    frappe.db.commit()
    print(f"Successfully configured all permissions for {LEAN_MANAGER_ROLE}.")


def grant_permission(doctype, role, perm_dict):
    """
    Idempotently ensures a DocPerm entry exists for (doctype, role) with specified permissions.
    """
    if not frappe.db.exists("DocType", doctype):
        return

    docperms = frappe.get_all(
        "Custom DocPerm",
        filters={"parent": doctype, "role": role},
        fields=["name"]
    )

    if not docperms:
        # Also check standard DocPerm
        docperms = frappe.get_all(
            "DocPerm",
            filters={"parent": doctype, "role": role},
            fields=["name"]
        )

    if docperms:
        perm_name = docperms[0].name
        # Update existing permission
        frappe.db.set_value("DocPerm", perm_name, perm_dict)
    else:
        # Append to DocType permissions
        dt_doc = frappe.get_doc("DocType", doctype)
        perm_entry = {"role": role, "permlevel": 0}
        perm_entry.update(perm_dict)
        dt_doc.append("permissions", perm_entry)
        dt_doc.save(ignore_permissions=True)
