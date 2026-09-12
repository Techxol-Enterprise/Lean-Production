import frappe

def reproduce():
    # 1. Check if Customer Bottle Ledger has records that were left behind
    count = frappe.db.count("Customer Bottle Ledger")
    print(f"Current Customer Bottle Ledger count: {count}")
    
    # 2. Check if Customer Bottle Ledger has a company field in DocType
    meta = frappe.get_meta("Customer Bottle Ledger")
    has_company = meta.has_field("company")
    print(f"Customer Bottle Ledger has 'company' field: {has_company}")
    
    # 3. Check if Transaction Deletion Record discovers Customer Bottle Ledger
    tdr = frappe.new_doc("Transaction Deletion Record")
    tdr.company = "Wateena"
    tdr.generate_to_delete_list()
    
    discovered = any(d.doctype_name == "Customer Bottle Ledger" for d in tdr.doctypes_to_delete)
    print(f"TDR discovered Customer Bottle Ledger in To Delete list: {discovered}")
    
    if count > 0 and not has_company and not discovered:
        print("REPRODUCTION CONFIRMED (FAIL STATE): Customer Bottle Ledger lacks company field, was ignored by TDR, and has orphaned residual records.")
        return False
    else:
        print("PASS STATE: Customer Bottle Ledger is properly linked and handled.")
        return True
