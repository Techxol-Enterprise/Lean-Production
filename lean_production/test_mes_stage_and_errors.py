# Copyright (c) 2026, Techxol and contributors
# Empirical Challenger Verification Suite for Lean Production MES (challenger_mes_2)
# Tests:
# 1. Multi-stage MES Entries: Water Purification & Blow Molding with good_qty, scrap_qty, and materials child table
# 2. Negative/Error Handling:
#    - QC Status Fail rejection on Water Purification
#    - Non-existent BOM rejection
#    - Unsubmitted / Draft BOM rejection (docstatus = 0)
#    - Inactive BOM rejection (is_active = 0)
#    - Missing source_warehouse rejection in materials child table
#    - Zero and negative good_qty rejection across all 3 entry types

import frappe
from frappe.utils import flt, today, nowtime
from lean_production.stock_automation import get_bom_material_details


def setup_environment():
    if not getattr(frappe.local, "site", None):
        frappe.init(site="Wateena", sites_path="sites")
        frappe.connect()
    frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 1)


def test_stage_1_water_purification_mes():
    print("--- Test 1A: Water Purification Entry MES Multi-Stage Support ---")
    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    stores_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"
    fg_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"

    item_code = "INT-BULK-WATER"
    bom_no = frappe.db.get_value("BOM", {"item": item_code, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active submitted BOM for {item_code} must exist"

    good_qty = 500.0
    scrap_qty = 25.0
    total_qty = good_qty + scrap_qty  # 525.0 L consumed

    wpe = frappe.get_doc({
        "doctype": "Water Purification Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "mineral_water_item": item_code,
        "bom_no": bom_no,
        "good_qty": good_qty,
        "scrap_qty": scrap_qty,
        "target_warehouse": fg_wh,
        "qc_status": "Pass",
        "batch_no": "BATCH-WP-CHALLENGE-002"
    })

    materials = get_bom_material_details(
        item_code=item_code,
        bom_no=bom_no,
        total_qty=total_qty,
        company=company
    )
    assert len(materials) == 5, f"Expected 5 BOM materials, got {len(materials)}"

    for m in materials:
        wpe.append("materials", {
            "item_code": m["item_code"],
            "required_qty": m["required_qty"],
            "uom": m["uom"],
            "source_warehouse": stores_wh,
            "available_stock": m["available_stock"]
        })

    wpe.insert(ignore_permissions=True)
    wpe.submit()

    stock_entry_id = wpe.stock_entry
    assert stock_entry_id, f"Water Purification Entry {wpe.name} must have linked Stock Entry"

    se = frappe.get_doc("Stock Entry", stock_entry_id)
    assert se.docstatus == 1, "Stock Entry must be submitted"
    assert se.purpose == "Manufacture", f"Purpose must be Manufacture, got {se.purpose}"
    assert se.from_bom == 1, "from_bom must be 1"
    assert flt(se.fg_completed_qty) == good_qty, f"fg_completed_qty must be {good_qty}, got {se.fg_completed_qty}"

    # Finished Good row
    fg_items = [d for d in se.items if d.is_finished_item]
    assert len(fg_items) == 1, f"Expected 1 FG row, got {len(fg_items)}"
    fg_row = fg_items[0]
    assert fg_row.item_code == item_code
    assert flt(fg_row.qty) == good_qty
    assert fg_row.t_warehouse == fg_wh

    # Consumed Raw Materials: 525L worth (630L raw water, 105g Ca, 52.5g Mg, 52.5g Na, 2.1g antiscale)
    rm_items = {d.item_code: d for d in se.items if not d.is_finished_item}
    expected_rm = {
        "RM-WATER": 630.0,
        "MIN-CALCIUM": 105.0,
        "MIN-MAGNESIUM": 52.5,
        "MIN-SODIUM": 52.5,
        "CHEM-ANTISCALE": 2.1
    }
    for r_item, r_qty in expected_rm.items():
        assert r_item in rm_items, f"{r_item} missing from SE"
        assert abs(flt(rm_items[r_item].qty) - r_qty) < 1e-4, f"{r_item} qty expected {r_qty}, got {rm_items[r_item].qty}"
        assert rm_items[r_item].s_warehouse == stores_wh

    # Valuation conservation
    assert flt(se.total_incoming_value) > 0
    assert flt(se.total_outgoing_value) > 0
    assert abs(flt(se.total_incoming_value) - flt(se.total_outgoing_value)) < 1e-4, "Imbalance in Water Purification valuation"
    assert abs(flt(se.value_difference)) < 1e-4

    # Remarks MES metadata
    assert "Good Qty: 500.0" in se.remarks or "Good Qty: 500" in se.remarks
    assert "Scrap Qty: 25.0" in se.remarks or "Scrap Qty: 25" in se.remarks
    assert "BATCH-WP-CHALLENGE-002" in se.remarks

    # Two-way cancellation
    wpe.cancel()
    se.reload()
    assert se.docstatus == 2, "Stock Entry must be cancelled when Water Purification Entry is cancelled"
    frappe.db.commit()
    print("Water Purification Entry MES Multi-Stage Support: PASS")


def test_stage_2_blow_molding_mes():
    print("--- Test 1B: Blow Molding Entry MES Multi-Stage Support ---")
    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    stores_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"

    item_code = "INT-BTL-0.5L"
    bom_no = frappe.db.get_value("BOM", {"item": item_code, "is_active": 1, "docstatus": 1}, "name")
    assert bom_no, f"Active submitted BOM for {item_code} must exist"

    good_qty = 1000.0
    scrap_qty = 50.0
    total_qty = good_qty + scrap_qty  # 1050.0 bottles worth of preforms consumed

    bme = frappe.get_doc({
        "doctype": "Blow Molding Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "bottle_item": item_code,
        "bom_no": bom_no,
        "good_qty": good_qty,
        "scrap_qty": scrap_qty,
        "target_warehouse": stores_wh,
        "batch_no": "BATCH-BM-CHALLENGE-002"
    })

    materials = get_bom_material_details(
        item_code=item_code,
        bom_no=bom_no,
        total_qty=total_qty,
        company=company
    )
    assert len(materials) == 1, f"Expected 1 BOM material, got {len(materials)}"

    for m in materials:
        bme.append("materials", {
            "item_code": m["item_code"],
            "required_qty": m["required_qty"],
            "uom": m["uom"],
            "source_warehouse": stores_wh,
            "available_stock": m["available_stock"]
        })

    bme.insert(ignore_permissions=True)
    bme.submit()

    stock_entry_id = bme.stock_entry
    assert stock_entry_id, f"Blow Molding Entry {bme.name} must have linked Stock Entry"

    se = frappe.get_doc("Stock Entry", stock_entry_id)
    assert se.docstatus == 1, "Stock Entry must be submitted"
    assert se.purpose == "Manufacture"
    assert se.from_bom == 1
    assert flt(se.fg_completed_qty) == good_qty

    fg_items = [d for d in se.items if d.is_finished_item]
    assert len(fg_items) == 1
    fg_row = fg_items[0]
    assert fg_row.item_code == item_code
    assert flt(fg_row.qty) == good_qty
    assert fg_row.t_warehouse == stores_wh

    # Consumed Preforms: 15 Kg per 1000 * 1050 = 15.75 Kg
    rm_items = {d.item_code: d for d in se.items if not d.is_finished_item}
    assert "RM-PREFORM-15G" in rm_items
    assert abs(flt(rm_items["RM-PREFORM-15G"].qty) - 15.75) < 1e-4

    # Value conservation
    assert flt(se.total_incoming_value) > 0
    assert abs(flt(se.total_incoming_value) - flt(se.total_outgoing_value)) < 1e-4
    assert abs(flt(se.value_difference)) < 1e-4

    # Remarks MES metadata
    assert "Good Qty: 1000.0" in se.remarks or "Good Qty: 1000" in se.remarks
    assert "Scrap Qty: 50.0" in se.remarks or "Scrap Qty: 50" in se.remarks
    assert "BATCH-BM-CHALLENGE-002" in se.remarks

    # Two-way cancellation
    bme.cancel()
    se.reload()
    assert se.docstatus == 2, "Stock Entry must be cancelled when Blow Molding Entry is cancelled"
    frappe.db.commit()
    print("Blow Molding Entry MES Multi-Stage Support: PASS")


def test_negative_qc_status_rejection():
    print("--- Test 2A: Negative Test - QC Status Rejection on Water Purification ---")
    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    stores_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"
    fg_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"
    bom_no = frappe.db.get_value("BOM", {"item": "INT-BULK-WATER", "is_active": 1, "docstatus": 1}, "name")

    wpe = frappe.get_doc({
        "doctype": "Water Purification Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "mineral_water_item": "INT-BULK-WATER",
        "bom_no": bom_no,
        "good_qty": 500.0,
        "scrap_qty": 0.0,
        "target_warehouse": fg_wh,
        "qc_status": "Fail"
    })
    wpe.insert(ignore_permissions=True)
    try:
        wpe.submit()
        assert False, "Expected ValidationError for qc_status = 'Fail', but submit succeeded!"
    except frappe.ValidationError as e:
        print("Correctly rejected Water Purification with qc_status='Fail'")
        frappe.db.rollback()

    print("QC Status Guard Rejection: PASS")


def test_negative_invalid_and_unsubmitted_bom():
    print("--- Test 2B: Negative Test - Invalid / Unsubmitted BOM Rejection ---")
    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    fg_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"

    # 1. Non-existent BOM
    fe_nonexistent = frappe.get_doc({
        "doctype": "Filling Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "finished_good_item": "FG-WATER-0.5L-12",
        "bom_no": "BOM-DOES-NOT-EXIST-404",
        "good_qty": 100.0,
        "fg_warehouse": fg_wh
    })
    try:
        fe_nonexistent.insert(ignore_permissions=True)
        fe_nonexistent.submit()
        assert False, "Expected ValidationError for non-existent BOM!"
    except (frappe.ValidationError, frappe.LinkValidationError) as e:
        print(f"Correctly rejected non-existent BOM: {type(e).__name__}")
        frappe.db.rollback()

    # 2. Draft / Unsubmitted BOM (docstatus = 0)
    draft_bom = frappe.new_doc("BOM")
    draft_bom.item = "FG-WATER-0.5L-12"
    draft_bom.quantity = 1.0
    draft_bom.is_active = 1
    draft_bom.is_default = 0
    draft_bom.append("items", {"item_code": "RM-WRAP-12X", "qty": 1.0, "uom": "Unit"})
    draft_bom.insert(ignore_permissions=True)
    assert draft_bom.docstatus == 0, "Draft BOM must have docstatus=0"

    fe_draft = frappe.get_doc({
        "doctype": "Filling Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "finished_good_item": "FG-WATER-0.5L-12",
        "bom_no": draft_bom.name,
        "good_qty": 10.0,
        "fg_warehouse": fg_wh
    })
    fe_draft.insert(ignore_permissions=True)
    try:
        fe_draft.submit()
        assert False, "Expected ValidationError for draft/unsubmitted BOM!"
    except frappe.ValidationError as e:
        print(f"Correctly rejected unsubmitted/draft BOM: {type(e).__name__}")
        frappe.db.rollback()

    # 3. Inactive BOM (is_active = 0)
    inactive_bom = frappe.new_doc("BOM")
    inactive_bom.item = "FG-WATER-0.5L-12"
    inactive_bom.quantity = 1.0
    inactive_bom.is_active = 0
    inactive_bom.is_default = 0
    inactive_bom.append("items", {"item_code": "RM-WRAP-12X", "qty": 1.0, "uom": "Unit"})
    inactive_bom.insert(ignore_permissions=True)
    inactive_bom.submit()
    assert inactive_bom.docstatus == 1 and inactive_bom.is_active == 0

    fe_inactive = frappe.get_doc({
        "doctype": "Filling Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "finished_good_item": "FG-WATER-0.5L-12",
        "bom_no": inactive_bom.name,
        "good_qty": 10.0,
        "fg_warehouse": fg_wh
    })
    fe_inactive.insert(ignore_permissions=True)
    try:
        fe_inactive.submit()
        assert False, "Expected ValidationError for inactive BOM!"
    except frappe.ValidationError as e:
        print(f"Correctly rejected inactive BOM: {type(e).__name__}")
        frappe.db.rollback()

    # Clean up test BOMs
    if frappe.db.exists("BOM", inactive_bom.name):
        doc_inact = frappe.get_doc("BOM", inactive_bom.name)
        if doc_inact.docstatus == 1:
            doc_inact.cancel()
        frappe.delete_doc("BOM", inactive_bom.name, force=True)
    if frappe.db.exists("BOM", draft_bom.name):
        frappe.delete_doc("BOM", draft_bom.name, force=True)

    frappe.db.commit()
    print("Invalid / Unsubmitted BOM Rejection: PASS")


def test_negative_missing_warehouse_and_bad_qty():
    print("--- Test 2C: Negative Test - Missing Child Warehouse & Non-Positive Qty ---")
    company = frappe.db.get_single_value("Global Defaults", "default_company") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    stores_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"
    fg_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"
    bom_no = frappe.db.get_value("BOM", {"item": "FG-WATER-0.5L-12", "is_active": 1, "docstatus": 1}, "name")

    # 1. Missing source_warehouse in child table row (rejected on insert as mandatory)
    fe_no_wh = frappe.get_doc({
        "doctype": "Filling Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "finished_good_item": "FG-WATER-0.5L-12",
        "bom_no": bom_no,
        "good_qty": 10.0,
        "fg_warehouse": fg_wh
    })
    fe_no_wh.append("materials", {
        "item_code": "RM-WRAP-12X",
        "required_qty": 10.0,
        "uom": "Unit",
        "source_warehouse": None,
        "available_stock": 100.0
    })
    try:
        fe_no_wh.insert(ignore_permissions=True)
        fe_no_wh.submit()
        assert False, "Expected MandatoryError/ValidationError for missing source_warehouse in child table!"
    except (frappe.ValidationError, frappe.MandatoryError) as e:
        print(f"Correctly rejected missing child table source_warehouse: {type(e).__name__}")
        frappe.db.rollback()

    # 2. Zero / Negative Good Qty across all 3 entry types
    # Water Purification zero qty
    wpe_zero = frappe.get_doc({
        "doctype": "Water Purification Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "mineral_water_item": "INT-BULK-WATER",
        "bom_no": frappe.db.get_value("BOM", {"item": "INT-BULK-WATER", "is_active": 1, "docstatus": 1}, "name"),
        "good_qty": 0.0,
        "litres_purified": 0.0,
        "target_warehouse": fg_wh,
        "qc_status": "Pass"
    })
    wpe_zero.insert(ignore_permissions=True)
    try:
        wpe_zero.submit()
        assert False, "Expected ValidationError for zero good_qty in Water Purification!"
    except frappe.ValidationError:
        print("Correctly rejected zero good_qty in Water Purification Entry")
        frappe.db.rollback()

    # Blow Molding negative qty
    bme_neg = frappe.get_doc({
        "doctype": "Blow Molding Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "bottle_item": "INT-BTL-0.5L",
        "bom_no": frappe.db.get_value("BOM", {"item": "INT-BTL-0.5L", "is_active": 1, "docstatus": 1}, "name"),
        "good_qty": -10.0,
        "bottles_produced_qty": -10.0,
        "target_warehouse": stores_wh
    })
    bme_neg.insert(ignore_permissions=True)
    try:
        bme_neg.submit()
        assert False, "Expected ValidationError for negative good_qty in Blow Molding!"
    except frappe.ValidationError:
        print("Correctly rejected negative good_qty in Blow Molding Entry")
        frappe.db.rollback()

    # Filling Entry zero qty
    fe_bad_qty = frappe.get_doc({
        "doctype": "Filling Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "finished_good_item": "FG-WATER-0.5L-12",
        "bom_no": bom_no,
        "good_qty": 0.0,
        "cartons_produced": 0.0,
        "fg_warehouse": fg_wh
    })
    fe_bad_qty.insert(ignore_permissions=True)
    try:
        fe_bad_qty.submit()
        assert False, "Expected ValidationError for zero good_qty in Filling Entry!"
    except frappe.ValidationError:
        print("Correctly rejected zero good_qty in Filling Entry")
        frappe.db.rollback()

    frappe.db.commit()
    print("Missing Child Warehouse & Non-Positive Qty: PASS")


def run_stage_and_negative_suite():
    setup_environment()
    test_stage_1_water_purification_mes()
    test_stage_2_blow_molding_mes()
    test_negative_qc_status_rejection()
    test_negative_invalid_and_unsubmitted_bom()
    test_negative_missing_warehouse_and_bad_qty()
    print("=============================================================")
    print("ALL MULTI-STAGE MES & NEGATIVE ERROR HANDLING TESTS PASSED!")
    print("=============================================================")
    return "PASS"


if __name__ == "__main__":
    run_stage_and_negative_suite()
