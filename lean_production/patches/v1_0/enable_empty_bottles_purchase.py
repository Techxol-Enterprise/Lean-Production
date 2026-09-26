import frappe


def execute():
    """
    Migration patch to:
    1. Mark all empty bottle items (INT-BTL-*) as purchase items (is_purchase_item = 1)
       so plants without blow molding or running out of preforms can purchase empty bottles
       directly via Purchase Order, Purchase Receipt, and Purchase Invoice.
    2. Ensure INT-BULK-WATER has a non-zero default valuation_rate (0.50) if not set.
    """
    # 1. Update Empty Bottles to be purchase items
    frappe.db.sql("""
        UPDATE `tabItem`
        SET is_purchase_item = 1
        WHERE name LIKE 'INT-BTL%'
    """)

    # 2. Update INT-BULK-WATER baseline valuation rate if 0
    frappe.db.sql("""
        UPDATE `tabItem`
        SET valuation_rate = 0.50
        WHERE name = 'INT-BULK-WATER' AND (valuation_rate IS NULL OR valuation_rate <= 0)
    """)

    frappe.db.commit()
