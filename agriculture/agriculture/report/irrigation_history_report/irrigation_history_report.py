# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe import _
from agriculture.agriculture.report_utils import build_grouped_chart, count_unique, make_summary_item, sum_field



def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary


def get_columns():
	return [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 100},
		{"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 150},
		{"label": _("Field"), "fieldname": "field", "fieldtype": "Link", "options": "Field", "width": 150},
		{"label": _("Crop"), "fieldname": "crop", "fieldtype": "Data", "width": 120},
		{"label": _("Crop Stage"), "fieldname": "stage_of_crop", "fieldtype": "Data", "width": 100},
		{"label": _("Irrigation Method"), "fieldname": "irrigation_method", "fieldtype": "Data", "width": 130},
		{"label": _("Duration (hrs)"), "fieldname": "duration", "fieldtype": "Data", "width": 100},
		{"label": _("Water Source"), "fieldname": "water_source", "fieldtype": "Data", "width": 130},
		{"label": _("Operator"), "fieldname": "operator_supervisor", "fieldtype": "Link", "options": "Employee", "width": 130},
		{"label": _("Weather"), "fieldname": "weather_conditions", "fieldtype": "Data", "width": 120},
		{"label": _("Observations"), "fieldname": "observations", "fieldtype": "Data", "width": 200},
		{"label": _("Document"), "fieldname": "name", "fieldtype": "Link", "options": "Field Operation Log", "width": 130}
	]


def get_data(filters):
	conditions = []
	if filters.get("farm"):
		conditions.append("AND fol.farm = %(farm)s")
	if filters.get("field"):
		conditions.append("AND fol.field = %(field)s")
	if filters.get("from_date"):
		conditions.append("AND fol.date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("AND fol.date <= %(to_date)s")

	conditions_str = " ".join(conditions)

	data = frappe.db.sql(f"""
		SELECT
			fol.date,
			fol.farm,
			fol.field,
			p.crop_item as crop,
			fol.stage_of_crop,
			f.irrigation_method,
			fol.activity_description as duration,
			f.irrigation_source as water_source,
			fol.operator_supervisor,
			fol.weather_conditions,
			fol.observations,
			fol.name
		FROM
			`tabField Operation Log` fol
		LEFT JOIN
			`tabProject` p ON p.name = fol.crop_project
		LEFT JOIN
			`tabField` f ON f.name = fol.field
		WHERE
			fol.docstatus = 1
			AND fol.operation_type = 'Irrigation'
			{conditions_str}
		ORDER BY
			fol.date DESC
	""", filters, as_dict=1)

	return data


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.field,
		[{"name": _("Duration (hrs)"), "value_getter": lambda row: row.duration}],
		colors=["#0284C7"],
	)


def get_summary(data):
	return [
		make_summary_item(_("Irrigation Logs"), len(data), "Int", "Blue"),
		make_summary_item(_("Farms"), count_unique(data, lambda row: row.farm), "Int", "Blue"),
		make_summary_item(_("Fields"), count_unique(data, lambda row: row.field), "Int", "Blue"),
		make_summary_item(_("Total Duration"), sum_field(data, "duration"), "Float", "Green"),
	]
