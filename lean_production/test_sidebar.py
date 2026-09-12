import frappe
from frappe.desk.desktop import get_workspaces

def run():
    workspaces = get_workspaces()
    print("Type of workspaces:", type(workspaces))
    
    found = False
    pages = workspaces.get("pages") if isinstance(workspaces, dict) else workspaces
    for page in pages:
        if page.get("name") == 'Lean Production':
            found = True
            print(f"FOUND Lean Production! Icon: {page.get('icon')}, parent: {page.get('parent_page')}")
            break
            
    if not found:
        print("NOT FOUND in sidebar items!")
        print([p.get('name') for p in pages])
