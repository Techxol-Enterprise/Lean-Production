# Nova Beverages Production Site — BOM Master Specification & Setup Handover
**Client:** `Nova Beverages`  
**Site:** `novabeverages.techxol.net` (Local: `erpnext.local`)  
**Scope:** Stage 1 (Water Purification), Stage 2 (Blow Molding Lines: Pure & Mix), Stage 3 (Filling & Packaging Lines)  
**Valuation Basis:** `Valuation Rate` (all rates initialized at `0.00`, dynamically derived from actual purchase inventory)  
**Total BOMs Configured:** 26 (1 Purification + 12 Blow Molding + 13 Finished Goods Filling)

---

## 1. Architectural Overview & Multi-Stage Manufacturing Pipeline

```mermaid
graph TD
    subgraph Stage 1: Water Purification Line (Shared Plant)
        RM_W[RM-WATER: 1,000 L] --> RO[RO Purification Plant]
        MIN_CA[MIN-CALCIUM: 150 g] --> RO
        MIN_MG[MIN-MAGNESIUM: 30 g] --> RO
        MIN_NA[MIN-SODIUM: 25 g] --> RO
        CHEM[CHEM-ANTISCALE: 0.040 L] --> RO
        RO --> INT_W[INT-BULK-WATER: 1,000 Litres]
    end

    subgraph Stage 2A: Rehydrate Blow Molding (Pure PET - 1:1 Piece Ratio)
        P_REH_135[RM-PREFORM-PURE-13.5G: 1,000 Nos] --> BM_REH_1[Rehydrate Molder 1] --> B_REH_05_135[INT-BTL-REH-0.5L-13.5G: 1,000 Nos]
        P_REH_150[RM-PREFORM-PURE-15G: 1,000 Nos]   --> BM_REH_2[Rehydrate Molder 2] --> B_REH_05_150[INT-BTL-REH-0.5L-15G: 1,000 Nos]
        P_REH_270[RM-PREFORM-PURE-27G: 1,000 Nos]   --> BM_REH_3[Rehydrate Molder 3] --> B_REH_15_270[INT-BTL-REH-1.5L-27G: 1,000 Nos]
        P_REH_300[RM-PREFORM-PURE-30G: 1,000 Nos]   --> BM_REH_4[Rehydrate Molder 4] --> B_REH_15_300[INT-BTL-REH-1.5L-30G: 1,000 Nos]
    end

    subgraph Stage 2B: Hydrafina Pure Blow Molding (Pure PET - 1:1 Piece Ratio)
        P_HP_135[RM-PREFORM-PURE-13.5G: 1,000 Nos] --> BM_HP_1[Hydrafina Pure Molder 1] --> B_HP_05_135[INT-BTL-HYD-PURE-0.5L-13.5G: 1,000 Nos]
        P_HP_150[RM-PREFORM-PURE-15G: 1,000 Nos]   --> BM_HP_2[Hydrafina Pure Molder 2] --> B_HP_05_150[INT-BTL-HYD-PURE-0.5L-15G: 1,000 Nos]
        P_HP_270[RM-PREFORM-PURE-27G: 1,000 Nos]   --> BM_HP_3[Hydrafina Pure Molder 3] --> B_HP_15_270[INT-BTL-HYD-PURE-1.5L-27G: 1,000 Nos]
        P_HP_300[RM-PREFORM-PURE-30G: 1,000 Nos]   --> BM_HP_4[Hydrafina Pure Molder 4] --> B_HP_15_300[INT-BTL-HYD-PURE-1.5L-30G: 1,000 Nos]
    end

    subgraph Stage 2C: Hydrafina Mix Blow Molding (Mix PET Economy - 1:1 Piece Ratio)
        P_HM_135[RM-PREFORM-MIX-13.5G: 1,000 Nos] --> BM_HM_1[Hydrafina Mix Molder 1] --> B_HM_05_135[INT-BTL-HYD-MIX-0.5L-13.5G: 1,000 Nos]
        P_HM_150[RM-PREFORM-MIX-15G: 1,000 Nos]   --> BM_HM_2[Hydrafina Mix Molder 2] --> B_HM_05_150[INT-BTL-HYD-MIX-0.5L-15G: 1,000 Nos]
        P_HM_270[RM-PREFORM-MIX-27G: 1,000 Nos]   --> BM_HM_3[Hydrafina Mix Molder 3] --> B_HM_15_270[INT-BTL-HYD-MIX-1.5L-27G: 1,000 Nos]
        P_HM_300[RM-PREFORM-MIX-30G: 1,000 Nos]   --> BM_HM_4[Hydrafina Mix Molder 4] --> B_HM_15_300[INT-BTL-HYD-MIX-1.5L-30G: 1,000 Nos]
    end

    subgraph Stage 3A: Nova Rehydrate Filling & Packaging Lines
        INT_W --> REH_FILL[Rehydrate Line]
        B_REH_05_135 & B_REH_05_150 & B_REH_15_270 & B_REH_15_300 --> REH_FILL
        LBL_REH[RM-LBL-REH-0.5L & 1.5L] --> REH_FILL
        CAPS[RM-CAP-28MM] --> REH_FILL
        WRAP[RM-WRAP-12X & 06X] --> REH_FILL

        REH_FILL --> FG_REH_05_PL[FG-REH-WATER-0.5L-12-13.5G: PL 500ml x 12 Pack]
        REH_FILL --> FG_REH_05_PH[FG-REH-WATER-0.5L-12-15G: PH 500ml x 12 Pack]
        REH_FILL --> FG_REH_15_PL[FG-REH-WATER-1.5L-06-27G: PL 1.5L x 6 Pack]
        REH_FILL --> FG_REH_15_PH[FG-REH-WATER-1.5L-06-30G: PH 1.5L x 6 Pack]
        INT_W & CAPS --> FG_REH_19[FG-REH-19L-REFILL: 19L Refill]
    end

    subgraph Stage 3B: Nova Hydrafina Pure Filling & Packaging Lines
        INT_W --> HYD_P_FILL[Hydrafina Pure Line]
        B_HP_05_135 & B_HP_05_150 & B_HP_15_270 & B_HP_15_300 --> HYD_P_FILL
        LBL_HYD[RM-LBL-HYD-0.5L & 1.5L] --> HYD_P_FILL
        CAPS --> HYD_P_FILL
        WRAP --> HYD_P_FILL

        HYD_P_FILL --> FG_HYD_P05_PL[FG-HYD-WATER-PURE-0.5L-12-13.5G: PL 500ml x 12 Pack]
        HYD_P_FILL --> FG_HYD_P05_PH[FG-HYD-WATER-PURE-0.5L-12-15G: PH 500ml x 12 Pack]
        HYD_P_FILL --> FG_HYD_P15_PL[FG-HYD-WATER-PURE-1.5L-06-27G: PL 1.5L x 6 Pack]
        HYD_P_FILL --> FG_HYD_P15_PH[FG-HYD-WATER-PURE-1.5L-06-30G: PH 1.5L x 6 Pack]
    end

    subgraph Stage 3C: Nova Hydrafina Mix Filling & Packaging Lines
        INT_W --> HYD_M_FILL[Hydrafina Mix Line]
        B_HM_05_135 & B_HM_05_150 & B_HM_15_270 & B_HM_15_300 --> HYD_M_FILL
        LBL_HYD --> HYD_M_FILL
        CAPS --> HYD_M_FILL
        WRAP --> HYD_M_FILL

        HYD_M_FILL --> FG_HYD_M05_ML[FG-HYD-WATER-MIX-0.5L-12-13.5G: ML 500ml x 12 Pack]
        HYD_M_FILL --> FG_HYD_M05_MH[FG-HYD-WATER-MIX-0.5L-12-15G: MH 500ml x 12 Pack]
        HYD_M_FILL --> FG_HYD_M15_ML[FG-HYD-WATER-MIX-1.5L-06-27G: ML 1.5L x 6 Pack]
        HYD_M_FILL --> FG_HYD_M15_MH[FG-HYD-WATER-MIX-1.5L-06-30G: MH 1.5L x 6 Pack]
    end
```

