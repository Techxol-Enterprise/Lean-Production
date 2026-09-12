import frappe

def create_bottle_ledger_entry(doc, method):
    if doc.get("full_bottles_delivered") or doc.get("empty_bottles_received"):
        company = doc.get("company") or frappe.defaults.get_user_default("Company")
        ledger = frappe.get_doc({
            "doctype": "Customer Bottle Ledger",
            "company": company,
            "customer": doc.customer,
            "posting_date": doc.posting_date,
            "voucher_type": doc.doctype,
            "voucher_no": doc.name,
            "full_bottles_delivered": doc.full_bottles_delivered or 0,
            "empty_bottles_received": doc.empty_bottles_received or 0
        })
        ledger.insert(ignore_permissions=True)

def cancel_bottle_ledger_entry(doc, method):
    ledgers = frappe.get_all("Customer Bottle Ledger", filters={
        "voucher_type": doc.doctype,
        "voucher_no": doc.name
    })
    for l in ledgers:
        frappe.delete_doc("Customer Bottle Ledger", l.name, ignore_permissions=True)

def on_transaction_deletion_record_submit(doc, method):
    """
    Hook called when a Transaction Deletion Record is submitted.
    Ensures all Customer Bottle Ledger transactions belonging to the target company
    and any orphaned records are thoroughly wiped out.
    """
    if not doc.company:
        return

    # Delete records explicitly tied to the target company
    frappe.db.delete("Customer Bottle Ledger", {"company": doc.company})

    # Clean up any orphaned ledger rows where company is NULL/blank or referencing non-existent vouchers
    frappe.db.sql("""
        DELETE FROM `tabCustomer Bottle Ledger`
        WHERE company IS NULL
           OR company = ''
           OR (voucher_type = 'Sales Invoice' AND voucher_no NOT IN (SELECT name FROM `tabSales Invoice`))
    """)

    # Reset sequence counter if table is empty
    remaining = frappe.db.count("Customer Bottle Ledger")
    if remaining == 0:
        try:
            frappe.db.sql("ALTER SEQUENCE customer_bottle_ledger_id_seq RESTART WITH 1;")
        except Exception:
            pass
