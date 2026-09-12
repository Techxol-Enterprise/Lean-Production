import frappe
import json
import os

def apply_option_a():
    print("=== [1/3] Updating Number Card Labels & Colors (Option A) ===")
    card_updates = {
        "Total Water Purified Today": {
            "label": "Water Purified [Liters]",
            "color": "#0284c7",
        },
        "Bottles Molded Today": {
            "label": "Bottles Molded [Units]",
            "color": "#2563eb",
        },
        "Finished Goods Filled Today": {
            "label": "Finished Goods [Cartons]",
            "color": "#4f46e5",
        },
        "Water Purified Scrap Today": {
            "label": "Water Loss [Liters]",
            "color": "#f59e0b",
        },
        "Bottle Scrap Today": {
            "label": "Molding Defects [Bottles]",
            "color": "#ef4444",
        },
        "Finished Goods Current Stock": {
            "label": "FG Stock [Cartons]",
            "color": "#10b981",
        },
        "Available Raw Material": {
            "label": "Raw Materials [Units]",
            "color": "#0d9488",
        },
        "19L Bottles Delivered (MTD)": {
            "label": "19L Dispatched [Bottles]",
            "color": "#7c3aed",
        },
        "19L Bottles Received (MTD)": {
            "label": "19L Returned [Bottles]",
            "color": "#9333ea",
        },
        "First Pass Yield (FPY) %": {
            "label": "First Pass Yield (FPY) %",
            "color": "#059669",
        },
        "Overall Equipment Effectiveness (OEE)": {
            "label": "Overall Equipment Effectiveness (OEE)",
            "color": "#0284c7",
        },
    }

    for name, cfg in card_updates.items():
        if frappe.db.exists("Number Card", name):
            doc = frappe.get_doc("Number Card", name)
            doc.label = cfg["label"]
            doc.color = cfg["color"]
            doc.save(ignore_permissions=True)
            print(f"  [OK] Number Card '{name}' -> Label: '{cfg['label']}', Color: '{cfg['color']}'")

    print("\n=== [2/3] Updating Workspace Layout with 3 Tiered Sections ===")
    ws = frappe.get_doc("Workspace", "Lean Production")

    content_blocks = [
        # Tier 1: Stage Throughput
        {"id": "hdr_throughput", "type": "header", "data": {"text": "<span class=\"h4\"><b>Daily Production Throughput (Today)</b></span>", "col": 12}},
        {"id": "nc_water_today", "type": "number_card", "data": {"number_card_name": "Total Water Purified Today", "col": 4}},
        {"id": "nc_bottles_today", "type": "number_card", "data": {"number_card_name": "Bottles Molded Today", "col": 4}},
        {"id": "nc_fg_today", "type": "number_card", "data": {"number_card_name": "Finished Goods Filled Today", "col": 4}},

        # Tier 2: Quality Loss & Finished Stock
        {"id": "hdr_quality_stock", "type": "header", "data": {"text": "<span class=\"h4\"><b>Quality Loss & Finished Stock</b></span>", "col": 12}},
        {"id": "nc_water_scrap", "type": "number_card", "data": {"number_card_name": "Water Purified Scrap Today", "col": 4}},
        {"id": "nc_bottle_scrap", "type": "number_card", "data": {"number_card_name": "Bottle Scrap Today", "col": 4}},
        {"id": "nc_fg_stock", "type": "number_card", "data": {"number_card_name": "Finished Goods Current Stock", "col": 4}},

        # Tier 3: Raw Materials & Fleet Loop
        {"id": "hdr_raw_fleet", "type": "header", "data": {"text": "<span class=\"h4\"><b>Raw Material Buffer & 19L Fleet Assets</b></span>", "col": 12}},
        {"id": "nc_raw_material", "type": "number_card", "data": {"number_card_name": "Available Raw Material", "col": 4}},
        {"id": "nc_19l_delivered", "type": "number_card", "data": {"number_card_name": "19L Bottles Delivered (MTD)", "col": 4}},
        {"id": "nc_19l_received", "type": "number_card", "data": {"number_card_name": "19L Bottles Received (MTD)", "col": 4}},

        # Tier 4: Lean Performance Metrics
        {"id": "hdr_lean", "type": "header", "data": {"text": "<span class=\"h4\"><b>Lean Performance Metrics</b></span>", "col": 12}},
        {"id": "nc_fpy", "type": "number_card", "data": {"number_card_name": "First Pass Yield (FPY) %", "col": 6}},
        {"id": "nc_oee", "type": "number_card", "data": {"number_card_name": "Overall Equipment Effectiveness (OEE)", "col": 6}},

        # Tier 5: Production Trends
        {"id": "hdr_trends", "type": "header", "data": {"text": "<span class=\"h4\"><b>Production Trends</b></span>", "col": 12}},
        {"id": "ch_water_trend", "type": "chart", "data": {"chart_name": "Daily Water Purification Trend", "col": 12}},
        {"id": "ch_blow_quality", "type": "chart", "data": {"chart_name": "Blow Molding Quality (Good vs Scrap)", "col": 12}},
        {"id": "ch_daily_filling", "type": "chart", "data": {"chart_name": "Daily Filling Output", "col": 12}},
        {"id": "ch_monthly_prod", "type": "chart", "data": {"chart_name": "Monthly Production by Product", "col": 12}},
        {"id": "ch_purification_qc", "type": "chart", "data": {"chart_name": "Purification QC Status", "col": 6}},
        {"id": "ch_downtime_rca", "type": "chart", "data": {"chart_name": "Downtime Root Cause Analysis", "col": 6}},

        # Tier 6: Financial & Logistics
        {"id": "hdr_financial", "type": "header", "data": {"text": "<span class=\"h4\"><b>Financial & Logistics</b></span>", "col": 12}},
        {"id": "ch_payments_rec", "type": "chart", "data": {"chart_name": "Payments vs Receivables", "col": 6}},
        {"id": "ch_cash_bank", "type": "chart", "data": {"chart_name": "Cash & Bank Balances", "col": 6}},
        {"id": "ch_monthly_sales", "type": "chart", "data": {"chart_name": "Monthly Sales by Product", "col": 6}},
        {"id": "ch_indirect_exp", "type": "chart", "data": {"chart_name": "Monthly Indirect Expenses", "col": 6}},
        {"id": "ch_bottle_movement", "type": "chart", "data": {"chart_name": "Bottle Ledger Movement", "col": 6}},
        {"id": "ch_otif_trend", "type": "chart", "data": {"chart_name": "Delivery OTIF Trend", "col": 6}},
    ]

    ws.content = json.dumps(content_blocks)
    ws.save(ignore_permissions=True)
    frappe.db.commit()

    # Sync workspace JSON file on disk
    ws_file = "/Users/pirated/Frappe/bench15dev/frappe-bench/apps/lean_production/lean_production/lean_production/workspace/lean_production/lean_production.json"
    if os.path.exists(ws_file):
        with open(ws_file, "r") as f:
            ws_data = json.load(f)
        ws_data["content"] = json.dumps(content_blocks)
        with open(ws_file, "w") as f:
            json.dump(ws_data, f, indent=1)
        print("  [OK] Synced lean_production.json workspace on disk.")

    print("\n=== [3/3] Number Cards and Workspace Successfully Updated! ===")

if __name__ == "__main__":
    apply_option_a()