---

## 2. Stage 1: Water Purification BOM

### `BOM-INT-BULK-WATER-001`
- **Finished Item Produced**: `INT-BULK-WATER` (Purified Mineral Water (Bulk))
- **Base Output Quantity**: **1,000.0 Litres**
- **Rate of Materials Based On**: `Valuation Rate`
- **Is Active**: Yes (`1`) | **Is Default**: Yes (`1`)
- **Chemical Formulation Rationale**:
  - $1\text{ ppm} = 1\text{ mg/L} = 1\text{ gram per 1,000 Litres}$.
  - Calcium salt is dosed at 150 ppm (150 g per 1,000 L).
  - Magnesium salt is dosed at 30 ppm (30 g per 1,000 L).
  - Sodium salt is dosed at 25 ppm (25 g per 1,000 L).
  - Antiscalant liquid is dosed at 40 ppm (0.040 L / 40 ml per 1,000 L).
  - Raw water is modeled at 1,000 L (1:1 base, zero natural resource cost).

#### Components Table:
| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `RM-WATER` | Raw Untreated Water | **1,000.0** | Litre | 0.00 | 0.00 |
| 2 | `MIN-CALCIUM` | Calcium Mineral Salt | **150.0** | Gram | 0.00 | 0.00 |
| 3 | `MIN-MAGNESIUM` | Magnesium Mineral Salt | **30.0** | Gram | 0.00 | 0.00 |
| 4 | `MIN-SODIUM` | Sodium Mineral Salt | **25.0** | Gram | 0.00 | 0.00 |
| 5 | `CHEM-ANTISCALE` | RO Antiscalant Liquid | **0.040** | Litre | 0.00 | 0.00 |
| | **Total Batch Cost** | | | | | **Rs 0.00** |

