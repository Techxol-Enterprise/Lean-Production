# Copyright (c) 2026, Techxol and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from lean_production.verify_mes_filling_stock import run_mes_filling_test


class IntegrationTestFillingEntry(IntegrationTestCase):
	"""
	Integration tests for FillingEntry.
	Verifies MES stock automation, child table material consumption,
	scrap absorption into FG valuation, and two-way cancellation integrity.
	"""

	def test_mes_filling_stock_automation(self):
		result = run_mes_filling_test()
		self.assertEqual(result, "PASS")
