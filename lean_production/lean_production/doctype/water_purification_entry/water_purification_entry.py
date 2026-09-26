# Copyright (c) 2026, Techxol and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class WaterPurificationEntry(Document):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.docstatus == 0 and self.amended_from:
			self.stock_entry = None

	def _set_defaults(self):
		if self.docstatus == 0 and self.amended_from:
			self.stock_entry = None
		super()._set_defaults()

	def before_insert(self):
		if self.amended_from:
			self.stock_entry = None

	def before_validate(self):
		if self.docstatus == 0 and self.amended_from and self.stock_entry:
			if frappe.db.get_value("Stock Entry", self.stock_entry, "docstatus") == 2:
				self.stock_entry = None

		if self.get("good_qty") is None and getattr(self, "litres_purified", None) is not None:
			self.good_qty = flt(self.litres_purified)
		if self.get("good_qty") is not None and not getattr(self, "litres_purified", None):
			self.litres_purified = flt(self.good_qty)

	def validate(self):
		if self.get("good_qty") is None and getattr(self, "litres_purified", None) is not None:
			self.good_qty = flt(self.litres_purified)
		if self.get("good_qty") is not None and not getattr(self, "litres_purified", None):
			self.litres_purified = flt(self.good_qty)
