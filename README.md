# Lean-Production
Mineral Water Plant Management & Streamlined Stage-Based Manufacturing

### Overview
**Lean Production** is a specialized Frappe Framework / ERPNext custom application built for mineral water purification, blow molding, filling lines, and circular 19L bottle ledger management.

### Installation
You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/Techxol-Enterprise/Lean-Production.git --branch main
bench --site [your-site-name] install-app lean_production
```

If updating an existing site where the app is already installed:
```bash
bench --site [your-site-name] migrate
```

### Key Modules & Features
1. **Poka-Yoke Stage-Based Production**:
   - `Water Purification Entry` (Bulk water batch logs, dry-weight chemical/mineral consumption, QC Pass/Fail gate)
   - `Blow Molding Entry` (Preform to bottle conversion with scrap calculation)
   - `Filling Entry` (BOM-driven packaging into finished goods with dynamic UOM)
2. **Circular 19L Bottle Ledger Tracking**:
   - Live customer deposit liabilities (`Customer Bottle Deposits`)
   - Automatic dispatch and return tracking (`Full Bottles Delivered` vs `Empty Bottles Received`)
   - `Bottles with Customers` Net Held balance report
3. **Automated Provisioning (Out of the Box)**:
   - **Lean Production Manager Role**: Auto-created with full CRUD + submit permissions on all stages and desk access.
   - **Item Group Hierarchy**: Automatically builds and indexes the nested-set tree (`Raw Material`, `Mineral Water`, `Semi Finished Goods`, `Finished Goods`).
   - **Security Deposits**: Auto-configures deposit ledger accounts, deposit item, and price lists.
4. **Lean Management Dashboard & Workspace**:
   - Tiered real-time production KPI Number Cards
   - Dynamic Stacked Bar Charts with live UOM detection and zero legend overlap

### Contributing
This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/lean_production
pre-commit install
```

Pre-commit is configured to use:
- ruff
- eslint
- prettier
- pyupgrade

### License
MIT
