# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Farm(Document):
	def validate(self):
		self.validate_cost_center()
		self.validate_warehouse()

	def validate_cost_center(self):
		"""Validate or create cost center for farm"""
		if not self.cost_center:
			# Auto-create cost center if not exists
			cost_center_name = f"{self.farm_name} - {self.company}"

			if not frappe.db.exists("Cost Center", cost_center_name):
				cost_center = frappe.get_doc({
					"doctype": "Cost Center",
					"cost_center_name": self.farm_name,
					"parent_cost_center": frappe.get_cached_value("Company", self.company, "cost_center"),
					"company": self.company,
					"is_group": 0
				})
				cost_center.insert(ignore_permissions=True)
				self.cost_center = cost_center.name
			else:
				self.cost_center = cost_center_name

	def validate_warehouse(self):
		"""Validate or create warehouse for farm"""
		if not self.parent_warehouse:
			# Auto-create warehouse if not exists
			warehouse_name = f"{self.farm_name} Warehouse - {frappe.get_cached_value('Company', self.company, 'abbr')}"

			if not frappe.db.exists("Warehouse", warehouse_name):
				warehouse = frappe.get_doc({
					"doctype": "Warehouse",
					"warehouse_name": f"{self.farm_name} Warehouse",
					"company": self.company,
					"is_group": 0
				})
				warehouse.insert(ignore_permissions=True)
				self.parent_warehouse = warehouse.name
			else:
				self.parent_warehouse = warehouse_name

	def on_update(self):
		"""Create child warehouses for farm"""
		self.create_child_warehouses()

	def create_child_warehouses(self):
		"""Create standard child warehouses for the farm"""
		if not self.parent_warehouse:
			return

		abbr = frappe.get_cached_value('Company', self.company, 'abbr')
		child_warehouses = [
			f"{self.farm_name} - Inputs Store",
			f"{self.farm_name} - Fuel Store",
			f"{self.farm_name} - Produce Store",
			f"{self.farm_name} - Fields"
		]

		for wh_name in child_warehouses:
			full_name = f"{wh_name} - {abbr}"
			if not frappe.db.exists("Warehouse", full_name):
				warehouse = frappe.get_doc({
					"doctype": "Warehouse",
					"warehouse_name": wh_name,
					"parent_warehouse": self.parent_warehouse,
					"company": self.company,
					"is_group": 0
				})
				warehouse.insert(ignore_permissions=True)
