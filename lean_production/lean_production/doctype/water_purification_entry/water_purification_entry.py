# Copyright (c) 2026, Techxol and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import flt


class WaterPurificationEntry(Document):
	def before_validate(self):
		if self.get("good_qty") is None and getattr(self, "litres_purified", None) is not None:
			self.good_qty = flt(self.litres_purified)
		if self.get("good_qty") is not None and not getattr(self, "litres_purified", None):
			self.litres_purified = flt(self.good_qty)

	def validate(self):
		if self.get("good_qty") is None and getattr(self, "litres_purified", None) is not None:
			self.good_qty = flt(self.litres_purified)
		if self.get("good_qty") is not None and not getattr(self, "litres_purified", None):
			self.litres_purified = flt(self.good_qty)
