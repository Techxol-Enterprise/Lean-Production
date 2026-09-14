import frappe
from lean_production.setup_roles import setup_lean_roles


def execute():
    """
    Migration patch to ensure 'Lean Production Manager' role is created,
    configured with full permissions, and assigned to Administrator.
    """
    setup_lean_roles()
