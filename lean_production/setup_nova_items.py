# Copyright (c) 2026, Techxol and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt

def run():
    print("Starting Nova Beverages Item Master configuration...")

    # 1. Ensure Item Groups exist
    item_groups = [
        {"name": "Raw Water", "parent": "Raw Material"},
        {"name": "Chemicals & Minerals", "parent": "Raw Material"},
        {"name": "Packaging Materials", "parent": "Raw Material"},
        {"name": "Resins & Preforms", "parent": "Raw Material"},
        {"name": "Bulk Purified Water", "parent": "All Item Groups"},
        {"name": "Empty Bottles", "parent": "All Item Groups"},
        {"name": "Finished Goods", "parent": "All Item Groups"},
        {"name": "Services", "parent": "All Item Groups"},
    ]

    for ig in item_groups:
        if not frappe.db.exists("Item Group", ig["name"]):
            parent = ig["parent"] if frappe.db.exists("Item Group", ig["parent"]) else "All Item Groups"
            doc = frappe.new_doc("Item Group")
            doc.item_group_name = ig["name"]
            doc.parent_item_group = parent
            doc.is_group = 0
            doc.insert(ignore_permissions=True)
            print(f"Created Item Group: {ig['name']}")

    # 2. Ensure required UOMs exist
    required_uoms = ["Litre", "Gram", "Kg", "Nos", "Unit", "Pack"]
    for uom in required_uoms:
        if not frappe.db.exists("UOM", uom):
            u = frappe.new_doc("UOM")
            u.uom_name = uom
            u.must_be_whole_number = 1 if uom in ["Nos", "Unit", "Pack"] else 0
            u.insert(ignore_permissions=True)
            print(f"Created UOM: {uom}")

    # 3. Master Items Definition
    items_to_create = [
        # Upstream Raw Materials & Packaging
        {"code": "RM-WATER", "name": "Raw Untreated Water", "group": "Raw Water", "uom": "Litre", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "MIN-CALCIUM", "name": "Calcium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "MIN-MAGNESIUM", "name": "Magnesium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "MIN-SODIUM", "name": "Sodium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "CHEM-ANTISCALE", "name": "RO Antiscalant Liquid", "group": "Chemicals & Minerals", "uom": "Litre", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BULK-WATER", "name": "Purified Mineral Water (Bulk)", "group": "Bulk Purified Water", "uom": "Litre", "stock": 1, "purchase": 0, "sales": 0, "valuation_rate": 0.50},
        {"code": "RM-CAP-28MM", "name": "28mm Standard Plastic Cap", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-WRAP-12X", "name": "Shrink Wrap Film (12-pack)", "group": "Packaging Materials", "uom": "Unit", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-WRAP-06X", "name": "Shrink Wrap Film (6-pack)", "group": "Packaging Materials", "uom": "Unit", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "19L-BOTTLE-DEPOSIT", "name": "19L Bottle Security Deposit", "group": "Services", "uom": "Nos", "stock": 0, "purchase": 1, "sales": 1},

        # Raw Preforms - Pure (Stock UOM: Nos)
        {"code": "RM-PREFORM-PURE-13.5G", "name": "PET Preform - 13.5g Pure", "group": "Resins & Preforms", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-PREFORM-PURE-15G", "name": "PET Preform - 15g Pure", "group": "Resins & Preforms", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-PREFORM-PURE-27G", "name": "PET Preform - 27g Pure", "group": "Resins & Preforms", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-PREFORM-PURE-30G", "name": "PET Preform - 30g Pure", "group": "Resins & Preforms", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},

        # Raw Preforms - Mix (Stock UOM: Nos)
        {"code": "RM-PREFORM-MIX-13.5G", "name": "PET Preform - 13.5g Mix", "group": "Resins & Preforms", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-PREFORM-MIX-15G", "name": "PET Preform - 15g Mix", "group": "Resins & Preforms", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-PREFORM-MIX-27G", "name": "PET Preform - 27g Mix", "group": "Resins & Preforms", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-PREFORM-MIX-30G", "name": "PET Preform - 30g Mix", "group": "Resins & Preforms", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},

        # Labels
        {"code": "RM-LBL-REH-0.5L", "name": "Nova Beverages - Rehydrate Label - 500ml", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-LBL-REH-1.5L", "name": "Nova Beverages - Rehydrate Label - 1.5L", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-LBL-HYD-0.5L", "name": "Nova Beverages - Hydrafina Label - 500ml", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-LBL-HYD-1.5L", "name": "Nova Beverages - Hydrafina Label - 1.5L", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-LBL-REH-19L", "name": "Nova Beverages - Rehydrate Label - 19L", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},

        # 19L Dedicated Packaging Components
        {"code": "RM-CAP-55MM", "name": "55mm Non-Spill Cap (19L)", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-SEAL-19L", "name": "Heat Shrink Neck Seal - 19L", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-BAG-19L", "name": "Protective Dust Bag - 19L", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},

        # Empty Bottles - Rehydrate
        {"code": "INT-BTL-REH-0.5L-13.5G", "name": "Empty PET Bottle - Nova Rehydrate - 500ml (13.5g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-REH-0.5L-15G", "name": "Empty PET Bottle - Nova Rehydrate - 500ml (15g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-REH-1.5L-27G", "name": "Empty PET Bottle - Nova Rehydrate - 1.5L (27g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-REH-1.5L-30G", "name": "Empty PET Bottle - Nova Rehydrate - 1.5L (30g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},

        # Empty Bottles - Hydrafina Pure
        {"code": "INT-BTL-HYD-PURE-0.5L-13.5G", "name": "Empty PET Bottle - Nova Hydrafina Pure - 500ml (13.5g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-HYD-PURE-0.5L-15G", "name": "Empty PET Bottle - Nova Hydrafina Pure - 500ml (15g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-HYD-PURE-1.5L-27G", "name": "Empty PET Bottle - Nova Hydrafina Pure - 1.5L (27g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-HYD-PURE-1.5L-30G", "name": "Empty PET Bottle - Nova Hydrafina Pure - 1.5L (30g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},

        # Empty Bottles - Hydrafina Mix
        {"code": "INT-BTL-HYD-MIX-0.5L-13.5G", "name": "Empty PET Bottle - Nova Hydrafina Mix - 500ml (13.5g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-HYD-MIX-0.5L-15G", "name": "Empty PET Bottle - Nova Hydrafina Mix - 500ml (15g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-HYD-MIX-1.5L-27G", "name": "Empty PET Bottle - Nova Hydrafina Mix - 1.5L (27g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BTL-HYD-MIX-1.5L-30G", "name": "Empty PET Bottle - Nova Hydrafina Mix - 1.5L (30g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},

        # Finished Goods - Rehydrate
        {"code": "FG-REH-WATER-0.5L-12-13.5G", "name": "Nova Beverages - Rehydrate Water - PL - 500ml x 12 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-REH-WATER-0.5L-12-15G", "name": "Nova Beverages - Rehydrate Water - PH - 500ml x 12 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-REH-WATER-1.5L-06-27G", "name": "Nova Beverages - Rehydrate Water - PL - 1.5L x 6 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-REH-WATER-1.5L-06-30G", "name": "Nova Beverages - Rehydrate Water - PH - 1.5L x 6 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-REH-19L-REFILL", "name": "Nova Beverages - Rehydrate 19L (Refill)", "group": "Finished Goods", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 1},

        # Finished Goods - Hydrafina Pure
        {"code": "FG-HYD-WATER-PURE-0.5L-12-13.5G", "name": "Nova Beverages - Hydrafina Water - PL - 500ml x 12 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-HYD-WATER-PURE-0.5L-12-15G", "name": "Nova Beverages - Hydrafina Water - PH - 500ml x 12 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-HYD-WATER-PURE-1.5L-06-27G", "name": "Nova Beverages - Hydrafina Water - PL - 1.5L x 6 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-HYD-WATER-PURE-1.5L-06-30G", "name": "Nova Beverages - Hydrafina Water - PH - 1.5L x 6 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},

        # Finished Goods - Hydrafina Mix
        {"code": "FG-HYD-WATER-MIX-0.5L-12-13.5G", "name": "Nova Beverages - Hydrafina Water - ML - 500ml x 12 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-HYD-WATER-MIX-0.5L-12-15G", "name": "Nova Beverages - Hydrafina Water - MH - 500ml x 12 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-HYD-WATER-MIX-1.5L-06-27G", "name": "Nova Beverages - Hydrafina Water - ML - 1.5L x 6 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-HYD-WATER-MIX-1.5L-06-30G", "name": "Nova Beverages - Hydrafina Water - MH - 1.5L x 6 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
    ]

    for item_data in items_to_create:
        code = item_data["code"]
        if frappe.db.exists("Item", code):
            doc = frappe.get_doc("Item", code)
            doc.item_name = item_data["name"]
            doc.item_group = item_data["group"]
            doc.stock_uom = item_data["uom"]
            doc.is_stock_item = item_data["stock"]
            doc.is_purchase_item = item_data["purchase"]
            doc.is_sales_item = item_data["sales"]
            if "valuation_rate" in item_data and flt(doc.valuation_rate) <= 0:
                doc.valuation_rate = item_data["valuation_rate"]
            doc.save(ignore_permissions=True)
            print(f"Updated Item: {code}")
        else:
            doc = frappe.new_doc("Item")
            doc.item_code = code
            doc.item_name = item_data["name"]
            doc.item_group = item_data["group"]
            doc.stock_uom = item_data["uom"]
            doc.is_stock_item = item_data["stock"]
            doc.is_purchase_item = item_data["purchase"]
            doc.is_sales_item = item_data["sales"]
            doc.valuation_rate = item_data.get("valuation_rate", 0.0)

            if "conversions" in item_data:
                for uom_name, factor in item_data["conversions"]:
                    doc.append("uoms", {"uom": uom_name, "conversion_factor": factor})

            doc.insert(ignore_permissions=True)
            print(f"Created Item: {code}")

    frappe.db.commit()
    print("All 47 Nova Beverages items successfully configured!")
