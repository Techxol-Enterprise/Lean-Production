import frappe
import json

def fix_workspace():
    workspace = frappe.get_doc("Workspace", "Lean Production")
    
    # 1. Clear existing charts and number_cards child tables
    workspace.set("charts", [])
    workspace.set("number_cards", [])
    
    # 2. Add charts to child table
    charts = [
        "Daily Water Purification Trend",
        "Blow Molding Quality (Good vs Scrap)",
        "Daily Filling Output",
        "Payments vs Receivables",
        "Cash & Bank Balances",
        "Monthly Sales by Product",
        "Monthly Indirect Expenses",
        "Delivery OTIF Trend"
    ]
    for chart in charts:
        workspace.append("charts", {"chart_name": chart})
        
    # 3. Add number cards to child table
    number_cards = [
        "Total Water Purified Today",
        "Bottles Molded Today",
        "Finished Goods Filled Today",
        "First Pass Yield (FPY) %",
        "Overall Equipment Effectiveness (OEE)"
    ]
    for card in number_cards:
        workspace.append("number_cards", {"number_card_name": card})

    # The content is already correctly set, but we will save to persist the child tables.
    workspace.save(ignore_permissions=True)
    frappe.db.commit()
    print("Workspace child tables populated and fixed.")

fix_workspace()
