import frappe

def fix_order(doctype):
    doc = frappe.get_doc("DocType", doctype)
    
    # Frappe has a method to sort fields based on their array index
    for i, df in enumerate(doc.fields):
        df.idx = i + 1
        
    # Calling doc.save() will update tabDocField
    doc.save()

frappe.init(site="Wateena", sites_path="sites")
frappe.connect()

fix_order("Water Purification Entry")
fix_order("Blow Molding Entry")
fix_order("Filling Entry")

frappe.db.commit()
