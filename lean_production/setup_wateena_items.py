import frappe

def run():
    print("Beginning Wateena Item Master Setup (21 Items)...")

    # 1. Ensure required Item Groups exist
    item_groups = [
        "Raw Water",
        "Resins & Preforms",
        "Packaging Materials",
        "Chemicals & Minerals",
        "Bulk Purified Water",
        "Empty Bottles",
        "Finished Goods",
        "Services"
    ]
    for group_name in item_groups:
        if not frappe.db.exists("Item Group", group_name):
            ig = frappe.new_doc("Item Group")
            ig.item_group_name = group_name
            ig.parent_item_group = "All Item Groups"
            ig.is_group = 0
            ig.insert(ignore_permissions=True)
            print(f"Created Item Group: {group_name}")

    # 2. Ensure required UOMs exist
    required_uoms = ["Litre", "Gram", "Kg", "Nos", "Unit", "Pack"]
    for uom in required_uoms:
        if not frappe.db.exists("UOM", uom):
            u = frappe.new_doc("UOM")
            u.uom_name = uom
            u.must_be_whole_number = 1 if uom in ["Nos", "Unit", "Pack"] else 0
            u.insert(ignore_permissions=True)
            print(f"Created UOM: {uom}")

    # 3. Master Items Definition (21 Total Items)
    items_to_create = [
        # Upstream Raw Materials & Bulk Water
        {"code": "RM-WATER", "name": "Raw Untreated Water", "group": "Raw Water", "uom": "Litre", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "MIN-CALCIUM", "name": "Calcium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "MIN-MAGNESIUM", "name": "Magnesium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "MIN-SODIUM", "name": "Sodium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "CHEM-ANTISCALE", "name": "RO Antiscalant Liquid", "group": "Chemicals & Minerals", "uom": "Litre", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BULK-WATER", "name": "Purified Mineral Water (Bulk)", "group": "Bulk Purified Water", "uom": "Litre", "stock": 1, "purchase": 0, "sales": 0},

        # Resins & Preforms
        {"code": "RM-PREFORM-15G", "name": "PET Preform - 15g (for 500ml)", "group": "Resins & Preforms", "uom": "Kg", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-PREFORM-30G", "name": "PET Preform - 30g (for 1.5L)", "group": "Resins & Preforms", "uom": "Kg", "stock": 1, "purchase": 1, "sales": 0},

        # Packaging Materials - General
        {"code": "RM-CAP-28MM", "name": "28mm Standard Plastic Cap", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-LBL-0.5L", "name": "Shrink Label - 500ml", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-LBL-1.5L", "name": "Shrink Label - 1.5L", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-WRAP-12X", "name": "Shrink Wrap Film (12-pack)", "group": "Packaging Materials", "uom": "Unit", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-WRAP-06X", "name": "Shrink Wrap Film (6-pack)", "group": "Packaging Materials", "uom": "Unit", "stock": 1, "purchase": 1, "sales": 0},

        # 19L Packaging Materials
        {"code": "RM-CAP-55MM", "name": "55mm Non-Spill Cap (19L)", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "RM-SEAL-19L", "name": "Heat Shrink Neck Seal - 19L", "group": "Packaging Materials", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 0},

        # Empty Bottles
        {"code": "INT-BTL-0.5L", "name": "Empty PET Bottle - 500ml", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-1.5L", "name": "Empty PET Bottle - 1.5L", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},

        # Finished Goods
        {"code": "FG-WATER-0.5L-12", "name": "Wateena Water - 500ml x 12 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-WATER-1.5L-06", "name": "Wateena Water - 1.5L x 6 Pack", "group": "Finished Goods", "uom": "Pack", "stock": 1, "purchase": 0, "sales": 1},
        {"code": "FG-19L-REFILL", "name": "Wateena 19L (Refill)", "group": "Finished Goods", "uom": "Nos", "stock": 1, "purchase": 1, "sales": 1},

        # Services & Deposits
        {"code": "19L-BOTTLE-DEPOSIT", "name": "19L Bottle Security Deposit", "group": "Services", "uom": "Nos", "stock": 0, "purchase": 1, "sales": 1},
    ]

    for item in items_to_create:
        code = item["code"]
        if not frappe.db.exists("Item", code):
            doc = frappe.new_doc("Item")
            doc.item_code = code
            doc.item_name = item["name"]
            doc.item_group = item["group"]
            doc.stock_uom = item["uom"]
            doc.is_stock_item = item["stock"]
            doc.is_purchase_item = item["purchase"]
            doc.is_sales_item = item["sales"]
            doc.valuation_rate = 0.0

            if "conversions" in item:
                for conv_uom, factor in item["conversions"]:
                    doc.append("uoms", {
                        "uom": conv_uom,
                        "conversion_factor": factor
                    })

            doc.insert(ignore_permissions=True)
            print(f"Created Item: {code} ({item['name']})")
        else:
            doc = frappe.get_doc("Item", code)
            modified = False
            if doc.item_name != item["name"]:
                doc.item_name = item["name"]
                modified = True
            if doc.item_group != item["group"]:
                doc.item_group = item["group"]
                modified = True
            if doc.stock_uom != item["uom"]:
                doc.stock_uom = item["uom"]
                modified = True
            if doc.is_stock_item != item["stock"]:
                doc.is_stock_item = item["stock"]
                modified = True
            if doc.is_purchase_item != item["purchase"]:
                doc.is_purchase_item = item["purchase"]
                modified = True
            if doc.is_sales_item != item["sales"]:
                doc.is_sales_item = item["sales"]
                modified = True

            if modified:
                doc.save(ignore_permissions=True)
                print(f"Updated Item attributes for: {code}")
            else:
                print(f"Item already in desired state: {code}")

    # Remove obsolete 19L packaging items if present
    for obsolete_code in ["RM-BAG-19L", "RM-LBL-19L"]:
        if frappe.db.exists("Item", obsolete_code):
            frappe.delete_doc("Item", obsolete_code, force=True)
            print(f"Deleted obsolete item: {obsolete_code}")

    frappe.db.commit()
    print("All 21 Wateena Items successfully verified/provisioned!")
