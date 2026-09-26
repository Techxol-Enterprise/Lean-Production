# Wateena Production Site — Item Master List & Setup Handover
**Site:** `wateena` (`wateena.techxol.net`)  
**Extracted / Generated At:** 2026-09-24  
**Total Items:** 21  

---

## 1. Item Master Table

| # | Item Code | Item Name | Item Group | Stock UOM | Stock Item | Purchase Item | Sales Item | Valuation Rate | UOM Conversions | Disabled |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| 1 | `RM-WATER` | Raw Untreated Water | Raw Water | Litre | Yes | No | No | 0.00 | Litre (1.0) | No |
| 2 | `MIN-CALCIUM` | Calcium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 3 | `MIN-MAGNESIUM` | Magnesium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 4 | `MIN-SODIUM` | Sodium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 5 | `CHEM-ANTISCALE` | RO Antiscalant Liquid | Chemicals & Minerals | Litre | Yes | Yes | No | 0.00 | Litre (1.0) | No |
| 6 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | Bulk Purified Water | Litre | Yes | No | No | 0.00 | Litre (1.0) | No |
| 7 | `RM-PREFORM-15G` | PET Preform - 15g (for 500ml) | Resins & Preforms | Kg | Yes | Yes | No | 0.00 | Kg (1.0) | No |
| 8 | `RM-PREFORM-30G` | PET Preform - 30g (for 1.5L) | Resins & Preforms | Kg | Yes | Yes | No | 0.00 | Kg (1.0) | No |
| 9 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 10 | `RM-LBL-0.5L` | Shrink Label - 500ml | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 11 | `RM-LBL-1.5L` | Shrink Label - 1.5L | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 12 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | Packaging Materials | Unit | Yes | Yes | No | 0.00 | Unit (1.0) | No |
| 13 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | Packaging Materials | Unit | Yes | Yes | No | 0.00 | Unit (1.0) | No |
| 14 | `RM-CAP-55MM` | 55mm Non-Spill Cap (19L) | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 15 | `RM-SEAL-19L` | Heat Shrink Neck Seal - 19L | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 16 | `INT-BTL-0.5L` | Empty PET Bottle - 500ml | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 17 | `INT-BTL-1.5L` | Empty PET Bottle - 1.5L | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 18 | `FG-WATER-0.5L-12` | Wateena Water - 500ml x 12 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 19 | `FG-WATER-1.5L-06` | Wateena Water - 1.5L x 6 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 20 | `FG-19L-REFILL` | Wateena 19L (Refill) | Finished Goods | Nos | Yes | Yes | Yes | 0.00 | Nos (1.0) | No |
| 21 | `19L-BOTTLE-DEPOSIT` | 19L Bottle Security Deposit | Services | Nos | No | Yes | Yes | 0.00 | Nos (1.0) | No |

---

## 2. Category & Operational Breakdown

### A. Raw Materials (RM)
* **`RM-WATER`**: Raw Untreated Water (Borehole feed for RO plant)
  * Stock UOM: `Litre` | Stock Item: Yes | Valuation: `0.00`
* **`RM-PREFORM-15G`**: PET Preform - 15g for 500ml bottles
  * Stock UOM: `Kg` | Stock Item: Yes | Purchase Item: Yes
* **`RM-PREFORM-30G`**: PET Preform - 30g for 1.5L bottles
  * Stock UOM: `Kg` | Stock Item: Yes | Purchase Item: Yes
* **`RM-CAP-28MM`**: 28mm Standard Plastic Cap (500ml and 1.5L personal bottles)
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-0.5L`**: Shrink Label - 500ml
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-1.5L`**: Shrink Label - 1.5L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-WRAP-06X`**: Shrink Wrap Film (6-pack)
  * Stock UOM: `Unit` | Stock Item: Yes | Purchase Item: Yes
* **`RM-WRAP-12X`**: Shrink Wrap Film (12-pack)
  * Stock UOM: `Unit` | Stock Item: Yes | Purchase Item: Yes

### B. Dedicated 19L Packaging Components
* **`RM-CAP-55MM`**: 55mm Non-Spill Cap (19L)
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: 55mm commercial non-spill snap-on cap with inner valve for 19L water dispensers.
* **`RM-SEAL-19L`**: Heat Shrink Neck Seal - 19L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
  * Purpose: Tamper-evident heat shrink PVC sleeve applied over the 55mm cap and neck.

### C. Chemicals & Mineral Salts (MIN / CHEM)
* **`MIN-SODIUM`**: Sodium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`MIN-MAGNESIUM`**: Magnesium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`MIN-CALCIUM`**: Calcium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`CHEM-ANTISCALE`**: RO Antiscalant Liquid
  * Stock UOM: `Litre` | Purchase UOM: `Litre`

### D. Intermediate / Semi-Finished Goods (INT)
* **`INT-BULK-WATER`**: Purified Mineral Water (Bulk output of RO Purification)
  * Stock UOM: `Litre` | Stock Item: Yes | Purchase: No | Sales: No | Default Valuation Rate: `0.50`
* **`INT-BTL-0.5L`**: Empty PET Bottle - 500ml
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase: Yes (In-house blowing or Market Purchase) | Sales: No
* **`INT-BTL-1.5L`**: Empty PET Bottle - 1.5L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase: Yes (In-house blowing or Market Purchase) | Sales: No

### E. Finished Goods (FG)
* **`FG-19L-REFILL`**: Wateena 19L (Refill)
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase: Yes | Sales: Yes
* **`FG-WATER-0.5L-12`**: Wateena Water - 500ml x 12 Pack
  * Stock UOM: `Pack` | Stock Item: Yes | Purchase: No | Sales: Yes
* **`FG-WATER-1.5L-06`**: Wateena Water - 1.5L x 6 Pack
  * Stock UOM: `Pack` | Stock Item: Yes | Purchase: No | Sales: Yes

### F. Services & Deposits
* **`19L-BOTTLE-DEPOSIT`**: 19L Bottle Security Deposit
  * Stock UOM: `Nos` | Stock Item: No (Service Item) | Purchase: Yes | Sales: Yes

---

## 3. Automated Provisioning Module

Execute directly via Bench CLI:
```bash
bench --site wateena execute lean_production.setup_wateena_items.run
```
