import frappe

def generate():
    groups = frappe.get_all("Item Group", fields=["name", "parent_item_group", "is_group"])
    items = frappe.get_all("Item", fields=["name", "item_name", "item_group"])

    tree = {}
    for g in groups:
        tree[g.name] = {"is_group": g.is_group, "parent": g.parent_item_group, "children": [], "items": []}
        
    for g in groups:
        parent = g.parent_item_group
        if parent and parent in tree:
            tree[parent]["children"].append(g.name)

    for i in items:
        ig = i.item_group
        if ig in tree:
            tree[ig]["items"].append(f"{i.name} ({i.item_name})")

    def print_tree(node, level=0):
        indent = "  " * level
        out = f"{indent}- **{node}**\n"
        
        for item in sorted(tree[node]["items"]):
            out += f"{indent}  - [Item] {item}\n"
            
        for child in sorted(tree[node]["children"]):
            out += print_tree(child, level + 1)
            
        return out

    report = "# Item Group & Item Hierarchy\n\n"
    
    roots = [g.name for g in groups if not g.parent_item_group]
    for r in sorted(roots):
        report += print_tree(r)
        
    with open("item_hierarchy.md", "w") as f:
        f.write(report)
