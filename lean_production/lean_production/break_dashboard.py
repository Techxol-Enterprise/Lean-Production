import frappe

def break_it():
    import json
    
    # 1. Delete all standard charts and cards
    frappe.db.sql("DELETE FROM `tabDashboard Chart` WHERE module='Lean Production'")
    frappe.db.sql("DELETE FROM `tabNumber Card` WHERE module='Lean Production'")
    
    # 2. Run original build_dashboard
    from lean_production.lean_production.build_dashboard import create_dashboard_charts, create_number_cards
    
    create_number_cards()
    create_dashboard_charts()
    
    # 3. Purposely inject the duplicate blocks into workspace
    ws = frappe.get_doc("Workspace", "Lean Production")
    ws.charts = []
    ws.number_cards = []
    ws.shortcuts = []
    
    # original duplicate logic
    content = [
        {"type": "header", "data": {"text": "Production & Quality Trends", "level": 2}},
        {"type": "chart", "data": {"chart_name": "Daily Water Purification Trend"}},
        {"type": "chart", "data": {"chart_name": "Blow Molding Quality (Good vs Scrap)"}},
        {"type": "chart", "data": {"chart_name": "Daily Filling Output"}},
        {"type": "chart", "data": {"chart_name": "Bottle Ledger Movement"}},
        {"type": "chart", "data": {"chart_name": "Downtime Root Cause Analysis"}},
        {"type": "chart", "data": {"chart_name": "Delivery OTIF Trend"}},
        {"type": "header", "data": {"text": "Financial & Sales Performance", "level": 2}},
        {"type": "chart", "data": {"chart_name": "Payments vs Receivables"}},
        {"type": "chart", "data": {"chart_name": "Cash & Bank Balances"}},
        {"type": "chart", "data": {"chart_name": "Monthly Sales by Product"}},
        {"type": "chart", "data": {"chart_name": "Monthly Indirect Expenses"}},
        {"type": "header", "data": {"text": "Operations Live Pulse", "level": 2}},
        {"type": "number_cards", "data": {"number_card_name": "Total Water Purified Today"}},
        {"type": "number_cards", "data": {"number_card_name": "Bottles Molded Today"}},
        {"type": "number_cards", "data": {"number_card_name": "Finished Goods Filled Today"}},
        {"type": "number_cards", "data": {"number_card_name": "First Pass Yield (FPY) %"}},
        {"type": "number_cards", "data": {"number_card_name": "Overall Equipment Effectiveness (OEE)"}}
    ]
    
    # duplicate it 3 times just like original
    ws.content = json.dumps(content + content + content)
    ws.save(ignore_permissions=True)
    frappe.db.commit()
    print("Dashboard successfully broken to original state!")

break_it()
