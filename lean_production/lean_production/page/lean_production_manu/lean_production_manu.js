frappe.pages['lean-production-manu'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Lean Production Manual',
		single_column: true
	});
	
	const markdown_content = `
# Lean Production - User Manual

Welcome to the **Lean Production** application. This custom app is designed to replace complex ERP manufacturing (Work Orders, Job Cards) with simple, flat-screen entry forms for floor operators, while maintaining strict backend accounting and inventory control.

This manual covers the two core modules of the app: **Plant Manufacturing** and **19L Bottle Delivery Tracking**.

---

## Module 1: Plant Manufacturing

The plant floor operates in three distinct stages. To prevent mistakes, the system features a "Poka-Yoke" (Mistake-Proofing) design: operators can only select items belonging to the correct stage. 

### Stage 1: Water Purification Entry
*   **Purpose:** Logs the purification of raw water into bulk mineral water.
*   **Item Selection:** Restricted to the \`Mineral Water\` group (e.g., *Bulk Purified Water*).
*   **Workflow:**
    1. Select the Operator and Workstation.
    2. Enter the **Good Qty** (Litres successfully purified) and **Scrap Qty** (Litres wasted).
    3. The system dynamically reads the Bill of Materials (BOM) and populates the **Material Consumption** table.
    4. You can adjust the **Source Warehouse** for the chemicals/minerals being consumed (measured in exact dry Kg/Grams).
    5. **Submit**. The system automatically generates a Stock Entry to consume the chemicals and increase your Bulk Purified Water stock.

### Stage 2: Blow Molding Entry
*   **Purpose:** Logs the melting of Preforms into Empty PET Bottles.
*   **Item Selection:** Restricted to the \`Semi Finished Goods\` group (e.g., *Empty Bottles*).
*   **Workflow:**
    1. Select the Bottle Item. 
    2. Enter **Good Qty** and **Scrap Qty**. 
    3. The system calculates how many Preforms are required. Select the warehouse holding your Preforms.
    4. **Submit**.

### Stage 3: Filling Entry
*   **Purpose:** Logs the filling of bottles, capping, and wrapping into the final salable product.
*   **Item Selection:** Restricted to the \`Finished Goods\` group.
*   **Workflow:**
    1. Select the final packed item (e.g., *Bottled Water 1.5L x 6 Pack*).
    2. Enter **Good Qty** and **Scrap Qty**.
    3. The system automatically pulls the requirements for Bulk Water, Empty Bottles, Caps, Labels, and Shrink Wrap.
    4. **Submit**. The Finished Goods warehouse is instantly updated and ready for dispatch.

---

## Module 2: 19L Returnable Bottle Tracking

This module tracks the expensive 19L physical empty bottles currently sitting with your customers, without forcing drivers to scan serial numbers or create warehouse transfers.

### Scenario A: Delivering to a New Customer (Deposit Required)
When a customer requests a 19L bottle for the first time, you must charge them a security deposit.
1. Create a **Sales Invoice**.
2. Add the item \`19L Mineral Water (Refill)\` and charge for the water.
3. Add the item \`19L Bottle Security Deposit\`. The system will automatically charge the standard deposit rate.
4. Scroll down to the **Bottle Tracking (19L)** section.
5. Set \`Full Bottles Delivered\` to **1**.
6. Set \`Empty Bottles Received\` to **0**.
7. **Submit**. The system automatically records that this customer owes you 1 empty bottle, and logs the liability.

### Scenario B: Refill Delivery (Exchange)
When a driver delivers a full bottle and takes back the empty one.
1. Create a **Sales Invoice**.
2. Add the item \`19L Mineral Water (Refill)\` and charge for the water. Do **NOT** add the Security Deposit item.
3. Scroll down to the **Bottle Tracking (19L)** section.
4. Set \`Full Bottles Delivered\` to **1**.
5. Set \`Empty Bottles Received\` to **1**.
6. **Submit**. The customer's bottle balance remains unchanged.

### Scenario C: VIP / Waived Deposit
If management authorizes a free bottle (no deposit cash collected):
1. Follow the steps for *Scenario A* and add the \`19L Bottle Security Deposit\` item.
2. In the Item table, expand the row and apply a **100% Discount** to the Deposit item.
3. **Submit**. The customer is given the bottle, the tracking ledger is updated, but no cash is collected.

### End of Day: Physical Bottle Restocking
Because the driver's Sales Invoice only tracks the *customer's* bottle balance, the physical empty bottles returning to the plant must be logged into stock.
*   **Workflow:** At the end of the shift, the Warehouse Manager counts all empty bottles in the truck and creates a single standard **Stock Entry (Material Receipt)** to receive the total count of \`Empty 19L Bottles\` back into the Main Warehouse.

---

## Module 3: Reporting & Analytics

Management can monitor the entire operation using three core methods:

1. **"Bottles with Customers" Report:**
   *   Search for this custom report in the top search bar.
   *   It displays every customer, the total bottles given to them, the total returned, and their **Net Bottles Held** balance.
   
2. **Security Deposits Audit:**
   *   Open the standard **General Ledger**.
   *   Filter by the \`Customer Bottle Deposits\` account and group by Party (Customer).
   *   This shows exactly how much deposit cash the company is holding as a liability for each customer.

3. **Waived Deposits Audit:**
   *   Open the **Sales Invoice Trend** (or standard Sales Register).
   *   Filter for invoices containing the \`19L Bottle Security Deposit\` item where the \`Discount % = 100\`.
   *   This allows management to audit all "free" bottles given out by drivers.
	`;
	
	$(frappe.markdown(markdown_content)).appendTo(page.main);
}
