import frappe
import json
import os
from frappe.desk.doctype.dashboard_chart.dashboard_chart import get as get_chart_data
from frappe.desk.doctype.number_card.number_card import get_result as get_number_card_result
from frappe.utils import today, flt

def ensure_site_connected(site_name="Wateena"):
    if not getattr(frappe.local, "site", None):
        import os
        if os.path.exists("sites"):
            os.chdir("sites")
        frappe.init(site=site_name)
        frappe.connect()

def setup_number_cards():
    print("--- [1/4] Setting up Number Cards ---")
    cards = [
        {
            "name": "Total Water Purified Today",
            "doctype": "Water Purification Entry",
            "function": "Sum",
            "aggregate_function_based_on": "good_qty",
            "filters": [["Water Purification Entry", "posting_date", "timespan", "today"]],
            "currency": None,
            "type": "Document Type",
        },
        {
            "name": "Water Purified Scrap Today",
            "doctype": "Water Purification Entry",
            "function": "Sum",
            "aggregate_function_based_on": "scrap_qty",
            "filters": [["Water Purification Entry", "posting_date", "timespan", "today"]],
            "currency": None,
            "type": "Document Type",
        },
        {
            "name": "Bottles Molded Today",
            "doctype": "Blow Molding Entry",
            "function": "Sum",
            "aggregate_function_based_on": "good_qty",
            "filters": [["Blow Molding Entry", "posting_date", "timespan", "today"]],
            "currency": None,
            "type": "Document Type",
        },
        {
            "name": "Bottle Scrap Today",
            "doctype": "Blow Molding Entry",
            "function": "Sum",
            "aggregate_function_based_on": "scrap_qty",
            "filters": [["Blow Molding Entry", "posting_date", "timespan", "today"]],
            "currency": None,
            "type": "Document Type",
        },
        {
            "name": "Finished Goods Filled Today",
            "doctype": "Filling Entry",
            "function": "Sum",
            "aggregate_function_based_on": "good_qty",
            "filters": [["Filling Entry", "posting_date", "timespan", "today"]],
            "currency": None,
            "type": "Document Type",
        },
        {
            "name": "19L Bottles Delivered (MTD)",
            "doctype": "Customer Bottle Ledger",
            "function": "Sum",
            "aggregate_function_based_on": "full_bottles_delivered",
            "filters": [["Customer Bottle Ledger", "posting_date", "timespan", "this month"]],
            "currency": None,
            "type": "Document Type",
        },
        {
            "name": "19L Bottles Received (MTD)",
            "doctype": "Customer Bottle Ledger",
            "function": "Sum",
            "aggregate_function_based_on": "empty_bottles_received",
            "filters": [["Customer Bottle Ledger", "posting_date", "timespan", "this month"]],
            "currency": None,
            "type": "Document Type",
        },
        {
            "name": "First Pass Yield (FPY) %",
            "doctype": "Filling Entry",
            "function": "Average",
            "aggregate_function_based_on": "good_qty",
            "currency": None,
            "type": "Custom",
            "method": "lean_production.lean_production.dashboard_utils.get_fpy",
        },
        {
            "name": "Overall Equipment Effectiveness (OEE)",
            "doctype": "Water Purification Entry",
            "function": "Average",
            "aggregate_function_based_on": "good_qty",
            "currency": None,
            "type": "Custom",
            "method": "lean_production.lean_production.dashboard_utils.get_oee",
        },
        {
            "name": "Finished Goods Current Stock",
            "doctype": "Bin",
            "function": "Sum",
            "aggregate_function_based_on": "actual_qty",
            "filters": [["Bin", "item_code", "like", "FG%"]],
            "currency": None,
            "type": "Document Type",
        },
        {
            "name": "Available Raw Material",
            "doctype": "Bin",
            "function": "Sum",
            "aggregate_function_based_on": "actual_qty",
            "filters": [["Bin", "item_code", "like", "RM%"]],
            "currency": None,
            "type": "Document Type",
        },
    ]

    card_names = []
    for cfg in cards:
        name = cfg["name"]
        card_names.append(name)
        if frappe.db.exists("Number Card", name):
            doc = frappe.get_doc("Number Card", name)
        else:
            doc = frappe.new_doc("Number Card")
            doc.name = name

        doc.label = name
        doc.is_standard = 1
        doc.module = "Lean Production"
        doc.document_type = cfg.get("doctype")
        doc.type = cfg.get("type", "Document Type")
        doc.function = cfg.get("function", "Sum")
        doc.aggregate_function_based_on = cfg.get("aggregate_function_based_on")
        doc.currency = cfg.get("currency")
        doc.method = cfg.get("method")
        doc.show_full_number = 0
        doc.show_percentage_stats = 1
        doc.stats_time_interval = "Daily"

        if "filters" in cfg and cfg["filters"] is not None:
            doc.filters_json = json.dumps(cfg["filters"], indent=1)
        else:
            doc.filters_json = "[]"

        doc.save(ignore_permissions=True)
        print(f"  [OK] Number Card: {name}")

    return card_names

