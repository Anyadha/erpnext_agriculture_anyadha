# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FieldOperationLog(Document):
	def on_submit(self):
		"""Update field status based on operation type"""
		self.update_field_status()

	def update_field_status(self):
		"""Update field current status based on operation"""
		if not self.field:
			return

		field = frappe.get_doc("Field", self.field)

		status_map = {
			"Land Preparation": "Under Preparation",
			"Sowing": "Sown",
			"Transplanting": "Sown",
			"Harvest": "Harvested"
		}

		if self.operation_type in status_map:
			field.current_status = status_map[self.operation_type]

			if self.operation_type in ["Sowing", "Transplanting"]:
				if self.crop_project:
					project = frappe.get_doc("Project", self.crop_project)
					field.current_crop = project.get("crop")
					field.current_crop_project = self.crop_project
					field.current_status = "Growing"

			field.save(ignore_permissions=True)
