# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
	"""Run after app installation"""
	create_agriculture_custom_fields()
	create_agriculture_roles()
	print("Agriculture app installed successfully!")


def create_agriculture_custom_fields():
	"""Create custom fields for ERPNext doctypes"""
	custom_fields = {
		"Project": [
			{
				"fieldname": "farm",
				"label": "Farm",
				"fieldtype": "Link",
				"options": "Farm",
				"insert_after": "department"
			},
			{
				"fieldname": "field",
				"label": "Field",
				"fieldtype": "Link",
				"options": "Field",
				"insert_after": "farm"
			},
			{
				"fieldname": "crop",
				"label": "Crop",
				"fieldtype": "Link",
				"options": "Item",
				"insert_after": "field"
			},
			{
				"fieldname": "season",
				"label": "Season",
				"fieldtype": "Select",
				"options": "\nRabi\nKharif\nZaid\nSummer\nWinter\nSpring\nFall",
				"insert_after": "crop"
			},
			{
				"fieldname": "agriculture_details_section",
				"label": "Agriculture Details",
				"fieldtype": "Section Break",
				"insert_after": "season",
				"collapsible": 1
			},
			{
				"fieldname": "area_under_cultivation",
				"label": "Area Under Cultivation",
				"fieldtype": "Float",
				"precision": "2",
				"insert_after": "agriculture_details_section"
			},
			{
				"fieldname": "area_uom",
				"label": "Area UOM",
				"fieldtype": "Link",
				"options": "UOM",
				"default": "Acre",
				"insert_after": "area_under_cultivation"
			},
			{
				"fieldname": "column_break_agri",
				"fieldtype": "Column Break",
				"insert_after": "area_uom"
			},
			{
				"fieldname": "expected_yield_per_unit",
				"label": "Expected Yield per Unit Area",
				"fieldtype": "Float",
				"precision": "2",
				"insert_after": "column_break_agri"
			},
			{
				"fieldname": "expected_total_yield",
				"label": "Expected Total Yield",
				"fieldtype": "Float",
				"precision": "2",
				"insert_after": "expected_yield_per_unit"
			},
			{
				"fieldname": "actual_yield",
				"label": "Actual Yield",
				"fieldtype": "Float",
				"precision": "2",
				"insert_after": "expected_total_yield",
				"read_only": 1
			}
		],
		"Stock Entry": [
			{
				"fieldname": "farm",
				"label": "Farm",
				"fieldtype": "Link",
				"options": "Farm",
				"insert_after": "company"
			},
			{
				"fieldname": "field",
				"label": "Field",
				"fieldtype": "Link",
				"options": "Field",
				"insert_after": "farm"
			}
		],
		"Timesheet": [
			{
				"fieldname": "farm",
				"label": "Farm",
				"fieldtype": "Link",
				"options": "Farm",
				"insert_after": "company"
			},
			{
				"fieldname": "field",
				"label": "Field",
				"fieldtype": "Link",
				"options": "Field",
				"insert_after": "farm"
			}
		],
		"Asset": [
			{
				"fieldname": "farm_details_section",
				"label": "Farm Details",
				"fieldtype": "Section Break",
				"insert_after": "calculate_depreciation",
				"collapsible": 1
			},
			{
				"fieldname": "farm",
				"label": "Farm",
				"fieldtype": "Link",
				"options": "Farm",
				"insert_after": "farm_details_section"
			},
			{
				"fieldname": "fuel_type",
				"label": "Fuel Type",
				"fieldtype": "Select",
				"options": "\nDiesel\nPetrol\nElectric\nN/A",
				"insert_after": "farm"
			},
			{
				"fieldname": "column_break_farm",
				"fieldtype": "Column Break",
				"insert_after": "fuel_type"
			},
			{
				"fieldname": "current_hour_meter_reading",
				"label": "Current Hour Meter Reading",
				"fieldtype": "Float",
				"precision": "2",
				"insert_after": "column_break_farm"
			},
			{
				"fieldname": "total_operating_hours",
				"label": "Total Operating Hours",
				"fieldtype": "Float",
				"precision": "2",
				"insert_after": "current_hour_meter_reading",
				"read_only": 1
			}
		],
		"Employee": [
			{
				"fieldname": "farm",
				"label": "Farm",
				"fieldtype": "Link",
				"options": "Farm",
				"insert_after": "branch"
			}
		]
	}

	create_custom_fields(custom_fields, update=True)


def create_agriculture_roles():
	"""Create Agriculture roles if they don't exist"""
	roles = ["Agriculture Manager", "Agriculture User"]

	for role in roles:
		if not frappe.db.exists("Role", role):
			frappe.get_doc({
				"doctype": "Role",
				"role_name": role,
				"desk_access": 1
			}).insert(ignore_permissions=True)

	frappe.db.commit()
