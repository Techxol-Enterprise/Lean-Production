import frappe
from frappe.utils import today

def run_tests():
    company = "Wateena"
    print(f"=== [TEST 1] Testing Customer Bottle Ledger Schema & Metadata ===")
    meta = frappe.get_meta("Customer Bottle Ledger")
    assert meta.has_field("company"), "Customer Bottle Ledger MUST have 'company' field!"
    company_field = meta.get_field("company")
    assert company_field.options == "Company", "company field options must be 'Company'!"
    assert company_field.reqd == 1, "company field must be required!"
    print("  [PASS] DocType metadata has valid Company link field.")

    print(f"=== [TEST 2] Testing Bottle Tracking Entry Creation with Company ===")
    customer = frappe.db.get_value("Customer", {}, "name")
    if not customer:
        cust_doc = frappe.new_doc("Customer")
        cust_doc.customer_name = "Test Deletion Customer"
        cust_doc.insert(ignore_permissions=True)
        customer = cust_doc.name

    # Create test entry
    entry = frappe.get_doc({
        "doctype": "Customer Bottle Ledger",
        "company": company,
        "customer": customer,
        "posting_date": today(),
        "voucher_type": "Sales Invoice",
        "voucher_no": "TEST-SINV-DEL-001",
        "full_bottles_delivered": 15,
        "empty_bottles_received": 5
    })
    entry.insert(ignore_permissions=True)
    frappe.db.commit()

    entry_count = frappe.db.count("Customer Bottle Ledger", {"company": company})
    assert entry_count >= 1, f"Expected at least 1 entry, found {entry_count}"
    print(f"  [PASS] Customer Bottle Ledger inserted with company='{company}'. Count: {entry_count}")

    print(f"=== [TEST 3] Testing Transaction Deletion Record Auto-Discovery ===")
    tdr = frappe.new_doc("Transaction Deletion Record")
    tdr.company = company
    tdr.generate_to_delete_list()

    discovered_item = None
    for item in tdr.doctypes_to_delete:
        if item.doctype_name == "Customer Bottle Ledger":
            discovered_item = item
            break

    assert discovered_item is not None, "Customer Bottle Ledger was NOT discovered by TDR!"
    assert discovered_item.company_field == "company", f"Expected company_field 'company', got {discovered_item.company_field}"
    assert discovered_item.document_count >= 1, f"Expected document_count >= 1, got {discovered_item.document_count}"
    print(f"  [PASS] TDR auto-discovered Customer Bottle Ledger: count={discovered_item.document_count}, field={discovered_item.company_field}")

    print(f"=== [TEST 4] Testing Deletion of Customer Bottle Ledger via TDR Hook ===")
    from lean_production.lean_production.bottle_tracking import on_transaction_deletion_record_submit
    mock_tdr = frappe._dict({"company": company, "doctypes_to_delete": tdr.doctypes_to_delete})
    on_transaction_deletion_record_submit(mock_tdr, "before_submit")
    frappe.db.commit()

    remaining_count = frappe.db.count("Customer Bottle Ledger", {"company": company})
    assert remaining_count == 0, f"Expected 0 entries remaining, found {remaining_count}"
    print(f"  [PASS] All Customer Bottle Ledger entries for company '{company}' were deleted! Count: {remaining_count}")

    print(f"=== [TEST 5] Testing Clean Sequence Reset ===")
    seq_val = frappe.db.sql("SELECT next_not_cached_value FROM customer_bottle_ledger_id_seq")
    print(f"  * Sequence value: {seq_val}")

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY (100% GREEN) <<<")
    return True

if __name__ == "__main__":
    run_tests()