---

## 3. Stage 2: Blow Molding BOMs (1:1 Piece Conversion Ratio)

All blow molding operations operate on standard batches of **1,000 Nos** of bottles produced from **1,000 Nos** of preforms.

### A. Rehydrate Pure Bottles (4 BOMs)
1. **`BOM-INT-BTL-REH-0.5L-13.5G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-REH-0.5L-13.5G`
   - Component: `RM-PREFORM-PURE-13.5G` — **1,000.0 Nos**
2. **`BOM-INT-BTL-REH-0.5L-15G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-REH-0.5L-15G`
   - Component: `RM-PREFORM-PURE-15G` — **1,000.0 Nos**
3. **`BOM-INT-BTL-REH-1.5L-27G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-REH-1.5L-27G`
   - Component: `RM-PREFORM-PURE-27G` — **1,000.0 Nos**
4. **`BOM-INT-BTL-REH-1.5L-30G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-REH-1.5L-30G`
   - Component: `RM-PREFORM-PURE-30G` — **1,000.0 Nos**

### B. Hydrafina Pure Bottles (4 BOMs)
5. **`BOM-INT-BTL-HYD-PURE-0.5L-13.5G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-HYD-PURE-0.5L-13.5G`
   - Component: `RM-PREFORM-PURE-13.5G` — **1,000.0 Nos**
6. **`BOM-INT-BTL-HYD-PURE-0.5L-15G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-HYD-PURE-0.5L-15G`
   - Component: `RM-PREFORM-PURE-15G` — **1,000.0 Nos**
7. **`BOM-INT-BTL-HYD-PURE-1.5L-27G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-HYD-PURE-1.5L-27G`
   - Component: `RM-PREFORM-PURE-27G` — **1,000.0 Nos**
8. **`BOM-INT-BTL-HYD-PURE-1.5L-30G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-HYD-PURE-1.5L-30G`
   - Component: `RM-PREFORM-PURE-30G` — **1,000.0 Nos**

### C. Hydrafina Mix Economy Bottles (4 BOMs)
9. **`BOM-INT-BTL-HYD-MIX-0.5L-13.5G-001`**
   - Output: **1,000.0 Nos** of `INT-BTL-HYD-MIX-0.5L-13.5G`
   - Component: `RM-PREFORM-MIX-13.5G` — **1,000.0 Nos**
10. **`BOM-INT-BTL-HYD-MIX-0.5L-15G-001`**
    - Output: **1,000.0 Nos** of `INT-BTL-HYD-MIX-0.5L-15G`
    - Component: `RM-PREFORM-MIX-15G` — **1,000.0 Nos**
11. **`BOM-INT-BTL-HYD-MIX-1.5L-27G-001`**
    - Output: **1,000.0 Nos** of `INT-BTL-HYD-MIX-1.5L-27G`
    - Component: `RM-PREFORM-MIX-27G` — **1,000.0 Nos**
12. **`BOM-INT-BTL-HYD-MIX-1.5L-30G-001`**
    - Output: **1,000.0 Nos** of `INT-BTL-HYD-MIX-1.5L-30G`
    - Component: `RM-PREFORM-MIX-30G` — **1,000.0 Nos**

---

## 4. Stage 3: Finished Goods Filling & Packaging BOMs

### A. Rehydrate Finished Goods (5 BOMs)

