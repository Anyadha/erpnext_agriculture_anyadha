# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe import _
from agriculture.agriculture.report_utils import build_grouped_chart, count_unique, make_summary_item, sum_field



def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data, filters)
	summary = get_summary(data)
	return columns, data, None, chart, summary


def get_columns():
	return [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 100},
		{"label": _("Asset"), "fieldname": "asset", "fieldtype": "Link", "options": "Asset", "width": 150},
		{"label": _("Asset Name"), "fieldname": "asset_name", "fieldtype": "Data", "width": 150},
		{"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 130},
		{"label": _("Field"), "fieldname": "field", "fieldtype": "Link", "options": "Field", "width": 130},
		{"label": _("Project"), "fieldname": "crop_project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Operator"), "fieldname": "operator", "fieldtype": "Link", "options": "Employee", "width": 130},
		{"label": _("Hours Used"), "fieldname": "hours_used", "fieldtype": "Float", "width": 100},
		{"label": _("Fuel Consumed"), "fieldname": "fuel_consumed", "fieldtype": "Float", "width": 110},
		{"label": _("Fuel Cost"), "fieldname": "fuel_cost", "fieldtype": "Currency", "width": 110},
		{"label": _("Total Cost"), "fieldname": "total_operating_cost", "fieldtype": "Currency", "width": 120},
		{"label": _("Document"), "fieldname": "name", "fieldtype": "Link", "options": "Equipment Usage Log", "width": 130}
	]


def get_data(filters):
	conditions = []
	if filters.get("farm"):
		conditions.append("AND farm = %(farm)s")
	if filters.get("field"):
		conditions.append("AND field = %(field)s")
	if filters.get("asset"):
		conditions.append("AND asset = %(asset)s")
	if filters.get("from_date"):
		conditions.append("AND date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("AND date <= %(to_date)s")

	conditions_str = " ".join(conditions)

	data = frappe.db.sql(f"""
		SELECT
			date,
			asset,
			asset_name,
			farm,
			field,
			crop_project,
			operator,
			hours_used,
			fuel_consumed,
			fuel_cost,
			total_operating_cost,
			name
		FROM
			`tabEquipment Usage Log`
		WHERE
			docstatus = 1
			{conditions_str}
		ORDER BY
			date DESC
	""", filters, as_dict=1)

	return data


def get_chart_data(data, filters):
	return build_grouped_chart(
		data,
		lambda row: row.asset_name or row.asset,
		[{"name": _("Hours Used"), "value_getter": lambda row: row.hours_used}],
		colors=["#7575FF"],
	)


def get_summary(data):
	return [
		make_summary_item(_("Usage Logs"), len(data), "Int", "Blue"),
		make_summary_item(_("Assets"), count_unique(data, lambda row: row.asset), "Int", "Blue"),
		make_summary_item(_("Hours Used"), sum_field(data, "hours_used"), "Float", "Green"),
		make_summary_item(_("Operating Cost"), sum_field(data, "total_operating_cost"), "Currency", "Orange"),
	]
