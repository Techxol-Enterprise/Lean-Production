import frappe
from lean_production.setup_item_groups import setup_lean_item_groups


def execute():
    """
    Migration patch to ensure Lean Production Item Group hierarchy is
    consistently provisioned across existing sites.
    """
    setup_lean_item_groups()
