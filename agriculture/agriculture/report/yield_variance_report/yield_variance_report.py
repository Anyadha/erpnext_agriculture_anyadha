# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe import _
from agriculture.agriculture.report_utils import build_grouped_chart, make_summary_item, sum_field


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
			"fieldname": "project",
			"label": _("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 200
		},
		{
			"fieldname": "farm",
			"label": _("Farm"),
			"fieldtype": "Link",
			"options": "Farm",
			"width": 150
		},
		{
			"fieldname": "field",
			"label": _("Field"),
			"fieldtype": "Link",
			"options": "Field",
			"width": 150
		},
		{
			"fieldname": "crop",
			"label": _("Crop"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"fieldname": "area",
			"label": _("Area"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "area_uom",
			"label": _("Area UOM"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "expected_yield",
			"label": _("Expected Yield"),
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "actual_yield",
			"label": _("Actual Yield"),
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "variance",
			"label": _("Variance"),
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "variance_percent",
			"label": _("Variance %"),
			"fieldtype": "Percent",
			"width": 100
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql(f"""
		SELECT
			p.name as project,
			p.farm,
			p.field,
			p.crop,
			p.area_under_cultivation as area,
			p.area_uom,
			p.expected_total_yield as expected_yield,
			p.actual_yield,
			(p.actual_yield - p.expected_total_yield) as variance,
			CASE
				WHEN p.expected_total_yield > 0
				THEN ((p.actual_yield - p.expected_total_yield) / p.expected_total_yield * 100)
				ELSE 0
			END as variance_percent,
			CASE
				WHEN p.actual_yield >= p.expected_total_yield THEN 'Above Target'
				WHEN p.actual_yield < p.expected_total_yield THEN 'Below Target'
				ELSE 'No Data'
			END as status
		FROM `tabProject` p
		WHERE p.docstatus < 2
			AND p.farm IS NOT NULL
			AND p.expected_total_yield > 0
			{conditions}
		ORDER BY p.expected_start_date DESC
	""", filters, as_dict=1)

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("farm"):
		conditions += " AND p.farm = %(farm)s"

	if filters.get("field"):
		conditions += " AND p.field = %(field)s"

	if filters.get("crop"):
		conditions += " AND p.crop = %(crop)s"

	if filters.get("from_date"):
		conditions += " AND p.expected_start_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND p.expected_end_date <= %(to_date)s"

	if filters.get("season"):
		conditions += " AND p.season = %(season)s"

	return conditions


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.project,
		[
			{"name": _("Expected Yield"), "value_getter": lambda row: row.expected_yield},
			{"name": _("Actual Yield"), "value_getter": lambda row: row.actual_yield},
		],
		colors=["#94A3B8", "#16A34A"],
		sort_index=1,
	)


def get_summary(data):
	total_expected_yield = sum_field(data, "expected_yield")
	total_actual_yield = sum_field(data, "actual_yield")
	total_variance = sum_field(data, "variance")

	return [
		make_summary_item(_("Projects"), len(data), "Int", "Blue"),
		make_summary_item(_("Expected Yield"), total_expected_yield, "Float", "Blue"),
		make_summary_item(_("Actual Yield"), total_actual_yield, "Float", "Green"),
		make_summary_item(
			_("Variance"),
			total_variance,
			"Float",
			"Green" if total_variance >= 0 else "Red",
		),
	]
