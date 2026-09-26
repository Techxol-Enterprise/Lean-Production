import frappe
from frappe.utils import flt, today


def test_purification_entry_cancellation():
    print("\n--- Testing Water Purification Entry Cancellation & Amendment ---")
    company = "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    source_wh = f"Stores - {abbr}"
    target_wh = f"Finished Goods - {abbr}"
    mineral_item = "INT-BULK-WATER"

    bom_no = frappe.db.get_value("BOM", {"item": mineral_item, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active BOM for {mineral_item} must exist"

    # 1. Create and submit Water Purification Entry
    wpe = frappe.get_doc({
        "doctype": "Water Purification Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "mineral_water_item": mineral_item,
        "bom_no": bom_no,
        "litres_purified": 100.0,
        "good_qty": 100.0,
        "source_warehouse": source_wh,
        "target_warehouse": target_wh,
        "qc_status": "Pass"
    })
    wpe.insert(ignore_permissions=True)
    wpe.submit()
    print(f"Created & Submitted Water Purification Entry: {wpe.name}")

    stock_entry_id = wpe.stock_entry or frappe.db.get_value("Water Purification Entry", wpe.name, "stock_entry")
    assert stock_entry_id, "Linked Stock Entry must be generated on submit"
    se1 = frappe.get_doc("Stock Entry", stock_entry_id)
    assert se1.docstatus == 1, f"Stock Entry {se1.name} must be submitted"
    print(f"Verified Linked Stock Entry {se1.name} is SUBMITTED (docstatus=1)")

    # 2. Cancel the Water Purification Entry
    wpe.cancel()
    print(f"Cancelled Water Purification Entry: {wpe.name}")

    # Reload Stock Entry and verify it was automatically cancelled
    se1.reload()
    assert se1.docstatus == 2, f"Stock Entry {se1.name} must be CANCELLED (docstatus=2), got {se1.docstatus}"
    print(f"Verified Linked Stock Entry {se1.name} is CANCELLED (docstatus=2) automatically!")

    # 3. Test Amendment workflow
    from frappe.model.mapper import get_mapped_doc
    # In Frappe, amend copies document with amended_from
    wpe_amended = frappe.copy_doc(wpe)
    wpe_amended.amended_from = wpe.name
    wpe_amended.docstatus = 0
    wpe_amended.insert(ignore_permissions=True)
    print(f"Created Amended Draft: {wpe_amended.name}")

    assert not wpe_amended.stock_entry, (
        f"Amended draft {wpe_amended.name} must have stock_entry cleared, got: {wpe_amended.stock_entry}"
    )
    print(f"Verified Amended Draft {wpe_amended.name} has stock_entry=None (clean slate)")

    # 4. Submit amended document with rectified quantity
    wpe_amended.good_qty = 150.0
    wpe_amended.litres_purified = 150.0
    wpe_amended.submit()
    print(f"Submitted Amended Water Purification Entry: {wpe_amended.name}")

    new_se_id = wpe_amended.stock_entry or frappe.db.get_value("Water Purification Entry", wpe_amended.name, "stock_entry")
    assert new_se_id, "New Stock Entry must be created for amended entry"
    assert new_se_id != stock_entry_id, f"New Stock Entry must differ from cancelled Stock Entry {stock_entry_id}"
    se2 = frappe.get_doc("Stock Entry", new_se_id)
    assert se2.docstatus == 1, f"New Stock Entry {se2.name} must be submitted"
    print(f"Verified New Stock Entry {se2.name} was cleanly created & submitted (docstatus=1)")

    # Clean up test amended document
    wpe_amended.cancel()
    se2.reload()
    assert se2.docstatus == 2, f"Stock Entry {se2.name} must be cancelled after cancelling amended WPE"
    print(f"Cleaned up amended WPE and verified {se2.name} is cancelled.")


def test_filling_entry_cancellation():
    print("\n--- Testing Filling Entry Cancellation & Amendment ---")
    company = "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    packaging_wh = f"Stores - {abbr}"
    water_wh = f"Finished Goods - {abbr}"
    fg_wh = f"Finished Goods - {abbr}"
    fg_item = "FG-WATER-0.5L-12"

    bom_no = frappe.db.get_value("BOM", {"item": fg_item, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active BOM for {fg_item} must exist"

    # 1. Create and submit Filling Entry
    fe = frappe.get_doc({
        "doctype": "Filling Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "finished_good_item": fg_item,
        "bom_no": bom_no,
        "cartons_produced": 10.0,
        "good_qty": 10.0,
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

    stock_entry_id = fe.stock_entry or frappe.db.get_value("Filling Entry", fe.name, "stock_entry")
    assert stock_entry_id, "Linked Stock Entry must be generated on submit"
    se = frappe.get_doc("Stock Entry", stock_entry_id)
    assert se.docstatus == 1, f"Stock Entry {se.name} must be submitted"
    print(f"Verified Linked Stock Entry {se.name} is SUBMITTED (docstatus=1)")

    # 2. Cancel the Filling Entry
    fe.cancel()
    print(f"Cancelled Filling Entry: {fe.name}")

    # Reload Stock Entry and verify it was automatically cancelled
    se.reload()
    assert se.docstatus == 2, f"Stock Entry {se.name} must be CANCELLED (docstatus=2), got {se.docstatus}"
    print(f"Verified Linked Stock Entry {se.name} is CANCELLED (docstatus=2) automatically!")

    # 3. Test Amendment workflow
    fe_amended = frappe.copy_doc(fe)
    fe_amended.amended_from = fe.name
    fe_amended.docstatus = 0
    fe_amended.insert(ignore_permissions=True)
    print(f"Created Amended Draft: {fe_amended.name}")

    assert not fe_amended.stock_entry, (
        f"Amended draft {fe_amended.name} must have stock_entry cleared, got: {fe_amended.stock_entry}"
    )
    print(f"Verified Amended Draft {fe_amended.name} has stock_entry=None (clean slate)")

    # 4. Submit amended document with rectified quantity
    fe_amended.good_qty = 15.0
    fe_amended.cartons_produced = 15.0
    fe_amended.submit()
    print(f"Submitted Amended Filling Entry: {fe_amended.name}")

    new_se_id = fe_amended.stock_entry or frappe.db.get_value("Filling Entry", fe_amended.name, "stock_entry")
    assert new_se_id, "New Stock Entry must be created for amended entry"
    assert new_se_id != stock_entry_id, f"New Stock Entry must differ from cancelled Stock Entry {stock_entry_id}"
    se2 = frappe.get_doc("Stock Entry", new_se_id)
    assert se2.docstatus == 1, f"New Stock Entry {se2.name} must be submitted"
    print(f"Verified New Stock Entry {se2.name} was cleanly created & submitted (docstatus=1)")

    # Clean up test amended document
    fe_amended.cancel()
    se2.reload()
    assert se2.docstatus == 2, f"Stock Entry {se2.name} must be cancelled after cancelling amended FE"
    print(f"Cleaned up amended FE and verified {se2.name} is cancelled.")


def test_downstream_consumption_guard():
    print("\n--- Testing Downstream Consumption Guard ---")
    company = "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    source_wh = f"Stores - {abbr}"
    target_wh = f"Finished Goods - {abbr}"
    mineral_item = "INT-BULK-WATER"

    bom_no = frappe.db.get_value("BOM", {"item": mineral_item, "is_active": 1, "docstatus": 1}, "name")

    # 1. Create and submit Water Purification Entry for 100L
    wpe = frappe.get_doc({
        "doctype": "Water Purification Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "mineral_water_item": mineral_item,
        "bom_no": bom_no,
        "litres_purified": 100.0,
        "good_qty": 100.0,
        "source_warehouse": source_wh,
        "target_warehouse": target_wh,
        "qc_status": "Pass"
    })
    wpe.insert(ignore_permissions=True)
    wpe.submit()

    stock_entry_id = wpe.stock_entry
    se = frappe.get_doc("Stock Entry", stock_entry_id)

    # 2. Simulate downstream consumption:
    # Disable allow_negative_stock and issue out stock from target_wh so remaining balance < 100L
    frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 0)

    current_bal = flt(frappe.db.get_value("Bin", {"item_code": mineral_item, "warehouse": target_wh}, "actual_qty") or 0.0)

    # Create a material issue to deplete the stock below 100L
    ste_issue = frappe.get_doc({
        "doctype": "Stock Entry",
        "purpose": "Material Issue",
        "stock_entry_type": "Material Issue",
        "company": company,
        "items": [{
            "item_code": mineral_item,
            "s_warehouse": target_wh,
            "qty": current_bal,
            "basic_rate": 0.50
        }]
    })
    ste_issue.insert(ignore_permissions=True)
    ste_issue.submit()

    # Now target_wh balance is 0. Attempting to cancel WPE (which produced 100L) must trigger our guard!
    guard_triggered = False
    try:
        wpe.cancel()
    except Exception as e:
        frappe.db.rollback()
        if "Downstream Stock Already Consumed" in str(e) or "has already been consumed" in str(e):
            guard_triggered = True
            print("Successfully caught Downstream Stock Consumption Guard error as expected!")
        else:
            raise e

    assert guard_triggered, "Expected downstream consumption guard to trigger and block cancellation!"
    print("Guard verification complete (transaction cleanly rolled back).")


def run():
    print("=" * 60)
    print("RUNNING AUTOMATED VERIFICATION ON SITE WATEENA")
    print("=" * 60)

    # Enable negative stock temporarily for testing if local warehouse is fresh
    orig_neg = frappe.db.get_single_value("Stock Settings", "allow_negative_stock")
    frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 1)

    try:
        test_purification_entry_cancellation()
        test_filling_entry_cancellation()
        test_downstream_consumption_guard()
        frappe.db.commit()
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED WITH 100% SUCCESS!")
        print("=" * 60)
        return "PASS"
    finally:
        frappe.db.set_single_value("Stock Settings", "allow_negative_stock", orig_neg)
        frappe.db.commit()
        frappe.db.set_single_value("Stock Settings", "allow_negative_stock", orig_neg)
        frappe.db.commit()


if __name__ == "__main__":
    run()
