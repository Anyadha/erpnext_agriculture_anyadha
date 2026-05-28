# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from agriculture.agriculture.report_utils import (
	average_field,
	build_grouped_chart,
	count_unique,
	make_summary_item,
	sum_field,
)


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary


def get_columns():
	return [
		{
			"fieldname": "asset",
			"label": _("Equipment/Asset"),
			"fieldtype": "Link",
			"options": "Asset",
			"width": 200
		},
		{
			"fieldname": "asset_name",
			"label": _("Asset Name"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "farm",
			"label": _("Farm"),
			"fieldtype": "Link",
			"options": "Farm",
			"width": 150
		},
		{
			"fieldname": "total_hours",
			"label": _("Total Operating Hours"),
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "total_fuel",
			"label": _("Total Fuel Consumed"),
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "fuel_efficiency",
			"label": _("Fuel Efficiency (L/Hr)"),
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "utilization_days",
			"label": _("Days Used"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "avg_hours_per_day",
			"label": _("Avg Hours/Day"),
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Efficiency Status"),
			"fieldtype": "Data",
			"width": 120
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql(f"""
		SELECT
			eul.asset,
			a.asset_name,
			eul.farm,
			SUM(eul.hours_used) as total_hours,
			SUM(eul.fuel_consumed) as total_fuel,
			CASE
				WHEN SUM(eul.hours_used) > 0
				THEN SUM(eul.fuel_consumed) / SUM(eul.hours_used)
				ELSE 0
			END as fuel_efficiency,
			COUNT(DISTINCT eul.date) as utilization_days,
			CASE
				WHEN COUNT(DISTINCT eul.date) > 0
				THEN SUM(eul.hours_used) / COUNT(DISTINCT eul.date)
				ELSE 0
			END as avg_hours_per_day,
			CASE
				WHEN SUM(eul.hours_used) / COUNT(DISTINCT eul.date) >= 6 THEN 'High'
				WHEN SUM(eul.hours_used) / COUNT(DISTINCT eul.date) >= 4 THEN 'Medium'
				ELSE 'Low'
			END as status
		FROM `tabEquipment Usage Log` eul
		LEFT JOIN `tabAsset` a ON a.name = eul.asset
		WHERE eul.docstatus = 1
			{conditions}
		GROUP BY eul.asset, eul.farm
		ORDER BY total_hours DESC
	""", filters, as_dict=1)

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("farm"):
		conditions += " AND eul.farm = %(farm)s"

	if filters.get("asset"):
		conditions += " AND eul.asset = %(asset)s"

	if filters.get("from_date"):
		conditions += " AND eul.date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND eul.date <= %(to_date)s"

	return conditions


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.asset_name or row.asset,
		[{"name": _("Operating Hours"), "value_getter": lambda row: row.total_hours}],
		colors=["#0F766E"],
	)


def get_summary(data):
	return [
		make_summary_item(_("Assets"), count_unique(data, lambda row: row.asset), "Int", "Blue"),
		make_summary_item(_("Operating Hours"), sum_field(data, "total_hours"), "Float", "Green"),
		make_summary_item(_("Fuel Consumed"), sum_field(data, "total_fuel"), "Float", "Orange"),
		make_summary_item(_("Avg Hours/Day"), average_field(data, "avg_hours_per_day"), "Float", "Blue"),
	]
