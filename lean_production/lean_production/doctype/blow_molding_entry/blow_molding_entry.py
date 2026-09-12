# Copyright (c) 2026, Techxol and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import flt


class BlowMoldingEntry(Document):
	def before_validate(self):
		if self.get("good_qty") is None and getattr(self, "bottles_produced_qty", None) is not None:
			self.good_qty = flt(self.bottles_produced_qty)
		if self.get("good_qty") is not None and not getattr(self, "bottles_produced_qty", None):
			self.bottles_produced_qty = flt(self.good_qty)

	def validate(self):
		if self.get("good_qty") is None and getattr(self, "bottles_produced_qty", None) is not None:
			self.good_qty = flt(self.bottles_produced_qty)
		if self.get("good_qty") is not None and not getattr(self, "bottles_produced_qty", None):
			self.bottles_produced_qty = flt(self.good_qty)
