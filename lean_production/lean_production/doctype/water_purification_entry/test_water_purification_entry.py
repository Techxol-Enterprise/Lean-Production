# Copyright (c) 2026, Techxol and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from lean_production.verify_purification_stock import run_test
from lean_production.verify_mes_filling_stock import run_mes_purification_test


class IntegrationTestWaterPurificationEntry(IntegrationTestCase):
	"""
	Integration tests for WaterPurificationEntry.
	Verifies dry-weight mineral consumption, MES child table consumption,
	scrap absorption, and two-way cancellation integrity.
	"""

	def test_legacy_purification_stock(self):
		result = run_test()
		self.assertEqual(result, "PASS")

	def test_mes_purification_stock(self):
		run_mes_purification_test()
