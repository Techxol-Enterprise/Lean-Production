import frappe

def create_or_update_group(group_name, parent_group="All Item Groups", is_group=1):
    if frappe.db.exists("Item Group", group_name):
        doc = frappe.get_doc("Item Group", group_name)
        doc.is_group = is_group
        doc.parent_item_group = parent_group
        doc.save()
    else:
        doc = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": group_name,
            "parent_item_group": parent_group,
            "is_group": is_group
        })
        doc.insert()

frappe.init(site="Wateena", sites_path="sites")
frappe.connect()

# 1. Ensure the 4 main group nodes exist
create_or_update_group("Raw Material", is_group=1)
create_or_update_group("Mineral Water", is_group=1)
create_or_update_group("Semi Finished Goods", is_group=1)
create_or_update_group("Finished Goods", is_group=1)

# 2. Re-assign existing groups to the new parents
mapping = {
    "Chemicals & Minerals": "Raw Material",
    "Packaging Materials": "Raw Material",
    "Resins & Preforms": "Raw Material",
    "Raw Water": "Raw Material",
    "Bulk Purified Water": "Mineral Water",
    "Empty Bottles": "Semi Finished Goods"
}

for child, parent in mapping.items():
    if frappe.db.exists("Item Group", child):
        doc = frappe.get_doc("Item Group", child)
        doc.parent_item_group = parent
        doc.save()

# Update the Old Items that were directly in 'All Item Groups'
# For example the finished goods might just be in "Finished Goods" group directly

frappe.db.commit()
print("Success")
