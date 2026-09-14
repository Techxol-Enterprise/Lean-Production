# Techxol Solutions — Enterprise Handover Document
## ERPNext Item Master Setup & Configuration Specification
**Domain**: Mineral Water Purification & Bottling Plant (19L, 1.5L, 500ml)  
**Target Environment**: Production Server (Frappe / ERPNext v16 / Lean Production App)

---

### 1. Executive Summary & Valuation Policy
This document contains the exact master data specifications for all **19 Items** across water purification, blow molding, filling, and packaging operations.

> [!IMPORTANT]
> **Valuation & Costing Policy:**
> 1. **Dynamic Market-Based Valuation**: Valuation rates for all purchased raw materials (preforms, caps, labels, shrink film, minerals, chemicals) are **omitted / left at 0.00** at this setup stage. ERPNext will dynamically calculate Moving Average / FIFO valuation rates automatically from actual **Purchase Receipts / Purchase Invoices** based on daily market price fluctuations.
> 2. **Zero Negative Stock Enforced**: Non-negative stock is strictly preserved across all warehouses.
> 3. **Underground Borehole Water (`RM-WATER`)**: Must be created as a **Stock Item** (`is_stock_item = 1`) with valuation rate `0.00`. It is received into stock via **Stock Entry > Material Receipt** with **`Allow Zero Valuation Rate = 1`**. It must **NEVER** be converted to a Service Item.
> 4. **Mineral Salts UOM**: Stock UOM is **`Gram`** to align with high-precision batch dosing in BOMs; Purchase UOM is **`Kg`** with conversion factor **`1000.0`** (1 Kg = 1,000 Grams).
> 5. **19L Security Deposit (`19L-BOTTLE-DEPOSIT`)**: Non-stock service item (`is_stock_item = 0`) used for customer bottle ledger tracking and invoice deposits.

---

### 2. Item Group Tree Hierarchy
Before creating items, verify that the following Item Group hierarchy exists (this is automatically built by the `lean_production` app setup patch):

```
All Item Groups
├── Raw Material (Is Group: Yes)
│   ├── Raw Water (Is Group: No)
│   ├── Chemicals & Minerals (Is Group: No)
│   ├── Packaging Materials (Is Group: No)
│   └── Resins & Preforms (Is Group: No)
├── Semi Finished Goods (Is Group: Yes)
│   └── Empty Bottles (Is Group: No)
├── Mineral Water (Is Group: Yes)
│   └── Bulk Purified Water (Is Group: No)
├── Finished Goods (Is Group: No / Yes)
└── Services (Is Group: No)
```

---

### 3. Master Item Specifications Table

| # | Item Code | Item Name | Item Group | Stock UOM | Purchase UOM / Conversion | Stock Item | Purchase Item | Sales Item | Valuation Rate | Operational Purpose |
|---|---|---|---|---|---|:---:|:---:|:---:|:---:|---|
| **1** | `RM-WATER` | Raw Untreated Water | Raw Water | **Litre** | Litre (1.0) | **Yes** | No | No | `0.00` *(Free)* | Underground borehole water input for RO plant |
| **2** | `MIN-SODIUM` | Sodium Mineral Salt | Chemicals & Minerals | **Gram** | **Kg (1,000.0)** | **Yes** | Yes | No | *From Purchase* | Mineral remineralization dosing |
| **3** | `MIN-MAGNESIUM` | Magnesium Mineral Salt | Chemicals & Minerals | **Gram** | **Kg (1,000.0)** | **Yes** | Yes | No | *From Purchase* | Mineral remineralization dosing |
| **4** | `MIN-CALCIUM` | Calcium Mineral Salt | Chemicals & Minerals | **Gram** | **Kg (1,000.0)** | **Yes** | Yes | No | *From Purchase* | Mineral remineralization dosing |
| **5** | `CHEM-ANTISCALE` | RO Antiscalant Powder | Chemicals & Minerals | **Kg** | Gram (0.001) | **Yes** | Yes | No | *From Purchase* | RO membrane anti-fouling chemical |
| **6** | `RM-PREFORM-15G` | PET Preform - 15g (for 500ml) | Resins & Preforms | **Kg** | Kg (1.0) | **Yes** | Yes | No | *From Purchase* | Blow molding preform for 500ml bottles |
| **7** | `RM-PREFORM-30G` | PET Preform - 30g (for 1.5L) | Resins & Preforms | **Kg** | Kg (1.0) | **Yes** | Yes | No | *From Purchase* | Blow molding preform for 1.5L bottles |
| **8** | `INT-BTL-0.5L` | Empty PET Bottle - 500ml | Empty Bottles | **Nos** | Nos (1.0) | **Yes** | No | No | *From Blow Molding* | Blown intermediate bottle for 500ml |
| **9** | `INT-BTL-1.5L` | Empty PET Bottle - 1.5L | Empty Bottles | **Nos** | Nos (1.0) | **Yes** | No | No | *From Blow Molding* | Blown intermediate bottle for 1.5L |
| **10** | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | Bulk Purified Water | **Litre** | Litre (1.0) | **Yes** | No | No | *From Purification* | Output of Water Purification Entry |
| **11** | `RM-CAP-28MM` | 28mm Standard Plastic Cap | Packaging Materials | **Nos** | Nos (1.0) | **Yes** | Yes | No | *From Purchase* | Capping for 500ml & 1.5L bottles |
| **12** | `RM-LBL-0.5L` | Shrink Label - 500ml | Packaging Materials | **Nos** | Nos (1.0) | **Yes** | Yes | No | *From Purchase* | Sleeve/shrink labeling for 500ml |
| **13** | `RM-LBL-1.5L` | Shrink Label - 1.5L | Packaging Materials | **Nos** | Nos (1.0) | **Yes** | Yes | No | *From Purchase* | Sleeve/shrink labeling for 1.5L |
| **14** | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | Packaging Materials | **Unit** | Unit (1.0) | **Yes** | Yes | No | *From Purchase* | Secondary bundle packaging (1.5L x 6) |
| **15** | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | Packaging Materials | **Unit** | Unit (1.0) | **Yes** | Yes | No | *From Purchase* | Secondary bundle packaging (500ml x 12) |
| **16** | `FG-WATER-0.5L-12` | Bottled Water - 500ml x 12 Pack | Finished Goods | **Pack** | Pack (1.0) | **Yes** | No | **Yes** | *From Filling Entry* | Finished commercial pack for sale |
| **17** | `FG-WATER-1.5L-06` | Bottled Water - 1.5L x 6 Pack | Finished Goods | **Pack** | Pack (1.0) | **Yes** | No | **Yes** | *From Filling Entry* | Finished commercial pack for sale |
| **18** | `19L-REFILL` | 19L Mineral Water (Refill) | Finished Goods | **Nos** | Nos (1.0) | **Yes** | Yes | **Yes** | *From Filling Entry* | Commercial refill bottle (water content) |
| **19** | `19L-BOTTLE-DEPOSIT`| 19L Bottle Security Deposit | Services | **Nos** | Nos (1.0) | **No** | Yes | **Yes** | `0.00` *(Non-Stock)* | Security deposit line on invoice |

