import frappe
frappe.init(site="Wateena")
frappe.connect()

accs = frappe.get_all("Account", filters={"account_name": "Customer Bottle Deposits"})
for a in accs:
    doc = frappe.get_doc("Account", a.name)
    doc.account_type = ""
    doc.save(ignore_permissions=True)
frappe.db.commit()
print("Account fixed.")
def run():
    accs = frappe.get_all("Account", filters={"account_name": "Customer Bottle Deposits"})
    for a in accs:
        doc = frappe.get_doc("Account", a.name)
        doc.account_type = ""
        doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Account fixed.")
