import frappe

def main():
    frappe.init(site="Wateena", sites_path="sites")
    frappe.connect()

    for dt in ["Water Purification Entry", "Blow Molding Entry", "Filling Entry"]:
        doc = frappe.get_doc("DocType", dt)
        doc.custom = 0
        doc.save(ignore_permissions=True)
    frappe.db.commit()

main()
