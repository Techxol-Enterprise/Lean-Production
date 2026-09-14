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

### Contributing
This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/lean_production
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:
- ruff
- eslint
- prettier
- pyupgrade

### License
MIT
