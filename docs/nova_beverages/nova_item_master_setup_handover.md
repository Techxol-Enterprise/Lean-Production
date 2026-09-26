# Nova Beverages Production Site — Item Master Setup Handover
**Client:** `Nova Beverages`  
**Site:** `novabeverages.techxol.net` (Local: `erpnext.local`)  
**Extracted / Generated At:** 2026-09-21  
**Total Items:** 51  
**Brands Supported:** Rehydrate (Premium Pure) & Hydrafina (Standard Pure + Economy Mix)

---

## 1. Complete Item Master Table

| # | Item Code | Item Name | Item Group | Stock UOM | Stock Item | Purchase Item | Sales Item | Valuation Rate | UOM Conversions | Disabled |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| 1 | `RM-WATER` | Raw Untreated Water | Raw Water | Litre | Yes | No | No | 0.00 | Litre (1.0) | No |
| 2 | `MIN-CALCIUM` | Calcium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 3 | `MIN-MAGNESIUM` | Magnesium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 4 | `MIN-SODIUM` | Sodium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 5 | `CHEM-ANTISCALE` | RO Antiscalant Liquid | Chemicals & Minerals | Litre | Yes | Yes | No | 0.00 | Litre (1.0) | No |
| 6 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | Bulk Purified Water | Litre | Yes | No | No | 0.00 | Litre (1.0) | No |
| 7 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 8 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | Packaging Materials | Unit | Yes | Yes | No | 0.00 | Unit (1.0) | No |
| 9 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | Packaging Materials | Unit | Yes | Yes | No | 0.00 | Unit (1.0) | No |
| 10 | `19L-BOTTLE-DEPOSIT` | 19L Bottle Security Deposit | Services | Nos | No | Yes | Yes | 0.00 | Nos (1.0) | No |
| 11 | `RM-PREFORM-PURE-13.5G` | PET Preform - 13.5g Pure | Resins & Preforms | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 12 | `RM-PREFORM-PURE-15G` | PET Preform - 15g Pure | Resins & Preforms | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 13 | `RM-PREFORM-PURE-27G` | PET Preform - 27g Pure | Resins & Preforms | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 14 | `RM-PREFORM-PURE-30G` | PET Preform - 30g Pure | Resins & Preforms | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 15 | `RM-PREFORM-MIX-13.5G` | PET Preform - 13.5g Mix | Resins & Preforms | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 16 | `RM-PREFORM-MIX-15G` | PET Preform - 15g Mix | Resins & Preforms | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 17 | `RM-PREFORM-MIX-27G` | PET Preform - 27g Mix | Resins & Preforms | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 18 | `RM-PREFORM-MIX-30G` | PET Preform - 30g Mix | Resins & Preforms | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 19 | `RM-LBL-REH-0.5L` | Nova Beverages - Rehydrate Label - 500ml | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 20 | `RM-LBL-REH-1.5L` | Nova Beverages - Rehydrate Label - 1.5L | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 21 | `RM-LBL-HYD-0.5L` | Nova Beverages - Hydrafina Label - 500ml | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 22 | `RM-LBL-HYD-1.5L` | Nova Beverages - Hydrafina Label - 1.5L | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 23 | `RM-LBL-REH-19L` | Nova Beverages - Rehydrate Label - 19L | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 24 | `RM-CAP-55MM` | 55mm Non-Spill Cap (19L) | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 25 | `RM-SEAL-19L` | Heat Shrink Neck Seal - 19L | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 26 | `RM-BAG-19L` | Protective Dust Bag - 19L | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 27 | `INT-BTL-REH-0.5L-13.5G` | Empty PET Bottle - Nova Rehydrate - 500ml (13.5g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 28 | `INT-BTL-REH-0.5L-15G` | Empty PET Bottle - Nova Rehydrate - 500ml (15g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 29 | `INT-BTL-REH-1.5L-27G` | Empty PET Bottle - Nova Rehydrate - 1.5L (27g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 30 | `INT-BTL-REH-1.5L-30G` | Empty PET Bottle - Nova Rehydrate - 1.5L (30g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 31 | `INT-BTL-HYD-PURE-0.5L-13.5G` | Empty PET Bottle - Nova Hydrafina Pure - 500ml (13.5g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 32 | `INT-BTL-HYD-PURE-0.5L-15G` | Empty PET Bottle - Nova Hydrafina Pure - 500ml (15g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 33 | `INT-BTL-HYD-PURE-1.5L-27G` | Empty PET Bottle - Nova Hydrafina Pure - 1.5L (27g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 34 | `INT-BTL-HYD-PURE-1.5L-30G` | Empty PET Bottle - Nova Hydrafina Pure - 1.5L (30g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 35 | `INT-BTL-HYD-MIX-0.5L-13.5G` | Empty PET Bottle - Nova Hydrafina Mix - 500ml (13.5g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 36 | `INT-BTL-HYD-MIX-0.5L-15G` | Empty PET Bottle - Nova Hydrafina Mix - 500ml (15g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 37 | `INT-BTL-HYD-MIX-1.5L-27G` | Empty PET Bottle - Nova Hydrafina Mix - 1.5L (27g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 38 | `INT-BTL-HYD-MIX-1.5L-30G` | Empty PET Bottle - Nova Hydrafina Mix - 1.5L (30g) | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 39 | `FG-REH-WATER-0.5L-12-13.5G` | Nova Beverages - Rehydrate Water - PL - 500ml x 12 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 40 | `FG-REH-WATER-0.5L-12-15G` | Nova Beverages - Rehydrate Water - PH - 500ml x 12 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 41 | `FG-REH-WATER-1.5L-06-27G` | Nova Beverages - Rehydrate Water - PL - 1.5L x 6 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 42 | `FG-REH-WATER-1.5L-06-30G` | Nova Beverages - Rehydrate Water - PH - 1.5L x 6 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 43 | `FG-REH-19L-REFILL` | Nova Beverages - Rehydrate 19L (Refill) | Finished Goods | Nos | Yes | Yes | Yes | 0.00 | Nos (1.0) | No |
| 44 | `FG-HYD-WATER-PURE-0.5L-12-13.5G` | Nova Beverages - Hydrafina Water - PL - 500ml x 12 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 45 | `FG-HYD-WATER-PURE-0.5L-12-15G` | Nova Beverages - Hydrafina Water - PH - 500ml x 12 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 46 | `FG-HYD-WATER-PURE-1.5L-06-27G` | Nova Beverages - Hydrafina Water - PL - 1.5L x 6 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 47 | `FG-HYD-WATER-PURE-1.5L-06-30G` | Nova Beverages - Hydrafina Water - PH - 1.5L x 6 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 48 | `FG-HYD-WATER-MIX-0.5L-12-13.5G` | Nova Beverages - Hydrafina Water - ML - 500ml x 12 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 49 | `FG-HYD-WATER-MIX-0.5L-12-15G` | Nova Beverages - Hydrafina Water - MH - 500ml x 12 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 50 | `FG-HYD-WATER-MIX-1.5L-06-27G` | Nova Beverages - Hydrafina Water - ML - 1.5L x 6 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 51 | `FG-HYD-WATER-MIX-1.5L-06-30G` | Nova Beverages - Hydrafina Water - MH - 1.5L x 6 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |

---

## 2. Category & Operational Lineage Breakdown

### A. Raw Materials (RM)
* **`RM-WATER`**: Raw Untreated Water (Borehole feed for RO plant)
  * Stock UOM: `Litre` | Stock Item: Yes | Valuation: `0.00`
* **`RM-PREFORM-PURE-13.5G`**: PET Preform - 13.5g Pure
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Blow molding lightweight 500ml bottles for Rehydrate (PL) and Hydrafina Pure (PL).
* **`RM-PREFORM-PURE-15G`**: PET Preform - 15g Pure
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Blow molding heavy/export 500ml bottles for Rehydrate (PH) and Hydrafina Pure (PH).
* **`RM-PREFORM-PURE-27G`**: PET Preform - 27g Pure
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Blow molding lightweight 1.5L bottles for Rehydrate (PL) and Hydrafina Pure (PL).
* **`RM-PREFORM-PURE-30G`**: PET Preform - 30g Pure
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Blow molding heavy/export 1.5L bottles for Rehydrate (PH) and Hydrafina Pure (PH).
* **`RM-PREFORM-MIX-13.5G`**: PET Preform - 13.5g Mix
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Blow molding economy 500ml bottles for Hydrafina Mix (ML).
* **`RM-PREFORM-MIX-15G`**: PET Preform - 15g Mix
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Blow molding economy heavy 500ml bottles for Hydrafina Mix (MH).
* **`RM-PREFORM-MIX-27G`**: PET Preform - 27g Mix
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Blow molding economy 1.5L bottles for Hydrafina Mix (ML).
* **`RM-PREFORM-MIX-30G`**: PET Preform - 30g Mix
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Blow molding economy heavy 1.5L bottles for Hydrafina Mix (MH).
* **`RM-CAP-28MM`**: 28mm Standard Plastic Cap (Universal closure)
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-WRAP-12X`**: Shrink Wrap Film (12-pack bundle)
  * Stock UOM: `Unit` | Stock Item: Yes | Purchase Item: Yes
* **`RM-WRAP-06X`**: Shrink Wrap Film (6-pack bundle)
  * Stock UOM: `Unit` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-REH-0.5L`**: Nova Beverages - Rehydrate Label - 500ml
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-REH-1.5L`**: Nova Beverages - Rehydrate Label - 1.5L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-HYD-0.5L`**: Nova Beverages - Hydrafina Label - 500ml
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-HYD-1.5L`**: Nova Beverages - Hydrafina Label - 1.5L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-REH-19L`**: Nova Beverages - Rehydrate Label - 19L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Brand identification and date collar sticker applied to filled 19L Rehydrate bottles.
* **`RM-CAP-55MM`**: 55mm Non-Spill Cap (19L)
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: 55mm commercial non-spill snap-on cap with inner valve for 19L water dispensers.
* **`RM-SEAL-19L`**: Heat Shrink Neck Seal - 19L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Tamper-evident heat shrink PVC sleeve applied over the 55mm cap and neck.
* **`RM-BAG-19L`**: Protective Dust Bag - 19L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Polyethylene dust protective cover slipped over filled 19L bottle during transit.

---

### B. Chemicals & Mineral Salts (MIN / CHEM)
* **`MIN-SODIUM`**: Sodium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`MIN-MAGNESIUM`**: Magnesium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`MIN-CALCIUM`**: Calcium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`CHEM-ANTISCALE`**: RO Antiscalant Liquid
  * Stock UOM: `Litre` | Purchase UOM: `Litre`

---

### C. Intermediate / Semi-Finished Goods (INT)
* **`INT-BULK-WATER`**: Purified Mineral Water (Bulk output of RO Purification)
  * Stock UOM: `Litre` | Stock Item: Yes | Purchase: No | Sales: No | Default Valuation Rate: `0.50`
* **Blown Bottles (Stock UOM: `Nos` | Stock Item: Yes | Purchase: Yes | Sales: No)**:
  * *Supports dual-sourcing: In-house blow molding from preforms or direct market purchase via Purchase Receipt / Invoice during peak demand.*
  * **Rehydrate Blown Bottles**:
    * `INT-BTL-REH-0.5L-13.5G`: Made from `RM-PREFORM-PURE-13.5G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-REH-0.5L-15G`: Made from `RM-PREFORM-PURE-15G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-REH-1.5L-27G`: Made from `RM-PREFORM-PURE-27G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-REH-1.5L-30G`: Made from `RM-PREFORM-PURE-30G` (1:1 piece ratio) or Market Purchase
  * **Hydrafina Pure Blown Bottles**:
    * `INT-BTL-HYD-PURE-0.5L-13.5G`: Made from `RM-PREFORM-PURE-13.5G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-HYD-PURE-0.5L-15G`: Made from `RM-PREFORM-PURE-15G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-HYD-PURE-1.5L-27G`: Made from `RM-PREFORM-PURE-27G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-HYD-PURE-1.5L-30G`: Made from `RM-PREFORM-PURE-30G` (1:1 piece ratio) or Market Purchase
  * **Hydrafina Mix Blown Bottles**:
    * `INT-BTL-HYD-MIX-0.5L-13.5G`: Made from `RM-PREFORM-MIX-13.5G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-HYD-MIX-0.5L-15G`: Made from `RM-PREFORM-MIX-15G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-HYD-MIX-1.5L-27G`: Made from `RM-PREFORM-MIX-27G` (1:1 piece ratio) or Market Purchase
    * `INT-BTL-HYD-MIX-1.5L-30G`: Made from `RM-PREFORM-MIX-30G` (1:1 piece ratio) or Market Purchase

---

### D. Finished Goods (FG)

#### 1. Rehydrate Finished Goods Lineup
* **`FG-REH-WATER-0.5L-12-13.5G`**: Nova Beverages - Rehydrate Water - PL - 500ml x 12 Pack
  * Made From: `INT-BTL-REH-0.5L-13.5G` | Stock UOM: `Pack`
* **`FG-REH-WATER-0.5L-12-15G`**: Nova Beverages - Rehydrate Water - PH - 500ml x 12 Pack
  * Made From: `INT-BTL-REH-0.5L-15G` | Stock UOM: `Pack`
* **`FG-REH-WATER-1.5L-06-27G`**: Nova Beverages - Rehydrate Water - PL - 1.5L x 6 Pack
  * Made From: `INT-BTL-REH-1.5L-27G` | Stock UOM: `Pack`
* **`FG-REH-WATER-1.5L-06-30G`**: Nova Beverages - Rehydrate Water - PH - 1.5L x 6 Pack
  * Made From: `INT-BTL-REH-1.5L-30G` | Stock UOM: `Pack`
* **`FG-REH-19L-REFILL`**: Nova Beverages - Rehydrate 19L (Refill)
  * Made From: Standard Purchased 19L Bottle | Stock UOM: `Nos`

#### 2. Hydrafina Pure Finished Goods Lineup (PL & PH)
* **`FG-HYD-WATER-PURE-0.5L-12-13.5G`**: Nova Beverages - Hydrafina Water - PL - 500ml x 12 Pack
  * Made From: `INT-BTL-HYD-PURE-0.5L-13.5G` | Stock UOM: `Pack`
* **`FG-HYD-WATER-PURE-0.5L-12-15G`**: Nova Beverages - Hydrafina Water - PH - 500ml x 12 Pack
  * Made From: `INT-BTL-HYD-PURE-0.5L-15G` | Stock UOM: `Pack`
* **`FG-HYD-WATER-PURE-1.5L-06-27G`**: Nova Beverages - Hydrafina Water - PL - 1.5L x 6 Pack
  * Made From: `INT-BTL-HYD-PURE-1.5L-27G` | Stock UOM: `Pack`
* **`FG-HYD-WATER-PURE-1.5L-06-30G`**: Nova Beverages - Hydrafina Water - PH - 1.5L x 6 Pack
  * Made From: `INT-BTL-HYD-PURE-1.5L-30G` | Stock UOM: `Pack`

#### 3. Hydrafina Mix Economy Finished Goods Lineup (ML & MH)
* **`FG-HYD-WATER-MIX-0.5L-12-13.5G`**: Nova Beverages - Hydrafina Water - ML - 500ml x 12 Pack
  * Made From: `INT-BTL-HYD-MIX-0.5L-13.5G` | Stock UOM: `Pack`
* **`FG-HYD-WATER-MIX-0.5L-12-15G`**: Nova Beverages - Hydrafina Water - MH - 500ml x 12 Pack
  * Made From: `INT-BTL-HYD-MIX-0.5L-15G` | Stock UOM: `Pack`
* **`FG-HYD-WATER-MIX-1.5L-06-27G`**: Nova Beverages - Hydrafina Water - ML - 1.5L x 6 Pack
  * Made From: `INT-BTL-HYD-MIX-1.5L-27G` | Stock UOM: `Pack`
* **`FG-HYD-WATER-MIX-1.5L-06-30G`**: Nova Beverages - Hydrafina Water - MH - 1.5L x 6 Pack
  * Made From: `INT-BTL-HYD-MIX-1.5L-30G` | Stock UOM: `Pack`

---

### E. Services & Deposits
* **`19L-BOTTLE-DEPOSIT`**: 19L Bottle Security Deposit
  * Stock UOM: `Nos` | Stock Item: No (Service Item) | Purchase: Yes | Sales: Yes

---

## 3. Automated Python Provisioning Script for Production Server

Save this script as `setup_nova_items.py` in your bench directory, then execute:
```bash
./env/bin/bench --site <site_name> execute setup_nova_items.run
```

```python
import frappe

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

    # 2. Master Items Definition
    items_to_create = [
        # Upstream Raw Materials & Packaging
        {"code": "RM-WATER", "name": "Raw Untreated Water", "group": "Raw Water", "uom": "Litre", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "MIN-CALCIUM", "name": "Calcium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "MIN-MAGNESIUM", "name": "Magnesium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "MIN-SODIUM", "name": "Sodium Mineral Salt", "group": "Chemicals & Minerals", "uom": "Gram", "stock": 1, "purchase": 1, "sales": 0, "conversions": [("Kg", 1000.0)]},
        {"code": "CHEM-ANTISCALE", "name": "RO Antiscalant Liquid", "group": "Chemicals & Minerals", "uom": "Litre", "stock": 1, "purchase": 1, "sales": 0},
        {"code": "INT-BULK-WATER", "name": "Purified Mineral Water (Bulk)", "group": "Bulk Purified Water", "uom": "Litre", "stock": 1, "purchase": 0, "sales": 0},
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
        {"code": "INT-BTL-REH-0.5L-13.5G", "name": "Empty PET Bottle - Nova Rehydrate - 500ml (13.5g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-REH-0.5L-15G", "name": "Empty PET Bottle - Nova Rehydrate - 500ml (15g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-REH-1.5L-27G", "name": "Empty PET Bottle - Nova Rehydrate - 1.5L (27g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-REH-1.5L-30G", "name": "Empty PET Bottle - Nova Rehydrate - 1.5L (30g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},

        # Empty Bottles - Hydrafina Pure
        {"code": "INT-BTL-HYD-PURE-0.5L-13.5G", "name": "Empty PET Bottle - Nova Hydrafina Pure - 500ml (13.5g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-HYD-PURE-0.5L-15G", "name": "Empty PET Bottle - Nova Hydrafina Pure - 500ml (15g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-HYD-PURE-1.5L-27G", "name": "Empty PET Bottle - Nova Hydrafina Pure - 1.5L (27g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-HYD-PURE-1.5L-30G", "name": "Empty PET Bottle - Nova Hydrafina Pure - 1.5L (30g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},

        # Empty Bottles - Hydrafina Mix
        {"code": "INT-BTL-HYD-MIX-0.5L-13.5G", "name": "Empty PET Bottle - Nova Hydrafina Mix - 500ml (13.5g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-HYD-MIX-0.5L-15G", "name": "Empty PET Bottle - Nova Hydrafina Mix - 500ml (15g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-HYD-MIX-1.5L-27G", "name": "Empty PET Bottle - Nova Hydrafina Mix - 1.5L (27g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},
        {"code": "INT-BTL-HYD-MIX-1.5L-30G", "name": "Empty PET Bottle - Nova Hydrafina Mix - 1.5L (30g)", "group": "Empty Bottles", "uom": "Nos", "stock": 1, "purchase": 0, "sales": 0},

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
            doc.valuation_rate = 0.0
            
            # Append UOM Conversions if defined
            if "conversions" in item_data:
                for uom_name, factor in item_data["conversions"]:
                    doc.append("uoms", {"uom": uom_name, "conversion_factor": factor})

            doc.insert(ignore_permissions=True)
            print(f"Created Item: {code}")

    frappe.db.commit()
    print("All 51 Nova Beverages items successfully configured!")
```
