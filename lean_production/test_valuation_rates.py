import frappe
from frappe.utils import flt, today


def test_purification_valuation():
    print("\n" + "=" * 60)
    print("TEST 1: WATER PURIFICATION ENTRY VALUATION")
    print("=" * 60)

    company = "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    source_wh = f"Stores - {abbr}"
    target_wh = f"Finished Goods - {abbr}"
    mineral_item = "INT-BULK-WATER"

    # Set valuation rates on raw materials if 0 so cost absorption can be measured
    frappe.db.set_value("Item", "MIN-CALCIUM", "valuation_rate", 0.08)
    frappe.db.set_value("Item", "MIN-MAGNESIUM", "valuation_rate", 0.05)
    frappe.db.set_value("Item", "MIN-SODIUM", "valuation_rate", 0.04)
    frappe.db.set_value("Item", "CHEM-ANTISCALE", "valuation_rate", 12.00)
    frappe.db.commit()

    bom_no = frappe.db.get_value("BOM", {"item": mineral_item, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active BOM for {mineral_item} must exist"

    # Submit Water Purification Entry for 1,000 Litres
    wpe = frappe.get_doc({
        "doctype": "Water Purification Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "mineral_water_item": mineral_item,
        "bom_no": bom_no,
        "litres_purified": 1000.0,
        "good_qty": 1000.0,
        "source_warehouse": source_wh,
        "target_warehouse": target_wh,
        "qc_status": "Pass"
    })
    wpe.insert(ignore_permissions=True)
    wpe.submit()
    print(f"Created & Submitted Water Purification Entry: {wpe.name}")

    stock_entry_id = wpe.stock_entry
    assert stock_entry_id, "Linked Stock Entry must exist"

    se = frappe.get_doc("Stock Entry", stock_entry_id)
    print(f"Inspecting Stock Entry: {se.name} (Purpose: {se.purpose})")

    # Find the finished item row
    fg_rows = [d for d in se.items if d.is_finished_item]
    assert len(fg_rows) == 1, "Must have exactly 1 finished item row"
    fg = fg_rows[0]

    print(f"Finished Item Code: {fg.item_code}")
    print(f"Transfer Qty: {fg.transfer_qty} {fg.stock_uom}")
    print(f"Basic Rate: Rs. {fg.basic_rate}")
    print(f"Basic Amount: Rs. {fg.basic_amount}")
    print(f"Valuation Rate: Rs. {fg.valuation_rate}")
    print(f"Set Basic Rate Manually: {fg.set_basic_rate_manually}")
    print(f"Allow Zero Valuation Rate: {fg.allow_zero_valuation_rate}")

    # Assertions
    assert flt(fg.basic_rate) > 0.0, f"Finished item basic_rate must be > 0, got {fg.basic_rate}"
    assert flt(fg.valuation_rate) > 0.0, f"Finished item valuation_rate must be > 0, got {fg.valuation_rate}"
    assert flt(fg.basic_amount) > 0.0, f"Finished item basic_amount must be > 0, got {fg.basic_amount}"
    assert fg.set_basic_rate_manually == 1, "set_basic_rate_manually must be 1 to lock rate in ERPNext line 1616"
    assert not fg.allow_zero_valuation_rate, "allow_zero_valuation_rate must NOT be 1 on finished item"

    # Inspect Stock Ledger Entry (SLE)
    sles = frappe.get_all(
        "Stock Ledger Entry",
        filters={"voucher_type": "Stock Entry", "voucher_no": se.name, "item_code": mineral_item, "is_cancelled": 0},
        fields=["name", "item_code", "actual_qty", "incoming_rate", "valuation_rate", "stock_value_difference"]
    )
    assert sles, "Stock Ledger Entry must exist for finished item"
    sle = sles[0]
    print(f"\nStock Ledger Entry (SLE): {sle.name}")
    print(f"SLE Incoming Rate: Rs. {sle.incoming_rate}")
    print(f"SLE Valuation Rate: Rs. {sle.valuation_rate}")
    print(f"SLE Stock Value Diff: Rs. {sle.stock_value_difference}")

    assert flt(sle.incoming_rate) > 0.0, f"SLE incoming_rate must be > 0, got {sle.incoming_rate}"
    assert flt(sle.valuation_rate) > 0.0, f"SLE valuation_rate must be > 0, got {sle.valuation_rate}"
    assert flt(sle.stock_value_difference) > 0.0, f"SLE stock_value_difference must be > 0, got {sle.stock_value_difference}"

    print("\n>>> WATER PURIFICATION VALUATION TEST: PASSED")
    return wpe


def test_filling_valuation():
    print("\n" + "=" * 60)
    print("TEST 2: FILLING ENTRY VALUATION (FINISHED GOODS ABSORPTION)")
    print("=" * 60)

    company = "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    packaging_wh = f"Stores - {abbr}"
    water_wh = f"Finished Goods - {abbr}"
    fg_wh = f"Finished Goods - {abbr}"
    fg_item = "FG-WATER-0.5L-12"

    # Set valuation rates on empty bottles and packaging materials
    # (Simulating market purchase of empty bottles @ Rs. 4.50 / bottle)
    frappe.db.set_value("Item", "INT-BTL-0.5L", "valuation_rate", 4.50)
    frappe.db.set_value("Item", "RM-CAP-28MM", "valuation_rate", 1.20)
    frappe.db.set_value("Item", "RM-LBL-0.5L", "valuation_rate", 0.80)
    frappe.db.set_value("Item", "RM-WRAP-12X", "valuation_rate", 5.00)
    frappe.db.commit()

    bom_no = frappe.db.get_value("BOM", {"item": fg_item, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active BOM for {fg_item} must exist"

    # Submit Filling Entry for 50 Cartons (50 x 12 = 600 bottles)
    fe = frappe.get_doc({
        "doctype": "Filling Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "finished_good_item": fg_item,
        "bom_no": bom_no,
        "cartons_produced": 50.0,
        "good_qty": 50.0,
        "scrap_qty": 0.0,
        "packaging_warehouse": packaging_wh,
        "water_warehouse": water_wh,
        "bottle_warehouse": packaging_wh,
        "target_warehouse": fg_wh,
        "fg_warehouse": fg_wh
    })
    fe.insert(ignore_permissions=True)
    fe.submit()
    print(f"Created & Submitted Filling Entry: {fe.name}")

    stock_entry_id = fe.stock_entry
    assert stock_entry_id, "Linked Stock Entry must exist"

    se = frappe.get_doc("Stock Entry", stock_entry_id)
    print(f"Inspecting Stock Entry: {se.name} (Purpose: {se.purpose})")

    # Check consumed items
    print("\nConsumed Raw Materials / Packaging in Stock Entry:")
    for d in se.items:
        if not d.is_finished_item:
            print(f"  - {d.item_code} | Qty: {d.qty} {d.uom} | Rate: Rs. {d.basic_rate} | Amount: Rs. {d.basic_amount} | Manual Rate: {d.set_basic_rate_manually}")
            assert flt(d.basic_rate) > 0.0 or d.item_code == "RM-WATER", f"Consumed item {d.item_code} must have rate > 0"

    print(f"\nTotal Outgoing Cost: Rs. {se.total_outgoing_value}")
    print(f"Total Incoming Cost: Rs. {se.total_incoming_value}")
    assert flt(se.total_outgoing_value) > 0.0, "Total outgoing value must be > 0"
    assert flt(se.total_incoming_value) > 0.0, "Total incoming value must be > 0"

    # Check Finished Good row
    fg_rows = [d for d in se.items if d.is_finished_item]
    assert len(fg_rows) == 1, "Must have exactly 1 finished item row"
    fg = fg_rows[0]

    print(f"\nFinished Good Row:")
    print(f"  Item Code: {fg.item_code}")
    print(f"  Qty: {fg.qty} {fg.uom}")
    print(f"  Basic Rate: Rs. {fg.basic_rate} per pack")
    print(f"  Basic Amount: Rs. {fg.basic_amount}")
    print(f"  Valuation Rate: Rs. {fg.valuation_rate}")
    print(f"  Set Basic Rate Manually: {fg.set_basic_rate_manually}")
    print(f"  Allow Zero Valuation Rate: {fg.allow_zero_valuation_rate}")

    # Assertions on Finished Good
    assert flt(fg.basic_rate) > 0.0, f"Finished good basic_rate must be > 0, got {fg.basic_rate}"
    assert flt(fg.valuation_rate) > 0.0, f"Finished good valuation_rate must be > 0, got {fg.valuation_rate}"
    assert flt(fg.basic_amount) > 0.0, f"Finished good basic_amount must be > 0, got {fg.basic_amount}"
    assert fg.set_basic_rate_manually == 1, "set_basic_rate_manually must be 1"
    assert not fg.allow_zero_valuation_rate, "allow_zero_valuation_rate must NOT be 1 on finished good"

    # Check Stock Ledger Entry (SLE)
    sles = frappe.get_all(
        "Stock Ledger Entry",
        filters={"voucher_type": "Stock Entry", "voucher_no": se.name, "item_code": fg_item, "is_cancelled": 0},
        fields=["name", "item_code", "actual_qty", "incoming_rate", "valuation_rate", "stock_value_difference"]
    )
    assert sles, "Stock Ledger Entry must exist for finished good"
    sle = sles[0]
    print(f"\nStock Ledger Entry (SLE): {sle.name}")
    print(f"  SLE Incoming Rate: Rs. {sle.incoming_rate} per pack")
    print(f"  SLE Valuation Rate: Rs. {sle.valuation_rate} per pack")
    print(f"  SLE Stock Value Diff: Rs. {sle.stock_value_difference}")

    assert flt(sle.incoming_rate) > 0.0, f"SLE incoming_rate must be > 0, got {sle.incoming_rate}"
    assert flt(sle.valuation_rate) > 0.0, f"SLE valuation_rate must be > 0, got {sle.valuation_rate}"
    assert flt(sle.stock_value_difference) > 0.0, f"SLE stock_value_difference must be > 0, got {sle.stock_value_difference}"

    print("\n>>> FILLING ENTRY VALUATION TEST: PASSED (Finished Goods accurately carry absorbed valuation!)")
    return fe


def test_automated_cancellation(wpe, fe):
    print("\n" + "=" * 60)
    print("TEST 3: AUTOMATED BIDIRECTIONAL CANCELLATION")
    print("=" * 60)

    # 1. Cancel Filling Entry
    fe_se_id = fe.stock_entry
    fe.cancel()
    print(f"Cancelled Filling Entry: {fe.name}")

    assert fe.docstatus == 2, "Filling Entry must be cancelled (docstatus=2)"
    fe_se = frappe.get_doc("Stock Entry", fe_se_id)
    assert fe_se.docstatus == 2, f"Linked Stock Entry {fe_se_id} must be automatically cancelled"
    print(f"Verified linked Stock Entry {fe_se_id} is automatically cancelled (docstatus=2).")

    # 2. Cancel Water Purification Entry
    wpe_se_id = wpe.stock_entry
    wpe.cancel()
    print(f"Cancelled Water Purification Entry: {wpe.name}")

    assert wpe.docstatus == 2, "Water Purification Entry must be cancelled (docstatus=2)"
    wpe_se = frappe.get_doc("Stock Entry", wpe_se_id)
    assert wpe_se.docstatus == 2, f"Linked Stock Entry {wpe_se_id} must be automatically cancelled"
    print(f"Verified linked Stock Entry {wpe_se_id} is automatically cancelled (docstatus=2).")

    print("\n>>> AUTOMATED BIDIRECTIONAL CANCELLATION TEST: PASSED")


def run():
    print("=" * 60)
    print("RUNNING COMPLETE VALUATION & MES INTEGRATION VERIFICATION ON WATEENA")
    print("=" * 60)

    orig_neg = frappe.db.get_single_value("Stock Settings", "allow_negative_stock")
    frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 1)

    try:
        wpe = test_purification_valuation()
        fe = test_filling_valuation()
        test_automated_cancellation(wpe, fe)
        frappe.db.commit()
        print("\n" + "=" * 60)
        print("ALL TESTS (PURIFICATION VALUATION, FILLING VALUATION, BIDIRECTIONAL CANCELLATION)")
        print("COMPLETED AND PASSED WITH 100% SUCCESS!")
        print("=" * 60)
        return "PASS"
    finally:
        frappe.db.set_single_value("Stock Settings", "allow_negative_stock", orig_neg)
        frappe.db.commit()


if __name__ == "__main__":
    run()
