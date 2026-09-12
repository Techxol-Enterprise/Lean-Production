import frappe

def fix_charts():
    charts = frappe.get_all("Dashboard Chart", filters={"module": "Lean Production"}, fields=["name", "document_type", "based_on", "value_based_on"])
    
    for chart in charts:
        # The quantitative field was incorrectly put into based_on
        quant_field = chart.based_on
        if not quant_field and chart.name != "Downtime Root Cause Analysis":
            continue
            
        doc = frappe.get_doc("Dashboard Chart", chart.name)
        
        # Set the date field for timeseries
        if doc.document_type == "Sales Invoice Item":
            doc.based_on = "creation"
        else:
            doc.based_on = "posting_date"
            
        # Set the quantitative value field if applicable
        if quant_field:
            doc.value_based_on = quant_field
            
        # Ensure it is a time series chart
        doc.timespan = "Last Year"
        
        doc.save(ignore_permissions=True)
        
    frappe.db.commit()
    print("Dashboard charts configuration fixed.")

fix_charts()