#### 1. `BOM-FG-REH-WATER-0.5L-12-13.5G-001` (PL - 500ml x 12 Pack)
- **Output**: **1.0 Pack** of `FG-REH-WATER-0.5L-12-13.5G`
- **Lineage**: Made from 13.5g bottle (`INT-BTL-REH-0.5L-13.5G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **6.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-REH-0.5L-13.5G` | Empty PET Bottle - Nova Rehydrate - 500ml (13.5g) | **12.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **12.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-REH-0.5L` | Nova Beverages - Rehydrate Label - 500ml | **12.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 2. `BOM-FG-REH-WATER-0.5L-12-15G-001` (PH - 500ml x 12 Pack)
- **Output**: **1.0 Pack** of `FG-REH-WATER-0.5L-12-15G`
- **Lineage**: Made from 15g bottle (`INT-BTL-REH-0.5L-15G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **6.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-REH-0.5L-15G` | Empty PET Bottle - Nova Rehydrate - 500ml (15g) | **12.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **12.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-REH-0.5L` | Nova Beverages - Rehydrate Label - 500ml | **12.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 3. `BOM-FG-REH-WATER-1.5L-06-27G-001` (PL - 1.5L x 6 Pack)
- **Output**: **1.0 Pack** of `FG-REH-WATER-1.5L-06-27G`
- **Lineage**: Made from 27g bottle (`INT-BTL-REH-1.5L-27G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **9.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-REH-1.5L-27G` | Empty PET Bottle - Nova Rehydrate - 1.5L (27g) | **6.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **6.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-REH-1.5L` | Nova Beverages - Rehydrate Label - 1.5L | **6.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 4. `BOM-FG-REH-WATER-1.5L-06-30G-001` (PH - 1.5L x 6 Pack)
- **Output**: **1.0 Pack** of `FG-REH-WATER-1.5L-06-30G`
- **Lineage**: Made from 30g bottle (`INT-BTL-REH-1.5L-30G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **9.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-REH-1.5L-30G` | Empty PET Bottle - Nova Rehydrate - 1.5L (30g) | **6.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **6.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-REH-1.5L` | Nova Beverages - Rehydrate Label - 1.5L | **6.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 5. `BOM-FG-REH-19L-REFILL-001` (19-Litre Commercial Bottle Refill)
- **Output**: **1.0 Nos** of `FG-REH-19L-REFILL`
- **Lineage**: Made from Standard Purchased 19L Bottle (Asset tracked in Customer Bottle Ledger)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **19.0** | Litre | 0.00 | 0.00 |
| 2 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **1.0** | Nos | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

---

### B. Hydrafina Pure Finished Goods (4 BOMs — PL & PH)

#### 6. `BOM-FG-HYD-WATER-PURE-0.5L-12-13.5G-001` (PL - 500ml x 12 Pack)
- **Output**: **1.0 Pack** of `FG-HYD-WATER-PURE-0.5L-12-13.5G`
- **Lineage**: Made from 13.5g bottle (`INT-BTL-HYD-PURE-0.5L-13.5G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **6.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-HYD-PURE-0.5L-13.5G` | Empty PET Bottle - Nova Hydrafina Pure - 500ml (13.5g) | **12.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **12.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-HYD-0.5L` | Nova Beverages - Hydrafina Label - 500ml | **12.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 7. `BOM-FG-HYD-WATER-PURE-0.5L-12-15G-001` (PH - 500ml x 12 Pack)
- **Output**: **1.0 Pack** of `FG-HYD-WATER-PURE-0.5L-12-15G`
- **Lineage**: Made from 15g bottle (`INT-BTL-HYD-PURE-0.5L-15G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **6.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-HYD-PURE-0.5L-15G` | Empty PET Bottle - Nova Hydrafina Pure - 500ml (15g) | **12.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **12.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-HYD-0.5L` | Nova Beverages - Hydrafina Label - 500ml | **12.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 8. `BOM-FG-HYD-WATER-PURE-1.5L-06-27G-001` (PL - 1.5L x 6 Pack)
- **Output**: **1.0 Pack** of `FG-HYD-WATER-PURE-1.5L-06-27G`
- **Lineage**: Made from 27g bottle (`INT-BTL-HYD-PURE-1.5L-27G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **9.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-HYD-PURE-1.5L-27G` | Empty PET Bottle - Nova Hydrafina Pure - 1.5L (27g) | **6.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **6.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-HYD-1.5L` | Nova Beverages - Hydrafina Label - 1.5L | **6.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 9. `BOM-FG-HYD-WATER-PURE-1.5L-06-30G-001` (PH - 1.5L x 6 Pack)
- **Output**: **1.0 Pack** of `FG-HYD-WATER-PURE-1.5L-06-30G`
- **Lineage**: Made from 30g bottle (`INT-BTL-HYD-PURE-1.5L-30G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **9.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-HYD-PURE-1.5L-30G` | Empty PET Bottle - Nova Hydrafina Pure - 1.5L (30g) | **6.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **6.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-HYD-1.5L` | Nova Beverages - Hydrafina Label - 1.5L | **6.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

---

### C. Hydrafina Mix Economy Finished Goods (4 BOMs — ML & MH)

#### 10. `BOM-FG-HYD-WATER-MIX-0.5L-12-13.5G-001` (ML - 500ml x 12 Pack)
- **Output**: **1.0 Pack** of `FG-HYD-WATER-MIX-0.5L-12-13.5G`
- **Lineage**: Made from 13.5g Mix bottle (`INT-BTL-HYD-MIX-0.5L-13.5G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **6.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-HYD-MIX-0.5L-13.5G` | Empty PET Bottle - Nova Hydrafina Mix - 500ml (13.5g) | **12.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **12.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-HYD-0.5L` | Nova Beverages - Hydrafina Label - 500ml | **12.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 11. `BOM-FG-HYD-WATER-MIX-0.5L-12-15G-001` (MH - 500ml x 12 Pack)
- **Output**: **1.0 Pack** of `FG-HYD-WATER-MIX-0.5L-12-15G`
- **Lineage**: Made from 15g Mix bottle (`INT-BTL-HYD-MIX-0.5L-15G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **6.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-HYD-MIX-0.5L-15G` | Empty PET Bottle - Nova Hydrafina Mix - 500ml (15g) | **12.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **12.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-HYD-0.5L` | Nova Beverages - Hydrafina Label - 500ml | **12.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-12X` | Shrink Wrap Film (12-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 12. `BOM-FG-HYD-WATER-MIX-1.5L-06-27G-001` (ML - 1.5L x 6 Pack)
- **Output**: **1.0 Pack** of `FG-HYD-WATER-MIX-1.5L-06-27G`
- **Lineage**: Made from 27g Mix bottle (`INT-BTL-HYD-MIX-1.5L-27G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **9.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-HYD-MIX-1.5L-27G` | Empty PET Bottle - Nova Hydrafina Mix - 1.5L (27g) | **6.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **6.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-HYD-1.5L` | Nova Beverages - Hydrafina Label - 1.5L | **6.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

#### 13. `BOM-FG-HYD-WATER-MIX-1.5L-06-30G-001` (MH - 1.5L x 6 Pack)
- **Output**: **1.0 Pack** of `FG-HYD-WATER-MIX-1.5L-06-30G`
- **Lineage**: Made from 30g Mix bottle (`INT-BTL-HYD-MIX-1.5L-30G`)

| # | Item Code | Item Name | Quantity | UOM | Rate | Amount |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | `INT-BULK-WATER` | Purified Mineral Water (Bulk) | **9.0** | Litre | 0.00 | 0.00 |
| 2 | `INT-BTL-HYD-MIX-1.5L-30G` | Empty PET Bottle - Nova Hydrafina Mix - 1.5L (30g) | **6.0** | Nos | 0.00 | 0.00 |
| 3 | `RM-CAP-28MM` | 28mm Standard Plastic Cap | **6.0** | Nos | 0.00 | 0.00 |
| 4 | `RM-LBL-HYD-1.5L` | Nova Beverages - Hydrafina Label - 1.5L | **6.0** | Nos | 0.00 | 0.00 |
| 5 | `RM-WRAP-06X` | Shrink Wrap Film (6-pack) | **1.0** | Unit | 0.00 | 0.00 |
| | **Total BOM Cost** | | | | | **Rs 0.00** |

---

## 5. Automated Python Provisioning Script for Production Server

Save this script as `setup_nova_boms.py` in your bench directory, then execute:
```bash
./env/bin/bench --site <site_name> execute setup_nova_boms.run
```

```python
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
                {"item_code": "RM-CAP-28MM", "qty": 1.0, "uom": "Nos"},
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

        # Deactivate any older BOMs for this item
        old_boms = frappe.get_all("BOM", filters={"item": item_code, "docstatus": 1})
        for ob in old_boms:
            frappe.db.set_value("BOM", ob.name, {"is_default": 0, "is_active": 0})

        # Create new BOM
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
        print(f"Created and activated BOM {doc.name} for {item_code}")

    # Ensure all rates in BOMs are clean 0.00 until purchases are booked
    frappe.db.sql("UPDATE `tabBOM Item` SET rate=0.0, amount=0.0, base_rate=0.0, base_amount=0.0")
    frappe.db.sql("UPDATE `tabBOM` SET raw_material_cost=0.0, total_cost=0.0, base_raw_material_cost=0.0, base_total_cost=0.0, rm_cost_as_per='Valuation Rate'")

    frappe.db.commit()
    print("All 26 Nova Beverages BOMs successfully configured on production!")
```
