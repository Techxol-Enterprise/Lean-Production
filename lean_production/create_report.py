import frappe

def run():
    if not frappe.db.exists("Report", "Bottles with Customers"):
        doc = frappe.get_doc({
            "doctype": "Report",
            "report_name": "Bottles with Customers",
            "ref_doctype": "Customer Bottle Ledger",
            "report_type": "Query Report",
            "is_standard": "Yes",
            "module": "Lean Production",
            "query": """
SELECT 
    customer AS "Customer:Link/Customer:200", 
    SUM(full_bottles_delivered) AS "Total Given:Int:120", 
    SUM(empty_bottles_received) AS "Total Returned:Int:120",
    SUM(full_bottles_delivered) - SUM(empty_bottles_received) AS "Net Bottles Held:Int:150"
FROM 
    `tabCustomer Bottle Ledger`
GROUP BY 
    customer
ORDER BY 
    "Net Bottles Held:Int:150" DESC
            """
        })
        doc.insert(ignore_permissions=True)
        print("Report Created.")
    frappe.db.commit()
