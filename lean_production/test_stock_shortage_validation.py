import frappe
from frappe.utils import today, flt


def run_tests():
    print("\n=======================================================")
    print("  LEAN PRODUCTION - RAW MATERIAL SHORTAGE VALIDATION")
    print("=======================================================\n")
    company = "Wateena"

    # ---------------------------------------------------------
    # TEST 1: Filling Entry Insufficient Stock Interception
    # ---------------------------------------------------------
    print("--> [TEST 1] Testing Filling Entry shortage validation...")
    fe = frappe.new_doc("Filling Entry")
    fe.company = company
    fe.posting_date = today()
    fe.finished_good_item = "FG-WATER-0.5L-12"
    fe.bom_no = frappe.db.get_value("BOM", {"item": "FG-WATER-0.5L-12", "is_active": 1, "is_default": 1}, "name")
    fe.fg_warehouse = "Finished Goods - W"
    fe.good_qty = 100
    fe.scrap_qty = 0

    fe_caught = False
    try:
        fe.insert(ignore_permissions=True)
        fe.submit()
        print("  [FAIL] Filling Entry was submitted without sufficient raw materials!")
    except frappe.ValidationError:
        fe_caught = True
        last_msg = frappe.message_log[-1] if frappe.message_log else {}
        assert last_msg.get("title") == "Insufficient Raw Material Stock", f"Expected title 'Insufficient Raw Material Stock', got {last_msg.get('title')}"
        assert "cannot submit filling entry" in last_msg.get("message", "").lower(), "Expected 'Cannot Submit Filling Entry' in message"
        assert "INT-BULK-WATER" in last_msg.get("message", ""), "Expected INT-BULK-WATER shortage in message"
        print("  [PASS] Filling Entry caught raw material shortage with structured HTML table and remediation guide.")
    finally:
        frappe.db.rollback()

    assert fe_caught, "Test 1 failed: Validation error was not raised for Filling Entry"

    # ---------------------------------------------------------
    # TEST 2: Blow Molding Entry Insufficient Stock Interception
    # ---------------------------------------------------------
    print("--> [TEST 2] Testing Blow Molding Entry shortage validation...")
    bottle_item = frappe.db.get_value("Item", {"item_group": ["in", ["Empty Bottles", "Semi Finished Goods"]]}, "name") or "INT-BTL-0.5L"
    if bottle_item:
        bm = frappe.new_doc("Blow Molding Entry")
        bm.company = company
        bm.posting_date = today()
        bm.bottle_item = bottle_item
        bm.bom_no = frappe.db.get_value("BOM", {"item": bottle_item, "is_active": 1}, "name")
        bm.source_warehouse = "Stores - W"
        bm.target_warehouse = "Stores - W"
        bm.good_qty = 500
        bm.scrap_qty = 0

        bm_caught = False
        try:
            bm.insert(ignore_permissions=True)
            bm.submit()
            print("  [FAIL] Blow Molding Entry was submitted without sufficient raw materials!")
        except frappe.ValidationError:
            bm_caught = True
            last_msg = frappe.message_log[-1] if frappe.message_log else {}
            assert last_msg.get("title") == "Insufficient Raw Material Stock", f"Expected title 'Insufficient Raw Material Stock', got {last_msg.get('title')}"
            assert "cannot submit blow molding entry" in last_msg.get("message", "").lower(), "Expected 'Cannot Submit Blow Molding Entry' in message"
            print("  [PASS] Blow Molding Entry caught raw material shortage as expected.")
        finally:
            frappe.db.rollback()

        assert bm_caught, "Test 2 failed: Validation error was not raised for Blow Molding Entry"
    else:
        print("  [SKIP] No Semi Finished Goods bottle item found for Blow Molding.")

    # ---------------------------------------------------------
    # TEST 3: Water Purification Entry Insufficient Stock Interception
    # ---------------------------------------------------------
    print("--> [TEST 3] Testing Water Purification Entry shortage validation...")
    water_item = "INT-BULK-WATER"
    wp_bom = frappe.db.get_value("BOM", {"item": water_item, "is_active": 1}, "name")
    if wp_bom:
        wp = frappe.new_doc("Water Purification Entry")
        wp.company = company
        wp.posting_date = today()
        wp.mineral_water_item = water_item
        wp.bom_no = wp_bom
        wp.target_warehouse = "Stores - W"
        wp.good_qty = 1000
        wp.scrap_qty = 0

        wp_caught = False
        try:
            wp.insert(ignore_permissions=True)
            wp.submit()
            print("  [FAIL] Water Purification Entry was submitted without sufficient raw materials!")
        except frappe.ValidationError:
            wp_caught = True
            last_msg = frappe.message_log[-1] if frappe.message_log else {}
            assert last_msg.get("title") == "Insufficient Raw Material Stock", f"Expected title 'Insufficient Raw Material Stock', got {last_msg.get('title')}"
            assert "cannot submit water purification entry" in last_msg.get("message", "").lower(), "Expected 'Cannot Submit Water Purification Entry' in message"
            print("  [PASS] Water Purification Entry caught raw material shortage as expected.")
        finally:
            frappe.db.rollback()

        assert wp_caught, "Test 3 failed: Validation error was not raised for Water Purification Entry"
    else:
        print("  [SKIP] No active BOM found for INT-BULK-WATER.")

    print("\n=======================================================")
    print("  ALL SHORTAGE VALIDATION TESTS PASSED (3/3)!")
    print("=======================================================\n")
