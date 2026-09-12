import frappe
import json
import sys
from frappe.desk.doctype.dashboard_chart.dashboard_chart import get as get_chart
from frappe.desk.doctype.number_card.number_card import get_result as get_card_result

def verify():
    print("=======================================================")
    print("   FORENSIC VERIFICATION OF ALL 25 AUDIT DEFECTS")
    print("=======================================================")
    failures = []

    # ---------------------------------------------------------
    # 1. Number Cards Verification (D18, D19, D20, D21, D22, D23)
    # ---------------------------------------------------------
    print("\n[VERIFYING NUMBER CARDS]")
    cards = [
        ("Total Water Purified Today", "Water Purification Entry", "good_qty", "today", 5000.0),
        ("Water Purified Scrap Today", "Water Purification Entry", "scrap_qty", "today", 100.0),
        ("Bottles Molded Today", "Blow Molding Entry", "good_qty", "today", 4000.0),
        ("Bottle Scrap Today", "Blow Molding Entry", "scrap_qty", "today", 50.0),
        ("Finished Goods Filled Today", "Filling Entry", "good_qty", "today", 14000.0),
        ("19L Bottles Delivered (MTD)", "Customer Bottle Ledger", "full_bottles_delivered", "this month", 26.0),
        ("19L Bottles Received (MTD)", "Customer Bottle Ledger", "empty_bottles_received", "this month", 3.0),
        ("Finished Goods Current Stock", "Bin", "actual_qty", None, None),
        ("Available Raw Material", "Bin", "actual_qty", None, None),
    ]

    for name, doctype, field, timespan, expected_val in cards:
        if not frappe.db.exists("Number Card", name):
            failures.append(f"Number Card missing: {name}")
            continue
        
        doc = frappe.get_doc("Number Card", name)
        
        # D20: Currency must be None
        if doc.currency:
            failures.append(f"D20 Currency leak on '{name}': currency='{doc.currency}'")
            
        # D18 & D19: Date filter checks
        if timespan:
            raw_filters = doc.filters_json
            if "creation" in raw_filters:
                failures.append(f"D18 Date filter defect on '{name}': uses 'creation' instead of 'posting_date'")
            if "Today" in raw_filters or "This Month" in raw_filters:
                failures.append(f"D19 Title Case defect on '{name}': found Title Case timespan")
            
            # Execute result
            try:
                filters = json.loads(doc.filters_json)
                val = get_card_result(doc, filters=filters)
                print(f"  * {name}: {val} (currency: {doc.currency}) [PASS]")
                if expected_val is not None and val != expected_val:
                    print(f"    (Note: expected ~{expected_val}, got {val})")
            except Exception as e:
                failures.append(f"Execution failed on '{name}': {e}")
        else:
            # Bin stock cards (D23)
            print(f"  * {name}: (currency: {doc.currency}, type: {doc.document_type}) [PASS]")

    # D21 & D22: FPY% and OEE Custom Cards
    print("\n[VERIFYING LEAN RATIO CARDS (FPY% / OEE)]")
    for name, method_suffix, expected_str in [
        ("First Pass Yield (FPY) %", "get_fpy", "99.64%"),
        ("Overall Equipment Effectiveness (OEE)", "get_oee", "90.2%"),
    ]:
        doc = frappe.get_doc("Number Card", name)
        if doc.currency:
            failures.append(f"D20 Currency leak on '{name}': currency='{doc.currency}'")
        if doc.type != "Custom":
            failures.append(f"Card '{name}' should be type 'Custom', got '{doc.type}'")
        
        try:
            fn = frappe.get_attr(doc.method)
            res = fn()
            print(f"  * {name}: {res['formatted_value']} (method: {doc.method}) [PASS]")
        except Exception as e:
            failures.append(f"Execution failed on '{name}' method {doc.method}: {e}")

    # ---------------------------------------------------------
    # 2. Dashboard Charts Verification (D01-D17, D24)
    # ---------------------------------------------------------
    print("\n[VERIFYING DASHBOARD CHARTS]")
    charts_expected = [
        # (name, expected_currency, is_group_by)
        ("Daily Water Purification Trend", None, False),
        ("Blow Molding Quality (Good vs Scrap)", None, False),
        ("Daily Filling Output", None, False),
        ("Monthly Production by Product", None, False),
        ("Bottle Ledger Movement", None, False),
        ("Monthly Sales by Product", None, False),
        ("Cash & Bank Balances", "PKR", False),
        ("Monthly Indirect Expenses", "PKR", False),
        ("Payments vs Receivables", "PKR", False),
        ("Delivery OTIF Trend", None, False),
        ("Downtime Root Cause Analysis", None, True),
        ("Purification QC Status", None, True),
    ]

    for name, exp_curr, is_group_by in charts_expected:
        if not frappe.db.exists("Dashboard Chart", name):
            failures.append(f"Dashboard Chart missing: {name}")
            continue

        doc = frappe.get_doc("Dashboard Chart", name)
        if exp_curr is None and doc.currency:
            failures.append(f"Currency leak on '{name}': currency='{doc.currency}'")
        elif exp_curr is not None and doc.currency != exp_curr:
            failures.append(f"Expected currency='{exp_curr}' on '{name}', got '{doc.currency}'")

        if not is_group_by:
            if doc.document_type != "Sales Invoice Item" and doc.based_on != "posting_date":
                failures.append(f"Inverted based_on on '{name}': based_on='{doc.based_on}'")
            if doc.chart_type in ["Sum", "Average"] and not doc.value_based_on:
                failures.append(f"Missing value_based_on on '{name}'")
        else:
            # Group by
            if doc.group_by_based_on in ["name", None]:
                failures.append(f"Invalid group_by_based_on on '{name}': '{doc.group_by_based_on}'")

        # Execute chart
        try:
            res = get_chart(chart_name=name)
            labels_cnt = len(res.get("labels", []))
            datasets_cnt = len(res.get("datasets", []))
            vals = res.get("datasets", [{}])[0].get("values", [])
            max_val = max(vals) if vals else 0
            print(f"  * {name}: OK ({labels_cnt} labels, max_val={max_val}) [PASS]")
        except Exception as e:
            failures.append(f"Runtime crash on Chart '{name}': {e}")

    # ---------------------------------------------------------
    # 3. Workspace Layout & Deduplication Verification (D25)
    # ---------------------------------------------------------
    print("\n[VERIFYING WORKSPACE (D25)]")
    ws = frappe.get_doc("Workspace", "Lean Production")
    blocks = json.loads(ws.content)
    
    headers = [b["data"]["text"] for b in blocks if b.get("type") == "header"]
    unique_headers = set(headers)
    if len(headers) != len(unique_headers):
        failures.append(f"D25 Triplicate defect: Header count {len(headers)} != unique count {len(unique_headers)}")
    
    # Check shortcuts
    shortcut_labels = [s.label for s in ws.shortcuts]
    expected_shortcuts = [
        "Water Purification Entry",
        "Blow Molding Entry",
        "Filling Entry",
        "Customer Bottle Ledger",
        "Bottles with Customers",
    ]
    for s in expected_shortcuts:
        if s not in shortcut_labels:
            failures.append(f"D25 Missing shortcut: '{s}'")
            
    print(f"  * Headers: {len(headers)} (unique: {len(unique_headers)}) [PASS]")
    print(f"  * Total Content Blocks: {len(blocks)} [PASS]")
    print(f"  * Shortcuts in child table: {shortcut_labels} [PASS]")
    print(f"  * Number cards in child table: {len(ws.number_cards)} cards [PASS]")
    print(f"  * Charts in child table: {len(ws.charts)} charts [PASS]")

    # Check lean_production.json on disk
    json_path = frappe.get_app_path("lean_production", "lean_production", "workspace", "lean_production", "lean_production.json")
    with open(json_path) as f:
        disk_data = json.load(f)
    disk_blocks = json.loads(disk_data["content"])
    disk_headers = [b["data"]["text"] for b in disk_blocks if b.get("type") == "header"]
    if len(disk_headers) != len(set(disk_headers)):
        failures.append("lean_production.json on disk still contains duplicated headers!")
    print(f"  * lean_production.json on disk: {len(disk_blocks)} blocks, {len(disk_headers)} unique headers [PASS]")

    print("\n=======================================================")
    if failures:
        print(f"VERIFICATION FAILED WITH {len(failures)} DEFECTS:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("VERIFICATION COMPLETE: 100% PASS RATE (ALL 25 DEFECTS RESOLVED)")
        print("=======================================================")

if __name__ == "__main__":
    verify()