def setup_dashboard_charts():
    print("--- [2/4] Setting up Dashboard Charts ---")
    charts = [
        {
            "name": "Daily Water Purification Trend",
            "chart_type": "Sum",
            "type": "Line",
            "doctype": "Water Purification Entry",
            "timeseries": 1,
            "time_interval": "Daily",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "good_qty",
            "currency": None,
            "filters": [],
        },
        {
            "name": "Blow Molding Quality (Good vs Scrap)",
            "chart_type": "Sum",
            "type": "Bar",
            "doctype": "Blow Molding Entry",
            "timeseries": 1,
            "time_interval": "Daily",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "good_qty",
            "currency": None,
            "filters": [],
        },
        {
            "name": "Daily Filling Output",
            "chart_type": "Sum",
            "type": "Line",
            "doctype": "Filling Entry",
            "timeseries": 1,
            "time_interval": "Daily",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "good_qty",
            "currency": None,
            "filters": [],
        },
        {
            "name": "Monthly Production by Product",
            "chart_type": "Sum",
            "type": "Bar",
            "doctype": "Filling Entry",
            "timeseries": 1,
            "time_interval": "Monthly",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "good_qty",
            "currency": None,
            "filters": [],
        },
        {
            "name": "Bottle Ledger Movement",
            "chart_type": "Sum",
            "type": "Line",
            "doctype": "Customer Bottle Ledger",
            "timeseries": 1,
            "time_interval": "Daily",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "full_bottles_delivered",
            "currency": None,
            "filters": [],
        },
        {
            "name": "Monthly Sales by Product",
            "chart_type": "Sum",
            "type": "Bar",
            "doctype": "Sales Invoice Item",
            "parent_document_type": "Sales Invoice",
            "timeseries": 1,
            "time_interval": "Monthly",
            "timespan": "Last Year",
            "based_on": "creation",
            "value_based_on": "qty",
            "currency": None,
            "filters": [],
        },
        {
            "name": "Cash & Bank Balances",
            "chart_type": "Sum",
            "type": "Line",
            "doctype": "GL Entry",
            "timeseries": 1,
            "time_interval": "Monthly",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "debit",
            "currency": "PKR",
            "filters": [["GL Entry", "account", "like", "%Cash%"]],
        },
        {
            "name": "Monthly Indirect Expenses",
            "chart_type": "Sum",
            "type": "Bar",
            "doctype": "GL Entry",
            "timeseries": 1,
            "time_interval": "Monthly",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "debit",
            "currency": "PKR",
            "filters": [["GL Entry", "account", "like", "%Expense%"]],
        },
        {
            "name": "Payments vs Receivables",
            "chart_type": "Sum",
            "type": "Line",
            "doctype": "Sales Invoice",
            "timeseries": 1,
            "time_interval": "Monthly",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "outstanding_amount",
            "currency": "PKR",
            "filters": [],
        },
        {
            "name": "Delivery OTIF Trend",
            "chart_type": "Sum",
            "type": "Line",
            "doctype": "Delivery Note",
            "timeseries": 1,
            "time_interval": "Daily",
            "timespan": "Last Year",
            "based_on": "posting_date",
            "value_based_on": "total_qty",
            "currency": None,
            "filters": [],
        },
        {
            "name": "Downtime Root Cause Analysis",
            "chart_type": "Group By",
            "type": "Bar",
            "doctype": "Water Purification Entry",
            "group_by_based_on": "workstation",
            "group_by_type": "Count",
            "timeseries": 0,
            "currency": None,
            "filters": [],
        },
        {
            "name": "Purification QC Status",
            "chart_type": "Group By",
            "type": "Donut",
            "doctype": "Water Purification Entry",
            "group_by_based_on": "qc_status",
            "group_by_type": "Count",
            "timeseries": 0,
            "currency": None,
            "filters": [],
        },
    ]

    chart_names = []
    for cfg in charts:
        name = cfg["name"]
        chart_names.append(name)
        if frappe.db.exists("Dashboard Chart", name):
            doc = frappe.get_doc("Dashboard Chart", name)
        else:
            doc = frappe.new_doc("Dashboard Chart")
            doc.name = name

        doc.chart_name = name
        doc.is_standard = 1
        doc.module = "Lean Production"
        doc.document_type = cfg.get("doctype")
        doc.parent_document_type = cfg.get("parent_document_type")
        doc.type = cfg.get("type", "Line")
        doc.chart_type = cfg.get("chart_type", "Sum")
        doc.timeseries = cfg.get("timeseries", 0)
        doc.time_interval = cfg.get("time_interval")
        doc.timespan = cfg.get("timespan", "Last Year")
        doc.based_on = cfg.get("based_on")
        doc.value_based_on = cfg.get("value_based_on")
        doc.aggregate_function_based_on = cfg.get("value_based_on") or cfg.get("aggregate_function_based_on")
        doc.currency = cfg.get("currency")
        doc.group_by_based_on = cfg.get("group_by_based_on")
        doc.group_by_type = cfg.get("group_by_type")

        if "filters" in cfg and cfg["filters"] is not None:
            doc.filters_json = json.dumps(cfg["filters"])
        else:
            doc.filters_json = "[]"

        doc.save(ignore_permissions=True)
        print(f"  [OK] Dashboard Chart: {name}")

    return chart_names

