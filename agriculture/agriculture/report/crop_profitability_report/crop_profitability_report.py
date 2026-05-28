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
		{"label": _("Project"), "fieldname": "name", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 150},
		{"label": _("Field"), "fieldname": "field", "fieldtype": "Link", "options": "Field", "width": 150},
		{"label": _("Crop"), "fieldname": "crop", "fieldtype": "Data", "width": 130},
		{"label": _("Season"), "fieldname": "season", "fieldtype": "Data", "width": 100},
		{"label": _("Area"), "fieldname": "area_under_cultivation", "fieldtype": "Float", "width": 100},
		{"label": _("Expected Yield"), "fieldname": "expected_total_yield", "fieldtype": "Float", "width": 120},
		{"label": _("Actual Yield"), "fieldname": "actual_yield", "fieldtype": "Float", "width": 120},
		{"label": _("Total Cost"), "fieldname": "total_costing_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Revenue"), "fieldname": "total_sales_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Gross Profit"), "fieldname": "gross_profit", "fieldtype": "Currency", "width": 130},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100}
	]


def get_data(filters):
	conditions = []
	if filters.get("farm"):
		conditions.append("AND farm = %(farm)s")
	if filters.get("crop"):
		conditions.append("AND crop_item = %(crop)s")
	if filters.get("season"):
		conditions.append("AND season = %(season)s")

	conditions_str = " ".join(conditions)

	data = frappe.db.sql(f"""
		SELECT
			name,
			farm,
			field,
			crop_item as crop,
			season,
			area_under_cultivation,
			expected_total_yield,
			actual_yield,
			total_costing_amount,
			total_sales_amount,
			(COALESCE(total_sales_amount, 0) - COALESCE(total_costing_amount, 0)) as gross_profit,
			status
		FROM
			`tabProject`
		WHERE
			project_type = 'External'
			AND farm IS NOT NULL
			{conditions_str}
		ORDER BY
			name DESC
	""", filters, as_dict=1)

	return data


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.crop or row.name,
		[{"name": _("Gross Profit"), "value_getter": lambda row: row.gross_profit}],
		colors=["#15803D"],
	)


def get_summary(data):
	total_revenue = sum_field(data, "total_sales_amount")
	total_cost = sum_field(data, "total_costing_amount")
	total_gross_profit = sum_field(data, "gross_profit")

	return [
		make_summary_item(_("Projects"), len(data), "Int", "Blue"),
		make_summary_item(_("Revenue"), total_revenue, "Currency", "Green"),
		make_summary_item(_("Total Cost"), total_cost, "Currency", "Orange"),
		make_summary_item(
			_("Gross Profit"),
			total_gross_profit,
			"Currency",
			"Green" if total_gross_profit >= 0 else "Red",
		),
	]
