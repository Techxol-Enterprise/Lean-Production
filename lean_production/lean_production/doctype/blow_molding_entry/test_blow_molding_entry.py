# Copyright (c) 2026, Techxol and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from lean_production.verify_mes_filling_stock import run_mes_blow_molding_test


class IntegrationTestBlowMoldingEntry(IntegrationTestCase):
	"""
	Integration tests for BlowMoldingEntry.
	Verifies MES stock automation, child table material consumption,
	scrap absorption, and two-way cancellation integrity.
	"""

	def test_mes_blow_molding_stock(self):
		run_mes_blow_molding_test()
