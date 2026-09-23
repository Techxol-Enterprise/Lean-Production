# Copyright (c) 2026, Techxol and contributors
# For license information, please see license.txt

import frappe

def run():
    print("Starting Nova Beverages BOM configuration across Stages 1, 2, and 3...")

    boms_config = [
        # --- Stage 1: Water Purification (Shared) ---
        {
            "item": "INT-BULK-WATER",
            "quantity": 1000.0,
            "uom": "Litre",
            "items": [
                {"item_code": "RM-WATER", "qty": 1000.0, "uom": "Litre"},
                {"item_code": "MIN-CALCIUM", "qty": 150.0, "uom": "Gram"},
                {"item_code": "MIN-MAGNESIUM", "qty": 30.0, "uom": "Gram"},
                {"item_code": "MIN-SODIUM", "qty": 25.0, "uom": "Gram"},
                {"item_code": "CHEM-ANTISCALE", "qty": 0.040, "uom": "Litre"},
            ]
        },

        # --- Stage 2A: Rehydrate Blow Molding (Pure PET) ---
        {
            "item": "INT-BTL-REH-0.5L-13.5G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-PURE-13.5G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-REH-0.5L-15G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-PURE-15G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-REH-1.5L-27G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-PURE-27G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-REH-1.5L-30G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-PURE-30G", "qty": 1000.0, "uom": "Nos"}]
        },

        # --- Stage 2B: Hydrafina Pure Blow Molding (Pure PET) ---
        {
            "item": "INT-BTL-HYD-PURE-0.5L-13.5G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-PURE-13.5G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-HYD-PURE-0.5L-15G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-PURE-15G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-HYD-PURE-1.5L-27G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-PURE-27G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-HYD-PURE-1.5L-30G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-PURE-30G", "qty": 1000.0, "uom": "Nos"}]
        },

        # --- Stage 2C: Hydrafina Mix Blow Molding (Mix PET) ---
        {
            "item": "INT-BTL-HYD-MIX-0.5L-13.5G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-MIX-13.5G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-HYD-MIX-0.5L-15G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-MIX-15G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-HYD-MIX-1.5L-27G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-MIX-27G", "qty": 1000.0, "uom": "Nos"}]
        },
        {
            "item": "INT-BTL-HYD-MIX-1.5L-30G",
            "quantity": 1000.0,
            "uom": "Nos",
            "items": [{"item_code": "RM-PREFORM-MIX-30G", "qty": 1000.0, "uom": "Nos"}]
        },

        # --- Stage 3A: Rehydrate Finished Goods Filling Lines ---
        {
            "item": "FG-REH-WATER-0.5L-12-13.5G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 6.0, "uom": "Litre"},
                {"item_code": "INT-BTL-REH-0.5L-13.5G", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-LBL-REH-0.5L", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-12X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-REH-WATER-0.5L-12-15G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 6.0, "uom": "Litre"},
                {"item_code": "INT-BTL-REH-0.5L-15G", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-LBL-REH-0.5L", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-12X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-REH-WATER-1.5L-06-27G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 9.0, "uom": "Litre"},
                {"item_code": "INT-BTL-REH-1.5L-27G", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-LBL-REH-1.5L", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-06X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-REH-WATER-1.5L-06-30G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 9.0, "uom": "Litre"},
                {"item_code": "INT-BTL-REH-1.5L-30G", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-LBL-REH-1.5L", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-06X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-REH-19L-REFILL",
            "quantity": 1.0,
            "uom": "Nos",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 19.0, "uom": "Litre"},
                {"item_code": "RM-CAP-55MM", "qty": 1.0, "uom": "Nos"},
                {"item_code": "RM-SEAL-19L", "qty": 1.0, "uom": "Nos"},
                {"item_code": "RM-BAG-19L", "qty": 1.0, "uom": "Nos"},
                {"item_code": "RM-LBL-REH-19L", "qty": 1.0, "uom": "Nos"},
            ]
        },

        # --- Stage 3B: Hydrafina Pure Finished Goods Lines ---
        {
            "item": "FG-HYD-WATER-PURE-0.5L-12-13.5G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 6.0, "uom": "Litre"},
                {"item_code": "INT-BTL-HYD-PURE-0.5L-13.5G", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-LBL-HYD-0.5L", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-12X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-HYD-WATER-PURE-0.5L-12-15G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 6.0, "uom": "Litre"},
                {"item_code": "INT-BTL-HYD-PURE-0.5L-15G", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-LBL-HYD-0.5L", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-12X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-HYD-WATER-PURE-1.5L-06-27G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 9.0, "uom": "Litre"},
                {"item_code": "INT-BTL-HYD-PURE-1.5L-27G", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-LBL-HYD-1.5L", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-06X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-HYD-WATER-PURE-1.5L-06-30G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 9.0, "uom": "Litre"},
                {"item_code": "INT-BTL-HYD-PURE-1.5L-30G", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-LBL-HYD-1.5L", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-06X", "qty": 1.0, "uom": "Unit"},
            ]
        },

        # --- Stage 3C: Hydrafina Mix Economy Finished Goods Lines ---
        {
            "item": "FG-HYD-WATER-MIX-0.5L-12-13.5G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 6.0, "uom": "Litre"},
                {"item_code": "INT-BTL-HYD-MIX-0.5L-13.5G", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-LBL-HYD-0.5L", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-12X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-HYD-WATER-MIX-0.5L-12-15G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 6.0, "uom": "Litre"},
                {"item_code": "INT-BTL-HYD-MIX-0.5L-15G", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-LBL-HYD-0.5L", "qty": 12.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-12X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-HYD-WATER-MIX-1.5L-06-27G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 9.0, "uom": "Litre"},
                {"item_code": "INT-BTL-HYD-MIX-1.5L-27G", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-LBL-HYD-1.5L", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-06X", "qty": 1.0, "uom": "Unit"},
            ]
        },
        {
            "item": "FG-HYD-WATER-MIX-1.5L-06-30G",
            "quantity": 1.0,
            "uom": "Pack",
            "items": [
                {"item_code": "INT-BULK-WATER", "qty": 9.0, "uom": "Litre"},
                {"item_code": "INT-BTL-HYD-MIX-1.5L-30G", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-CAP-28MM", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-LBL-HYD-1.5L", "qty": 6.0, "uom": "Nos"},
                {"item_code": "RM-WRAP-06X", "qty": 1.0, "uom": "Unit"},
            ]
        },
    ]

    for cfg in boms_config:
        item_code = cfg["item"]

        # Check existing active BOMs
        existing_boms = frappe.get_all("BOM", filters={"item": item_code, "docstatus": 1})
        is_up_to_date = False

        if existing_boms:
            for eb in existing_boms:
                bdoc = frappe.get_doc("BOM", eb.name)
                # Check if components match
                current_items = {d.item_code: (round(float(d.qty), 4), d.uom) for d in bdoc.items}
                target_items = {c["item_code"]: (round(float(c["qty"]), 4), c["uom"]) for c in cfg["items"]}

                if current_items == target_items and round(float(bdoc.quantity), 4) == round(float(cfg["quantity"]), 4):
                    is_up_to_date = True
                    frappe.db.set_value("BOM", bdoc.name, {"is_default": 1, "is_active": 1})
                    frappe.db.set_value("Item", item_code, "default_bom", bdoc.name)
                    print(f"BOM {bdoc.name} for {item_code} is already up to date.")
                else:
                    # Cancel and delete outdated BOM cleanly (no transactions exist)
                    print(f"BOM {bdoc.name} for {item_code} is outdated. Cancelling and deleting...")
                    if bdoc.docstatus == 1:
                        bdoc.cancel()
                    frappe.delete_doc("BOM", bdoc.name, force=True)

        if is_up_to_date:
            continue

        # Create clean canonical BOM
        doc = frappe.new_doc("BOM")
        doc.item = item_code
        doc.quantity = cfg["quantity"]
        doc.uom = cfg["uom"]
        doc.is_active = 1
        doc.is_default = 1
        doc.with_operations = 0
        doc.rm_cost_as_per = "Valuation Rate"

        for comp in cfg["items"]:
            comp_doc = frappe.get_doc("Item", comp["item_code"])
            doc.append("items", {
                "item_code": comp["item_code"],
                "qty": comp["qty"],
                "uom": comp["uom"],
                "stock_uom": comp_doc.stock_uom,
                "rate": 0.0,
                "amount": 0.0
            })

        doc.insert(ignore_permissions=True)
        doc.submit()

        # Set as default on Item Master
        frappe.db.set_value("Item", item_code, "default_bom", doc.name)
        print(f"Created and activated clean BOM {doc.name} for {item_code}")

    # Ensure all rates in BOMs are clean 0.00 until purchases are booked
    frappe.db.sql("UPDATE `tabBOM Item` SET rate=0.0, amount=0.0, base_rate=0.0, base_amount=0.0")
    frappe.db.sql("UPDATE `tabBOM` SET raw_material_cost=0.0, total_cost=0.0, base_raw_material_cost=0.0, base_total_cost=0.0, rm_cost_as_per='Valuation Rate'")

    frappe.db.commit()
    print("All 26 Nova Beverages BOMs successfully configured on production!")
