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
		{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
		{"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 130},
		{"label": _("Field"), "fieldname": "field", "fieldtype": "Link", "options": "Field", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Input Type"), "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 120},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
		{"label": _("Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 90},
		{"label": _("UOM"), "fieldname": "uom", "fieldtype": "Link", "options": "UOM", "width": 80},
		{"label": _("Rate"), "fieldname": "rate", "fieldtype": "Currency", "width": 100},
		{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 110},
		{"label": _("Batch"), "fieldname": "batch_no", "fieldtype": "Link", "options": "Batch", "width": 120},
		{"label": _("Stock Entry"), "fieldname": "stock_entry", "fieldtype": "Link", "options": "Stock Entry", "width": 130}
	]


def get_data(filters):
	conditions = []
	if filters.get("farm"):
		conditions.append("AND se.farm = %(farm)s")
	if filters.get("field"):
		conditions.append("AND se.field = %(field)s")
	if filters.get("project"):
		conditions.append("AND se.project = %(project)s")
	if filters.get("item_group"):
		conditions.append("AND i.item_group = %(item_group)s")
	if filters.get("from_date"):
		conditions.append("AND se.posting_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("AND se.posting_date <= %(to_date)s")

	conditions_str = " ".join(conditions)

	data = frappe.db.sql(f"""
		SELECT
			se.posting_date,
			se.farm,
			se.field,
			se.project,
			i.item_group,
			sed.item_code,
			sed.qty,
			sed.uom,
			sed.basic_rate as rate,
			sed.basic_amount as amount,
			sed.batch_no,
			se.name as stock_entry
		FROM
			`tabStock Entry` se
		INNER JOIN
			`tabStock Entry Detail` sed ON sed.parent = se.name
		LEFT JOIN
			`tabItem` i ON i.name = sed.item_code
		WHERE
			se.docstatus = 1
			AND se.stock_entry_type = 'Material Issue'
			{conditions_str}
		ORDER BY
			se.posting_date DESC
	""", filters, as_dict=1)

	return data


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.item_group or row.item_code,
		[{"name": _("Amount"), "value_getter": lambda row: row.amount}],
		colors=["#DC2626"],
	)


def get_summary(data):
	return [
		make_summary_item(_("Entries"), len(data), "Int", "Blue"),
		make_summary_item(_("Items"), count_unique(data, lambda row: row.item_code), "Int", "Blue"),
		make_summary_item(_("Total Qty"), sum_field(data, "qty"), "Float", "Green"),
		make_summary_item(_("Total Amount"), sum_field(data, "amount"), "Currency", "Orange"),
	]
