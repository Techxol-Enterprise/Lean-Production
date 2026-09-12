import frappe
from frappe.utils import flt, today, nowtime

def run_test():
    """
    Automated verification script for lean_production dry-weight chemical & mineral consumption.
    Programmatically creates a Water Purification Entry for 500L, verifies background Stock Entry
    generation, and asserts that the 4 minerals (MIN-SODIUM, MIN-MAGNESIUM, MIN-CALCIUM, CHEM-ANTISCALE)
    are successfully consumed in dry weights (Kg or Gram), printing PASS to the console.
    """
    if not getattr(frappe.local, "site", None):
        frappe.init(site="Wateena", sites_path="sites")
        frappe.connect()

    # Ensure Stock Settings allows negative stock for automated tests
    frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 1)

    company = frappe.db.get_single_value("Global Defaults", "default_company") or frappe.db.get_value("Company", {}, "name") or "Wateena"
    abbr = frappe.db.get_value("Company", company, "abbr") or "W"
    source_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Stores"}, "name") or f"Stores - {abbr}"
    target_wh = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": "Finished Goods"}, "name") or f"Finished Goods - {abbr}"
    mineral_item = "INT-BULK-WATER"

    # Get active BOM for INT-BULK-WATER
    bom_no = frappe.db.get_value("BOM", {"item": mineral_item, "is_active": 1, "docstatus": 1}, "name")
    if not bom_no:
        from lean_production.seed_master_data import main as seed_main
        seed_main()
        bom_no = frappe.db.get_value("BOM", {"item": mineral_item, "is_active": 1, "docstatus": 1}, "name")

    assert bom_no, f"Active submitted BOM for {mineral_item} must exist"

    # Programmatically create a Water Purification Entry for 500L
    wpe = frappe.get_doc({
        "doctype": "Water Purification Entry",
        "company": company,
        "posting_date": today(),
        "shift": "Morning",
        "mineral_water_item": mineral_item,
        "bom_no": bom_no,
        "litres_purified": 500.0,
        "source_warehouse": source_wh,
        "target_warehouse": target_wh,
        "qc_status": "Pass"
    })
    wpe.insert(ignore_permissions=True)
    wpe.submit()

    stock_entry_id = wpe.stock_entry or frappe.db.get_value("Water Purification Entry", wpe.name, "stock_entry")
    assert stock_entry_id, f"Water Purification Entry {wpe.name} must have a linked Stock Entry"

    se = frappe.get_doc("Stock Entry", stock_entry_id)
    assert se.docstatus == 1, f"Linked Stock Entry {se.name} must be submitted (docstatus=1)"
    assert se.purpose == "Manufacture", f"Stock Entry purpose must be Manufacture, got {se.purpose}"

    # Verify the 4 minerals consumption
    target_minerals = ["MIN-SODIUM", "MIN-MAGNESIUM", "MIN-CALCIUM", "CHEM-ANTISCALE"]
    consumed_items = {d.item_code: d for d in se.items if not d.is_finished_item}

    for mineral in target_minerals:
        assert mineral in consumed_items, f"Mineral {mineral} was not consumed in Stock Entry {se.name}"
        item_row = consumed_items[mineral]
        
        # Assert UOM is dry weight (Kg or Gram) and NOT fractional Litre
        assert item_row.uom in ["Kg", "Gram"], (
            f"Mineral {mineral} consumed UOM must be 'Kg' or 'Gram', got '{item_row.uom}'"
        )
        assert item_row.uom != "Litre", f"Mineral {mineral} must NOT be consumed in Litres"
        
        assert item_row.stock_uom in ["Kg", "Gram"], (
            f"Mineral {mineral} stock_uom must be 'Kg' or 'Gram', got '{item_row.stock_uom}'"
        )
        assert item_row.stock_uom != "Litre", f"Mineral {mineral} stock_uom must NOT be Litre"

        assert flt(item_row.qty) > 0, f"Consumed quantity for {mineral} must be positive, got {item_row.qty}"
        assert flt(item_row.transfer_qty) > 0, (
            f"Transfer quantity for {mineral} must be positive, got {item_row.transfer_qty}"
        )

    # Verify finished good item
    fg_items = [d for d in se.items if d.is_finished_item]
    assert len(fg_items) == 1, f"Stock Entry must have exactly 1 finished item row, found {len(fg_items)}"
    fg_row = fg_items[0]
    assert fg_row.item_code == mineral_item, f"Finished item must be {mineral_item}, got {fg_row.item_code}"
    assert flt(fg_row.qty) == 500.0, f"Finished item qty must be 500.0, got {fg_row.qty}"

    # Assert accurate cost absorption and valuation (preventing zero valuation loss)
    assert flt(fg_row.basic_rate) > 0, f"Finished item basic_rate must be positive, got {fg_row.basic_rate}"
    assert flt(fg_row.valuation_rate) > 0, f"Finished item valuation_rate must be positive, got {fg_row.valuation_rate}"
    assert flt(se.total_incoming_value) > 0, f"Total incoming value must be positive, got {se.total_incoming_value}"
    assert flt(se.total_outgoing_value) > 0, f"Total outgoing value must be positive, got {se.total_outgoing_value}"
    assert abs(flt(se.total_incoming_value) - flt(se.total_outgoing_value)) < 1e-4, (
        f"Incoming value ({se.total_incoming_value}) must match outgoing value ({se.total_outgoing_value})"
    )
    assert abs(flt(se.value_difference)) < 1e-4, f"Value difference must be 0, got {se.value_difference}"

    # Verify BOM link and FG completed qty retention
    assert se.from_bom == 1, f"Stock Entry {se.name} must have from_bom=1, got {se.from_bom}"
    assert flt(se.fg_completed_qty) == 500.0, (
        f"Stock Entry {se.name} fg_completed_qty must be 500.0, got {se.fg_completed_qty}"
    )

    frappe.db.commit()
    print("PASS")
    return "PASS"

def main():
    return run_test()

if __name__ == "__main__":
    run_test()
