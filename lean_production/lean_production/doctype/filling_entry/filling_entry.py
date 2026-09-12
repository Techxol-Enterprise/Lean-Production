# Copyright (c) 2026, Techxol and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import flt


class FillingEntry(Document):
	def before_validate(self):
		if self.get("good_qty") is None and getattr(self, "cartons_produced", None) is not None:
			self.good_qty = flt(self.cartons_produced)
		if self.get("good_qty") is not None and not getattr(self, "cartons_produced", None):
			self.cartons_produced = flt(self.good_qty)

	def validate(self):
		if self.get("good_qty") is None and getattr(self, "cartons_produced", None) is not None:
			self.good_qty = flt(self.cartons_produced)
		if self.get("good_qty") is not None and not getattr(self, "cartons_produced", None):
			self.cartons_produced = flt(self.good_qty)