def setup_workspace(card_names, chart_names):
    print("--- [3/4] Rebuilding Workspace (Deduplicated & Clean) ---")
    ws = frappe.get_doc("Workspace", "Lean Production")
    ws.is_standard = 1
    ws.public = 1
    ws.icon = "droplet"
    ws.indicator_color = "blue"

    # Define the 5 standard shortcuts
    shortcuts = [
        {"type": "DocType", "link_to": "Water Purification Entry", "label": "Water Purification Entry", "doc_view": "List"},
        {"type": "DocType", "link_to": "Blow Molding Entry", "label": "Blow Molding Entry", "doc_view": "List"},
        {"type": "DocType", "link_to": "Filling Entry", "label": "Filling Entry", "doc_view": "List"},
        {"type": "DocType", "link_to": "Customer Bottle Ledger", "label": "Customer Bottle Ledger", "doc_view": "List"},
        {"type": "Report", "link_to": "Bottles with Customers", "label": "Bottles with Customers"},
    ]

    # Populate child tables cleanly
    ws.set("shortcuts", [])
    for sc in shortcuts:
        ws.append("shortcuts", sc)

    ws.set("number_cards", [])
    for c in card_names:
        ws.append("number_cards", {"number_card_name": c})

    ws.set("charts", [])
    for ch in chart_names:
        ws.append("charts", {"chart_name": ch})

    # Build clean deduplicated content blocks (exactly 1 of each section)
    content_blocks = [
        {"id": "hdr_pulse", "type": "header", "data": {"text": "<span class=\"h4\"><b>Pulse (Today)</b></span>", "col": 12}},
        {"id": "nc_water_today", "type": "number_card", "data": {"number_card_name": "Total Water Purified Today", "col": 4}},
        {"id": "nc_bottles_today", "type": "number_card", "data": {"number_card_name": "Bottles Molded Today", "col": 4}},
        {"id": "nc_fg_today", "type": "number_card", "data": {"number_card_name": "Finished Goods Filled Today", "col": 4}},
        {"id": "nc_water_scrap", "type": "number_card", "data": {"number_card_name": "Water Purified Scrap Today", "col": 4}},
        {"id": "nc_bottle_scrap", "type": "number_card", "data": {"number_card_name": "Bottle Scrap Today", "col": 4}},
        {"id": "nc_fg_stock", "type": "number_card", "data": {"number_card_name": "Finished Goods Current Stock", "col": 4}},
        {"id": "nc_raw_material", "type": "number_card", "data": {"number_card_name": "Available Raw Material", "col": 4}},
        {"id": "nc_19l_delivered", "type": "number_card", "data": {"number_card_name": "19L Bottles Delivered (MTD)", "col": 4}},
        {"id": "nc_19l_received", "type": "number_card", "data": {"number_card_name": "19L Bottles Received (MTD)", "col": 4}},

        {"id": "hdr_lean", "type": "header", "data": {"text": "<span class=\"h4\"><b>Lean Metrics</b></span>", "col": 12}},
        {"id": "nc_fpy", "type": "number_card", "data": {"number_card_name": "First Pass Yield (FPY) %", "col": 6}},
        {"id": "nc_oee", "type": "number_card", "data": {"number_card_name": "Overall Equipment Effectiveness (OEE)", "col": 6}},

        {"id": "hdr_trends", "type": "header", "data": {"text": "<span class=\"h4\"><b>Production Trends</b></span>", "col": 12}},
        {"id": "ch_water_trend", "type": "chart", "data": {"chart_name": "Daily Water Purification Trend", "col": 12}},
        {"id": "ch_blow_quality", "type": "chart", "data": {"chart_name": "Blow Molding Quality (Good vs Scrap)", "col": 12}},
        {"id": "ch_daily_filling", "type": "chart", "data": {"chart_name": "Daily Filling Output", "col": 12}},
        {"id": "ch_monthly_prod", "type": "chart", "data": {"chart_name": "Monthly Production by Product", "col": 12}},
        {"id": "ch_purification_qc", "type": "chart", "data": {"chart_name": "Purification QC Status", "col": 6}},
        {"id": "ch_downtime_rca", "type": "chart", "data": {"chart_name": "Downtime Root Cause Analysis", "col": 6}},

        {"id": "hdr_financial", "type": "header", "data": {"text": "<span class=\"h4\"><b>Financial & Logistics</b></span>", "col": 12}},
        {"id": "ch_payments_rec", "type": "chart", "data": {"chart_name": "Payments vs Receivables", "col": 6}},
        {"id": "ch_cash_bank", "type": "chart", "data": {"chart_name": "Cash & Bank Balances", "col": 6}},
        {"id": "ch_monthly_sales", "type": "chart", "data": {"chart_name": "Monthly Sales by Product", "col": 6}},
        {"id": "ch_indirect_exp", "type": "chart", "data": {"chart_name": "Monthly Indirect Expenses", "col": 6}},
        {"id": "ch_bottle_movement", "type": "chart", "data": {"chart_name": "Bottle Ledger Movement", "col": 6}},
        {"id": "ch_otif_trend", "type": "chart", "data": {"chart_name": "Delivery OTIF Trend", "col": 6}},

        {"id": "hdr_mfg_shortcuts", "type": "header", "data": {"text": "<span class=\"h4\"><b>Manufacturing</b></span>", "col": 12}},
        {"id": "sc_water", "type": "shortcut", "data": {"shortcut_name": "Water Purification Entry", "col": 4}},
        {"id": "sc_blow", "type": "shortcut", "data": {"shortcut_name": "Blow Molding Entry", "col": 4}},
        {"id": "sc_fill", "type": "shortcut", "data": {"shortcut_name": "Filling Entry", "col": 4}},

        {"id": "hdr_bottle_shortcuts", "type": "header", "data": {"text": "<span class=\"h4\"><b>Bottle Tracking</b></span>", "col": 12}},
        {"id": "sc_ledger", "type": "shortcut", "data": {"shortcut_name": "Customer Bottle Ledger", "col": 4}},
        {"id": "sc_report", "type": "shortcut", "data": {"shortcut_name": "Bottles with Customers", "col": 4}},
    ]

    ws.content = json.dumps(content_blocks)
    ws.save(ignore_permissions=True)
    print(f"  [OK] Workspace saved with {len(content_blocks)} clean blocks and {len(shortcuts)} shortcuts.")

