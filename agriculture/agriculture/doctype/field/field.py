# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate


class Field(Document):
	def validate(self):
		self.calculate_days_vacant()

	def calculate_days_vacant(self):
		"""Calculate days vacant if field is vacant"""
		if self.current_status == "Vacant" and self.last_harvest_date:
			self.days_vacant = date_diff(getdate(), self.last_harvest_date)
		else:
			self.days_vacant = 0
