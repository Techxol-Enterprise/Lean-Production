import frappe

def create_bottle_ledger_entry(doc, method):
    if doc.get("full_bottles_delivered") or doc.get("empty_bottles_received"):
        ledger = frappe.get_doc({
            "doctype": "Customer Bottle Ledger",
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
