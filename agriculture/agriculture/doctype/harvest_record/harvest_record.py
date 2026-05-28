# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate


class HarvestRecord(Document):
	def validate(self):
		self.calculate_yield_per_area()
		self.calculate_team_amounts()

	def calculate_yield_per_area(self):
		"""Calculate actual yield per unit area"""
		if self.quantity_harvested and self.area_harvested:
			self.actual_yield_per_unit_area = flt(self.quantity_harvested) / flt(self.area_harvested)

	def calculate_team_amounts(self):
		"""Calculate amount for each team member"""
		for member in self.harvest_team:
			if member.hours and member.rate:
				member.amount = flt(member.hours) * flt(member.rate)

	def on_submit(self):
		"""Create stock entry on submit"""
		self.create_stock_entry()
		self.update_project_yield()
		self.update_field_status()

	def create_stock_entry(self):
		"""Create stock entry for harvested produce"""
		if self.stock_entry:
			return  # Already created

		# Get project costs for valuation
		valuation_rate = self.get_project_cost_per_unit()

		stock_entry = frappe.get_doc({
			"doctype": "Stock Entry",
			"stock_entry_type": "Manufacture",
			"posting_date": self.harvest_date,
			"company": frappe.get_cached_value("Farm", self.farm, "company"),
			"project": self.crop_project,
			"items": []
		})

		# Add items based on grade distribution
		if self.grade_distribution:
			for grade in self.grade_distribution:
				if grade.quantity > 0:
					stock_entry.append("items", {
						"item_code": grade.item_code or self.crop,
						"qty": grade.quantity,
						"uom": self.uom,
						"t_warehouse": self.target_warehouse,
						"basic_rate": valuation_rate,
						"cost_center": frappe.get_cached_value("Farm", self.farm, "cost_center"),
						"batch_no": self.batch_no or "",
						"allow_zero_valuation_rate": 1 if not valuation_rate else 0
					})
		else:
			# No grading, single entry
			stock_entry.append("items", {
				"item_code": self.crop,
				"qty": self.quantity_harvested,
				"uom": self.uom,
				"t_warehouse": self.target_warehouse,
				"basic_rate": valuation_rate,
				"cost_center": frappe.get_cached_value("Farm", self.farm, "cost_center"),
				"allow_zero_valuation_rate": 1 if not valuation_rate else 0
			})

		stock_entry.insert(ignore_permissions=True)
		stock_entry.submit()

		self.db_set("stock_entry", stock_entry.name)
		frappe.msgprint(f"Stock Entry {stock_entry.name} created successfully")

	def get_project_cost_per_unit(self):
		"""Calculate cost per unit from project"""
		if not self.crop_project:
			return 0

		# Get total project costs
		total_cost = frappe.db.sql("""
			SELECT SUM(total_costing_amount)
			FROM `tabProject`
			WHERE name = %s
		""", self.crop_project)[0][0] or 0

		if total_cost and self.quantity_harvested:
			return flt(total_cost) / flt(self.quantity_harvested)

		return 0

	def update_project_yield(self):
		"""Update actual yield in project"""
		if self.crop_project:
			project = frappe.get_doc("Project", self.crop_project)
			project.db_set("actual_yield", self.quantity_harvested)

	def update_field_status(self):
		"""Update field status to harvested"""
		if self.field:
			field = frappe.get_doc("Field", self.field)
			field.current_status = "Harvested"
			field.last_harvest_date = self.harvest_date
			field.last_crop = self.crop

			# Add to crop history
			field.append("crop_rotation_history", {
				"year": frappe.utils.getdate(self.harvest_date).year,
				"season": frappe.get_cached_value("Project", self.crop_project, "season") if self.crop_project else "",
				"crop": self.crop,
				"harvest_date": self.harvest_date,
				"yield_per_unit_area": self.actual_yield_per_unit_area,
				"total_yield": self.quantity_harvested
			})

			field.save(ignore_permissions=True)
