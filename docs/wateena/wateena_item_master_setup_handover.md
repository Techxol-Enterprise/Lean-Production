# Wateena Production Site - Item Master List
**Site:** `wateena` (`wateena.techxol.net`)  
**Extracted At:** 2026-09-14 16:26:00  
**Total Items:** 19  

---

## 1. Item Master Table

| # | Item Code | Item Name | Item Group | Stock UOM | Stock Item | Purchase Item | Sales Item | Valuation Rate | UOM Conversions | Disabled |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| 1 | `19L-BOTTLE-DEPOSIT` | 19L Bottle Security Deposit | Services | Nos | No | Yes | Yes | 0.00 | Nos (1.0) | No |
| 2 | `CHEM-ANTISCALE` | RO Antiscalant Liquid | Chemicals & Minerals | Litre | Yes | Yes | No | 0.00 | Litre (1.0) | No |
| 3 | `FG-19L-REFILL` | Wateena 19L (Refill) | Finished Goods | Nos | Yes | Yes | Yes | 0.00 | Nos (1.0) | No |
| 4 | `FG-WATER-0.5L-12` | Wateena Water - 500ml x 12 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 5 | `FG-WATER-1.5L-06` | Wateena Water - 1.5L x 6 Pack | Finished Goods | Pack | Yes | No | Yes | 0.00 | Pack (1.0) | No |
| 6 | `INT-BTL-0.5L` | Empty PET Bottle - 500ml | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 7 | `INT-BTL-1.5L` | Empty PET Bottle - 1.5L | Empty Bottles | Nos | Yes | No | No | 0.00 | Nos (1.0) | No |
| 8 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | Bulk Purified Water | Litre | Yes | No | No | 0.00 | Litre (1.0) | No |
| 9 | `MIN-CALCIUM` | Calcium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 10 | `MIN-MAGNESIUM` | Magnesium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 11 | `MIN-SODIUM` | Sodium Mineral Salt | Chemicals & Minerals | Gram | Yes | Yes | No | 0.00 | Gram (1.0), Kg (1000.0) | No |
| 12 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 13 | `RM-LBL-0.5L` | Shrink Label - 500ml | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 14 | `RM-LBL-1.5L` | Shrink Label - 1.5L | Packaging Materials | Nos | Yes | Yes | No | 0.00 | Nos (1.0) | No |
| 15 | `RM-PREFORM-15G` | PET Preform - 15g (for 500ml) | Resins & Preforms | Kg | Yes | Yes | No | 0.00 | Kg (1.0) | No |
| 16 | `RM-PREFORM-30G` | PET Preform - 30g (for 1.5L) | Resins & Preforms | Kg | Yes | Yes | No | 0.00 | Kg (1.0) | No |
| 17 | `RM-WATER` | Raw Untreated Water | Raw Water | Litre | Yes | No | No | 0.00 | Litre (1.0) | No |
| 18 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | Packaging Materials | Unit | Yes | Yes | No | 0.00 | Unit (1.0) | No |
| 19 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | Packaging Materials | Unit | Yes | Yes | No | 0.00 | Unit (1.0) | No |

---

## 2. Category & Operational Breakdown

### A. Raw Materials (RM)
* **`RM-WATER`**: Raw Untreated Water (Borehole feed for RO plant)
  * Stock UOM: `Litre` | Stock Item: Yes | Valuation: `0.00` *(booked via Material Receipt with Allow Zero Valuation Rate)*
* **`RM-PREFORM-15G`**: PET Preform - 15g for 500ml bottles
  * Stock UOM: `Kg` | Stock Item: Yes | Purchase Item: Yes
* **`RM-PREFORM-30G`**: PET Preform - 30g for 1.5L bottles
  * Stock UOM: `Kg` | Stock Item: Yes | Purchase Item: Yes
* **`RM-CAP-28MM`**: 28mm Standard Plastic Cap
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-0.5L`**: Shrink Label - 500ml
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-LBL-1.5L`**: Shrink Label - 1.5L
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase Item: Yes
* **`RM-WRAP-06X`**: Shrink Wrap Film (6-pack)
  * Stock UOM: `Unit` | Stock Item: Yes | Purchase Item: Yes
* **`RM-WRAP-12X`**: Shrink Wrap Film (12-pack)
  * Stock UOM: `Unit` | Stock Item: Yes | Purchase Item: Yes

### B. Chemicals & Mineral Salts (MIN / CHEM)
* **`MIN-SODIUM`**: Sodium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`MIN-MAGNESIUM`**: Magnesium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`MIN-CALCIUM`**: Calcium Mineral Salt
  * Stock UOM: `Gram` | Purchase UOM: `Kg` (`1 Kg = 1000 Grams`)
* **`CHEM-ANTISCALE`**: RO Antiscalant Liquid
  * Stock UOM: `Litre` | Purchase UOM: `Litre` (`1 Litre = 1.0 Litre`)

### C. Intermediate / Semi-Finished Goods (INT)
* **`INT-BULK-WATER`**: Purified Mineral Water (Bulk output of RO Purification)
  * Stock UOM: `Litre` | Stock Item: Yes | Purchase: No | Sales: No
* **`INT-BTL-0.5L`**: Empty PET Bottle - 500ml (output of Blow Molding)
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase: No | Sales: No
* **`INT-BTL-1.5L`**: Empty PET Bottle - 1.5L (output of Blow Molding)
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase: No | Sales: No

### D. Finished Goods (FG)
* **`FG-19L-REFILL`**: Wateena 19L (Refill)
  * Stock UOM: `Nos` | Stock Item: Yes | Purchase: Yes | Sales: Yes
* **`FG-WATER-0.5L-12`**: Wateena Water - 500ml x 12 Pack
  * Stock UOM: `Pack` | Stock Item: Yes | Purchase: No | Sales: Yes
* **`FG-WATER-1.5L-06`**: Wateena Water - 1.5L x 6 Pack
  * Stock UOM: `Pack` | Stock Item: Yes | Purchase: No | Sales: Yes

### E. Services & Deposits
* **`19L-BOTTLE-DEPOSIT`**: 19L Bottle Security Deposit
  * Stock UOM: `Nos` | Stock Item: No (Service Item) | Purchase: Yes | Sales: Yes