---

### 4. Special Configuration Details

#### A. Mineral Salts (`MIN-SODIUM`, `MIN-MAGNESIUM`, `MIN-CALCIUM`)
- **Stock UOM**: Must be **`Gram`**.
- **UOM Conversion Detail Table**:
  - `Gram` -> Conversion Factor: `1.0`
  - `Kg` -> Conversion Factor: `1000.0`
- **Dynamic Valuation**: When a Purchase Receipt for mineral salts is submitted in **Kg** at current market price (e.g. Rs 100/Kg), ERPNext will automatically compute the valuation rate as Rs 0.10/Gram.
- **BOM Behavior**: The Water Purification BOM consumes minerals directly in Grams per batch.

#### B. Underground Water (`RM-WATER`)
- **Stock UOM**: `Litre`.
- **Default Warehouse**: `Stores - [Abbr]` (or `Raw Water Tank`).
- **Initial Inventory / Routine Intake**:
  - Since **Negative Stock is strictly disabled**, water must be received into stock via:
    - **Document**: `Stock Entry`
    - **Type**: `Material Receipt`
    - **Rate**: `0.00`
    - **Allow Zero Valuation Rate**: Checked (`✔`)
  - Shift supervisors log a Material Receipt corresponding to flow meter readings (e.g. 50,000 or 100,000 Litres at a time).

#### C. Packaged Finished Goods (`FG-WATER-0.5L-12` & `FG-WATER-1.5L-06`)
- **Stock UOM**: **`Pack`**.
- Ensure the UOM **`Pack`** exists in ERPNext (`Stock > UOM`). If not, create it before creating the item.

---

### 5. Automated Setup Script for Production Server
The receiving developer or agent can execute this self-contained script on the production server via `bench execute` to automatically create or update all 19 items with exact UOMs, conversions, and groups, leaving initial valuation rate at `0.00` to be populated dynamically by purchases:

Save this script as `setup_production_items.py` inside the bench directory and run:
```bash
./env/bin/bench --site <site_name> execute setup_production_items.run
```