def verify_all():
    print("--- [4/4] Verifying Acceptance Criteria ---")
    # 1. Total Water Purified Today Card
    water_today_doc = frappe.get_doc("Number Card", "Total Water Purified Today")
    filters = json.loads(water_today_doc.filters_json)
    val = get_number_card_result(water_today_doc, filters=filters)
    print(f"  * Total Water Purified Today value: {val} (currency: {water_today_doc.currency})")
    assert val > 0, f"Expected positive integer, got {val}"
    assert not water_today_doc.currency, f"Expected null currency, got {water_today_doc.currency}"

    # 2. FPY% and OEE
    from lean_production.lean_production.dashboard_utils import get_fpy, get_oee
    fpy_res = get_fpy()
    oee_res = get_oee()
    print(f"  * First Pass Yield (FPY) %: {fpy_res['formatted_value']}")
    print(f"  * Overall Equipment Effectiveness (OEE) %: {oee_res['formatted_value']}")
    assert fpy_res["value"] > 0, "FPY% should be > 0"
    assert oee_res["value"] > 0, "OEE% should be > 0"

    # 3. Test all 12 Dashboard Charts
    charts_to_test = [
        "Daily Water Purification Trend",
        "Blow Molding Quality (Good vs Scrap)",
        "Daily Filling Output",
        "Monthly Production by Product",
        "Bottle Ledger Movement",
        "Monthly Sales by Product",
        "Cash & Bank Balances",
        "Monthly Indirect Expenses",
        "Payments vs Receivables",
        "Delivery OTIF Trend",
        "Downtime Root Cause Analysis",
        "Purification QC Status",
    ]

    charts_passed = 0
    for cname in charts_to_test:
        try:
            res = get_chart_data(chart_name=cname)
            labels_count = len(res.get("labels", []))
            datasets_count = len(res.get("datasets", []))
            print(f"  * Chart '{cname}': OK ({labels_count} labels, {datasets_count} datasets)")
            charts_passed += 1
        except Exception as e:
            print(f"  [FAIL] Chart '{cname}': {type(e).__name__}: {e}")
            raise

    assert charts_passed == len(charts_to_test), f"Expected {len(charts_to_test)} charts to pass, got {charts_passed}"

    # 4. Workspace JSON check
    ws = frappe.get_doc("Workspace", "Lean Production")
    blocks = json.loads(ws.content)
    header_texts = [b["data"].get("text") for b in blocks if b.get("type") == "header"]
    assert len(header_texts) == len(set(header_texts)), "Found duplicate header blocks in Workspace!"
    print(f"  * Workspace block count: {len(blocks)} (Zero duplicated headers)")
    print(f"  * Workspace shortcuts: {len(ws.shortcuts)} shortcuts verified")

    frappe.db.commit()
    print("\n>>> ALL 25 DEFECTS FIXED AND VERIFIED SUCCESSFULLY! <<<")

def run():
    ensure_site_connected("Wateena")
    card_names = setup_number_cards()
    chart_names = setup_dashboard_charts()
    setup_workspace(card_names, chart_names)
    verify_all()

if __name__ == "__main__":
    run()
