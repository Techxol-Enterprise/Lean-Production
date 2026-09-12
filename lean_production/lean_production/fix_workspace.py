import frappe
import json

def fix_workspace():
    workspace = frappe.get_doc("Workspace", "Lean Production")
    
    # Base shortcuts that were originally there
    base_content = [
        {"id": "header_production", "type": "header", "data": {"text": "<span class=\"h4\"><b>Manufacturing</b></span>", "col": 12}},
        {"id": "shortcut_water", "type": "shortcut", "data": {"shortcut_name": "Water Purification", "col": 4}},
        {"id": "shortcut_blow", "type": "shortcut", "data": {"shortcut_name": "Blow Molding", "col": 4}},
        {"id": "shortcut_fill", "type": "shortcut", "data": {"shortcut_name": "Filling", "col": 4}},
        {"id": "header_bottles", "type": "header", "data": {"text": "<span class=\"h4\"><b>Bottle Tracking</b></span>", "col": 12}},
        {"id": "shortcut_ledger", "type": "shortcut", "data": {"shortcut_name": "Customer Bottle Ledger", "col": 4}},
        {"id": "shortcut_report", "type": "shortcut", "data": {"shortcut_name": "Bottles with Customers", "col": 4}}
    ]
    
    # New Dashboard Blocks
    new_blocks = [
        {"id": frappe.generate_hash(length=8), "type": "header", "data": {"text": "<span class=\"h4\"><b>Pulse (Today)</b></span>", "col": 12}},
        {"id": frappe.generate_hash(length=8), "type": "number_card", "data": {"number_card_name": "Total Water Purified Today", "col": 4}},
        {"id": frappe.generate_hash(length=8), "type": "number_card", "data": {"number_card_name": "Bottles Molded Today", "col": 4}},
        {"id": frappe.generate_hash(length=8), "type": "number_card", "data": {"number_card_name": "Finished Goods Filled Today", "col": 4}},
        
        {"id": frappe.generate_hash(length=8), "type": "header", "data": {"text": "<span class=\"h4\"><b>Lean Metrics</b></span>", "col": 12}},
        {"id": frappe.generate_hash(length=8), "type": "number_card", "data": {"number_card_name": "First Pass Yield (FPY) %", "col": 6}},
        {"id": frappe.generate_hash(length=8), "type": "number_card", "data": {"number_card_name": "Overall Equipment Effectiveness (OEE)", "col": 6}},
        
        {"id": frappe.generate_hash(length=8), "type": "header", "data": {"text": "<span class=\"h4\"><b>Production Trends</b></span>", "col": 12}},
        {"id": frappe.generate_hash(length=8), "type": "chart", "data": {"chart_name": "Daily Water Purification Trend", "col": 12}},
        {"id": frappe.generate_hash(length=8), "type": "chart", "data": {"chart_name": "Blow Molding Quality (Good vs Scrap)", "col": 12}},
        {"id": frappe.generate_hash(length=8), "type": "chart", "data": {"chart_name": "Daily Filling Output", "col": 12}},
        
        {"id": frappe.generate_hash(length=8), "type": "header", "data": {"text": "<span class=\"h4\"><b>Financial & Logistics</b></span>", "col": 12}},
        {"id": frappe.generate_hash(length=8), "type": "chart", "data": {"chart_name": "Payments vs Receivables", "col": 6}},
        {"id": frappe.generate_hash(length=8), "type": "chart", "data": {"chart_name": "Cash & Bank Balances", "col": 6}},
        {"id": frappe.generate_hash(length=8), "type": "chart", "data": {"chart_name": "Monthly Sales by Product", "col": 6}},
        {"id": frappe.generate_hash(length=8), "type": "chart", "data": {"chart_name": "Monthly Indirect Expenses", "col": 6}},
        {"id": frappe.generate_hash(length=8), "type": "chart", "data": {"chart_name": "Delivery OTIF Trend", "col": 12}}
    ]
    
    workspace.content = json.dumps(new_blocks + base_content)
    workspace.save(ignore_permissions=True)
    frappe.db.commit()
    print("Workspace cleaned and fixed.")

fix_workspace()