```python
import frappe

def run():
    # 1. Ensure Pack UOM exists
    if not frappe.db.exists("UOM", "Pack"):
        uom_doc = frappe.get_doc({
            "doctype": "UOM",
            "uom_name": "Pack",
            "name": "Pack",
            "must_be_whole_number": 1
        })
        uom_doc.insert(ignore_permissions=True)
        print("Created UOM: Pack")

    # 2. Master Item Definitions (Valuation rate initialized to 0.00; dynamically set by PO/Receipts)
    items_data = [
        {
            "item_code": "RM-WATER",
            "item_name": "Raw Untreated Water",
            "item_group": "Raw Water",
            "stock_uom": "Litre",
            "is_stock_item": 1,
            "is_purchase_item": 0,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "MIN-SODIUM",
            "item_name": "Sodium Mineral Salt",
            "item_group": "Chemicals & Minerals",
            "stock_uom": "Gram",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": [{"uom": "Kg", "conversion_factor": 1000.0}]
        },
        {
            "item_code": "MIN-MAGNESIUM",
            "item_name": "Magnesium Mineral Salt",
            "item_group": "Chemicals & Minerals",
            "stock_uom": "Gram",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": [{"uom": "Kg", "conversion_factor": 1000.0}]
        },
        {
            "item_code": "MIN-CALCIUM",
            "item_name": "Calcium Mineral Salt",
            "item_group": "Chemicals & Minerals",
            "stock_uom": "Gram",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": [{"uom": "Kg", "conversion_factor": 1000.0}]
        },
        {
            "item_code": "CHEM-ANTISCALE",
            "item_name": "RO Antiscalant Powder",
            "item_group": "Chemicals & Minerals",
            "stock_uom": "Kg",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": [{"uom": "Gram", "conversion_factor": 0.001}]
        },
        {
            "item_code": "RM-PREFORM-15G",
            "item_name": "PET Preform - 15g (for 500ml)",
            "item_group": "Resins & Preforms",
            "stock_uom": "Kg",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "RM-PREFORM-30G",
            "item_name": "PET Preform - 30g (for 1.5L)",
            "item_group": "Resins & Preforms",
            "stock_uom": "Kg",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "INT-BTL-0.5L",
            "item_name": "Empty PET Bottle - 500ml",
            "item_group": "Empty Bottles",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "is_purchase_item": 0,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "INT-BTL-1.5L",
            "item_name": "Empty PET Bottle - 1.5L",
            "item_group": "Empty Bottles",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "is_purchase_item": 0,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "INT-BULK-WATER",
            "item_name": "Purified Mineral Water (Bulk)",
            "item_group": "Bulk Purified Water",
            "stock_uom": "Litre",
            "is_stock_item": 1,
            "is_purchase_item": 0,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "RM-CAP-28MM",
            "item_name": "28mm Standard Plastic Cap",
            "item_group": "Packaging Materials",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "RM-LBL-0.5L",
            "item_name": "Shrink Label - 500ml",
            "item_group": "Packaging Materials",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "RM-LBL-1.5L",
            "item_name": "Shrink Label - 1.5L",
            "item_group": "Packaging Materials",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "RM-WRAP-06X",
            "item_name": "Shrink Wrap Film (6-pack)",
            "item_group": "Packaging Materials",
            "stock_uom": "Unit",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "RM-WRAP-12X",
            "item_name": "Shrink Wrap Film (12-pack)",
            "item_group": "Packaging Materials",
            "stock_uom": "Unit",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 0,
            "uoms": []
        },
        {
            "item_code": "FG-WATER-0.5L-12",
            "item_name": "Bottled Water - 500ml x 12 Pack",
            "item_group": "Finished Goods",
            "stock_uom": "Pack",
            "is_stock_item": 1,
            "is_purchase_item": 0,
            "is_sales_item": 1,
            "uoms": []
        },
        {
            "item_code": "FG-WATER-1.5L-06",
            "item_name": "Bottled Water - 1.5L x 6 Pack",
            "item_group": "Finished Goods",
            "stock_uom": "Pack",
            "is_stock_item": 1,
            "is_purchase_item": 0,
            "is_sales_item": 1,
            "uoms": []
        },
        {
            "item_code": "19L-REFILL",
            "item_name": "19L Mineral Water (Refill)",
            "item_group": "Finished Goods",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 1,
            "uoms": []
        },
        {
            "item_code": "19L-BOTTLE-DEPOSIT",
            "item_name": "19L Bottle Security Deposit",
            "item_group": "Services",
            "stock_uom": "Nos",
            "is_stock_item": 0,
            "is_purchase_item": 1,
            "is_sales_item": 1,
            "uoms": []
        }
    ]

    for data in items_data:
        code = data["item_code"]
        if frappe.db.exists("Item", code):
            doc = frappe.get_doc("Item", code)
            doc.item_name = data["item_name"]
            doc.item_group = data["item_group"]
            doc.stock_uom = data["stock_uom"]
            doc.is_stock_item = data["is_stock_item"]
            doc.is_purchase_item = data["is_purchase_item"]
            doc.is_sales_item = data["is_sales_item"]
            doc.valuation_rate = 0.0
        else:
            doc = frappe.new_doc("Item")
            doc.item_code = code
            doc.item_name = data["item_name"]
            doc.item_group = data["item_group"]
            doc.stock_uom = data["stock_uom"]
            doc.is_stock_item = data["is_stock_item"]
            doc.is_purchase_item = data["is_purchase_item"]
            doc.is_sales_item = data["is_sales_item"]
            doc.valuation_rate = 0.0

        # Ensure UOM conversion details
        existing_uoms = {u.uom: u for u in doc.get("uoms", [])}
        for u in data.get("uoms", []):
            if u["uom"] in existing_uoms:
                existing_uoms[u["uom"]].conversion_factor = u["conversion_factor"]
            else:
                doc.append("uoms", {
                    "uom": u["uom"],
                    "conversion_factor": u["conversion_factor"]
                })

        doc.save(ignore_permissions=True)
        print(f"Verified/Configured Item: {code}")

    frappe.db.commit()
    print("All 19 Items successfully configured in ERPNext!")
```
