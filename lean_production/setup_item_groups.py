import frappe
from frappe.utils.nestedset import rebuild_tree

# Declarative Item Group Hierarchy for Lean Production
LEAN_ITEM_GROUPS = [
    # 1. Main Category Groups (is_group = 1)
    {"name": "Raw Material", "parent": "All Item Groups", "is_group": 1},
    {"name": "Mineral Water", "parent": "All Item Groups", "is_group": 1},
    {"name": "Semi Finished Goods", "parent": "All Item Groups", "is_group": 1},
    {"name": "Finished Goods", "parent": "All Item Groups", "is_group": 1},

    # 2. Subgroups / Leaf Nodes (is_group = 0)
    {"name": "Chemicals & Minerals", "parent": "Raw Material", "is_group": 0},
    {"name": "Packaging Materials", "parent": "Raw Material", "is_group": 0},
    {"name": "Resins & Preforms", "parent": "Raw Material", "is_group": 0},
    {"name": "Raw Water", "parent": "Raw Material", "is_group": 0},
    {"name": "Bulk Purified Water", "parent": "Mineral Water", "is_group": 0},
    {"name": "Empty Bottles", "parent": "Semi Finished Goods", "is_group": 0},
]


def setup_lean_item_groups():
    """
    Idempotently provisions and aligns the Item Group tree hierarchy required
    by Lean Production DocTypes (Water Purification, Blow Molding, Filling Lines).
    """
    root_group = "All Item Groups"
    if not frappe.db.exists("Item Group", root_group):
        # Fallback if standard root is missing or named differently
        existing_roots = frappe.get_all("Item Group", filters={"is_group": 1, "parent_item_group": ""}, pluck="name")
        if existing_roots:
            root_group = existing_roots[0]

    updated = False

    # Step 1: Create or update parent group containers first
    parents = [g for g in LEAN_ITEM_GROUPS if g["is_group"] == 1]
    children = [g for g in LEAN_ITEM_GROUPS if g["is_group"] == 0]

    for g in parents + children:
        name = g["name"]
        target_parent = root_group if g["parent"] == "All Item Groups" else g["parent"]
        target_is_group = g["is_group"]

        if not frappe.db.exists("Item Group", name):
            doc = frappe.new_doc("Item Group")
            doc.item_group_name = name
            doc.parent_item_group = target_parent
            doc.is_group = target_is_group
            doc.insert(ignore_permissions=True)
            updated = True
            frappe.logger("lean_production").info(f"Created Item Group: {name}")
        else:
            doc = frappe.get_doc("Item Group", name)
            changes = False
            if doc.parent_item_group != target_parent:
                doc.parent_item_group = target_parent
                changes = True
            if doc.is_group != target_is_group:
                # Only promote to group, never demote if it has children
                has_children = frappe.db.count("Item Group", {"parent_item_group": name}) > 0
                if target_is_group == 1 or not has_children:
                    doc.is_group = target_is_group
                    changes = True

            if changes:
                doc.save(ignore_permissions=True)
                updated = True
                frappe.logger("lean_production").info(f"Updated Item Group: {name}")

    # Step 2: Rebuild Nested Set Tree to ensure lft and rgt indexes are valid
    rebuild_tree("Item Group")
    frappe.db.commit()
    print("Lean Production Item Groups successfully provisioned and tree rebuilt.")
