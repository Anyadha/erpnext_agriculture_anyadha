# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class EquipmentUsageLog(Document):
	def validate(self):
		self.calculate_hours_and_distance()
		self.calculate_total_cost()

	def calculate_hours_and_distance(self):
		"""Calculate hours used and distance from meter readings"""
		if self.start_hour_meter_reading and self.end_hour_meter_reading:
			self.hours_used = flt(self.end_hour_meter_reading) - flt(self.start_hour_meter_reading)

		if self.odometer_start and self.odometer_end:
			self.distance_km = flt(self.odometer_end) - flt(self.odometer_start)

	def calculate_total_cost(self):
		"""Calculate total operating cost"""
		if self.hours_used and self.operating_cost_per_hour:
			self.total_operating_cost = flt(self.hours_used) * flt(self.operating_cost_per_hour)

	def on_submit(self):
		"""Create fuel stock entry and update asset"""
		if self.fuel_consumed:
			self.create_fuel_stock_entry()
		self.update_asset_hours()

	def create_fuel_stock_entry(self):
		"""Create stock entry for fuel consumption"""
		if self.fuel_stock_entry:
			return  # Already created

		# Get fuel item from asset or use default
		fuel_item = self.get_fuel_item()
		if not fuel_item:
			return

		farm_doc = frappe.get_doc("Farm", self.farm) if self.farm else None
		company = farm_doc.company if farm_doc else frappe.defaults.get_user_default("Company")

		stock_entry = frappe.get_doc({
			"doctype": "Stock Entry",
			"stock_entry_type": "Material Issue",
			"posting_date": self.date,
			"company": company,
			"project": self.crop_project,
			"items": [{
				"item_code": fuel_item,
				"qty": self.fuel_consumed,
				"uom": self.fuel_uom or "Litre",
				"s_warehouse": self.get_fuel_warehouse(),
				"cost_center": farm_doc.cost_center if farm_doc else None
			}]
		})

		stock_entry.insert(ignore_permissions=True)
		stock_entry.submit()

		self.db_set("fuel_stock_entry", stock_entry.name)

	def get_fuel_item(self):
		"""Get fuel item code based on asset fuel type"""
		# This is a placeholder - you would configure this based on your setup
		fuel_type = frappe.get_cached_value("Asset", self.asset, "fuel_type")

		if fuel_type == "Diesel":
			return "FUEL-DIESEL"  # Configure actual item code
		elif fuel_type == "Petrol":
			return "FUEL-PETROL"
		return None

	def get_fuel_warehouse(self):
		"""Get fuel warehouse for the farm"""
		if self.farm:
			farm = frappe.get_doc("Farm", self.farm)
			# Try to find fuel store child warehouse
			warehouses = frappe.get_all("Warehouse",
				filters={"parent_warehouse": farm.parent_warehouse, "warehouse_name": ["like", "%Fuel%"]},
				pluck="name")
			if warehouses:
				return warehouses[0]
			return farm.parent_warehouse
		return None

	def update_asset_hours(self):
		"""Update total operating hours on asset"""
		if self.asset and self.hours_used:
			asset = frappe.get_doc("Asset", self.asset)
			current_hours = flt(asset.get("total_operating_hours") or 0)
			asset.db_set("total_operating_hours", current_hours + flt(self.hours_used))
