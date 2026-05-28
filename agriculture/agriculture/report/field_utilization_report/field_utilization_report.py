# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe import _

from frappe.utils import date_diff, getdate
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
		{"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 150},
		{"label": _("Field ID"), "fieldname": "field_id", "fieldtype": "Link", "options": "Field", "width": 130},
		{"label": _("Field Name"), "fieldname": "field_name", "fieldtype": "Data", "width": 150},
		{"label": _("Area"), "fieldname": "area", "fieldtype": "Float", "width": 100},
		{"label": _("Status"), "fieldname": "current_status", "fieldtype": "Data", "width": 120},
		{"label": _("Current Crop"), "fieldname": "current_crop", "fieldtype": "Data", "width": 130},
		{"label": _("Last Harvest Date"), "fieldname": "last_harvest_date", "fieldtype": "Date", "width": 120},
		{"label": _("Days Vacant"), "fieldname": "days_vacant", "fieldtype": "Int", "width": 100},
		{"label": _("Soil Type"), "fieldname": "soil_type", "fieldtype": "Data", "width": 120}
	]


def get_data(filters):
	conditions = []
	if filters.get("farm"):
		conditions.append("AND farm = %(farm)s")
	if filters.get("current_status"):
		conditions.append("AND current_status = %(current_status)s")

	conditions_str = " ".join(conditions)

	data = frappe.db.sql(f"""
		SELECT
			farm,
			field_id,
			field_name,
			area,
			current_status,
			current_crop,
			last_harvest_date,
			days_vacant,
			soil_type
		FROM
			`tabField`
		WHERE
			1=1
			{conditions_str}
		ORDER BY
			farm, field_id
	""", filters, as_dict=1)

	return data


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.current_status,
		[{"name": _("Area"), "value_getter": lambda row: row.area}],
		colors=["#2563EB"],
	)


def get_summary(data):
	return [
		make_summary_item(_("Fields"), len(data), "Int", "Blue"),
		make_summary_item(_("Farms"), count_unique(data, lambda row: row.farm), "Int", "Blue"),
		make_summary_item(_("Total Area"), sum_field(data, "area"), "Float", "Green"),
		make_summary_item(_("Avg Days Vacant"), average_field(data, "days_vacant"), "Float", "Orange"),
	]
