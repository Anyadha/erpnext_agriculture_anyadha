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
		{"label": _("Employee"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
		{"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 130},
		{"label": _("Field"), "fieldname": "field", "fieldtype": "Link", "options": "Field", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Activity"), "fieldname": "activity_type", "fieldtype": "Data", "width": 130},
		{"label": _("Hours"), "fieldname": "total_hours", "fieldtype": "Float", "width": 80},
		{"label": _("Billing Rate"), "fieldname": "billing_rate", "fieldtype": "Currency", "width": 110},
		{"label": _("Billing Amount"), "fieldname": "billing_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Timesheet"), "fieldname": "name", "fieldtype": "Link", "options": "Timesheet", "width": 130}
	]


def get_data(filters):
	conditions = []
	if filters.get("farm"):
		conditions.append("AND t.farm = %(farm)s")
	if filters.get("field"):
		conditions.append("AND t.field = %(field)s")
	if filters.get("project"):
		conditions.append("AND td.project = %(project)s")
	if filters.get("employee"):
		conditions.append("AND t.employee = %(employee)s")
	if filters.get("from_date"):
		conditions.append("AND t.start_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("AND t.end_date <= %(to_date)s")

	conditions_str = " ".join(conditions)

	data = frappe.db.sql(f"""
		SELECT
			t.start_date as date,
			t.employee,
			t.employee_name,
			t.farm,
			t.field,
			td.project,
			td.activity_type,
			SUM(td.hours) as total_hours,
			td.billing_rate,
			SUM(td.billing_amount) as billing_amount,
			t.name
		FROM
			`tabTimesheet` t
		INNER JOIN
			`tabTimesheet Detail` td ON td.parent = t.name
		WHERE
			t.docstatus = 1
			{conditions_str}
		GROUP BY
			t.name, td.project, td.activity_type
		ORDER BY
			t.start_date DESC
	""", filters, as_dict=1)

	return data


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.employee_name or row.employee,
		[{"name": _("Hours"), "value_getter": lambda row: row.total_hours}],
		colors=["#2E7D32"],
	)


def get_summary(data):
	return [
		make_summary_item(_("Entries"), len(data), "Int", "Blue"),
		make_summary_item(_("Employees"), count_unique(data, lambda row: row.employee), "Int", "Blue"),
		make_summary_item(_("Total Hours"), sum_field(data, "total_hours"), "Float", "Green"),
		make_summary_item(_("Billing Amount"), sum_field(data, "billing_amount"), "Currency", "Orange"),
	]
