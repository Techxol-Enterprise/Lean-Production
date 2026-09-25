import frappe
from lean_production.setup_bottle_tracking import add_custom_fields


def execute():
    """
    Migration patch to ensure 19L Returnable Bottle Tracking custom fields
    (bottle_tracking_section, full_bottles_delivered, empty_bottles_received)
    are provisioned on Sales Invoice.
    """
    add_custom_fields()
