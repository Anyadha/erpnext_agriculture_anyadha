# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
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
			"fieldname": "crop",
			"label": _("Crop"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"fieldname": "total_budgeted_cost",
			"label": _("Budgeted Cost"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "total_actual_cost",
			"label": _("Actual Cost"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "variance",
			"label": _("Variance"),
			"fieldtype": "Currency",
			"width": 150
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
			p.crop,
			p.estimated_costing as total_budgeted_cost,
			p.total_costing_amount as total_actual_cost,
			(p.total_costing_amount - p.estimated_costing) as variance,
			CASE
				WHEN p.estimated_costing > 0
				THEN ((p.total_costing_amount - p.estimated_costing) / p.estimated_costing * 100)
				ELSE 0
			END as variance_percent,
			CASE
				WHEN p.total_costing_amount <= p.estimated_costing THEN 'Within Budget'
				WHEN p.total_costing_amount > p.estimated_costing THEN 'Over Budget'
				ELSE 'No Data'
			END as status
		FROM `tabProject` p
		WHERE p.docstatus < 2
			AND p.farm IS NOT NULL
			AND p.estimated_costing > 0
			{conditions}
		ORDER BY variance DESC
	""", filters, as_dict=1)

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("farm"):
		conditions += " AND p.farm = %(farm)s"

	if filters.get("crop"):
		conditions += " AND p.crop = %(crop)s"

	if filters.get("from_date"):
		conditions += " AND p.expected_start_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND p.expected_end_date <= %(to_date)s"

	return conditions


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.project,
		[
			{"name": _("Budgeted Cost"), "value_getter": lambda row: row.total_budgeted_cost},
			{"name": _("Actual Cost"), "value_getter": lambda row: row.total_actual_cost},
		],
		colors=["#64748B", "#B91C1C"],
		sort_index=1,
	)


def get_summary(data):
	total_budgeted_cost = sum_field(data, "total_budgeted_cost")
	total_actual_cost = sum_field(data, "total_actual_cost")
	total_variance = sum_field(data, "variance")

	return [
		make_summary_item(_("Projects"), len(data), "Int", "Blue"),
		make_summary_item(_("Budgeted Cost"), total_budgeted_cost, "Currency", "Blue"),
		make_summary_item(_("Actual Cost"), total_actual_cost, "Currency", "Orange"),
		make_summary_item(
			_("Variance"),
			total_variance,
			"Currency",
			"Green" if total_variance <= 0 else "Red",
		),
	]
