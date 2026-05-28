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
		{"label": _("Date"), "fieldname": "harvest_date", "fieldtype": "Date", "width": 100},
		{"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 150},
		{"label": _("Field"), "fieldname": "field", "fieldtype": "Link", "options": "Field", "width": 150},
		{"label": _("Crop"), "fieldname": "crop", "fieldtype": "Link", "options": "Item", "width": 130},
		{"label": _("Area Harvested"), "fieldname": "area_harvested", "fieldtype": "Float", "width": 110},
		{"label": _("Quantity"), "fieldname": "quantity_harvested", "fieldtype": "Float", "width": 110},
		{"label": _("UOM"), "fieldname": "uom", "fieldtype": "Link", "options": "UOM", "width": 80},
		{"label": _("Yield/Unit"), "fieldname": "actual_yield_per_unit_area", "fieldtype": "Float", "width": 100},
		{"label": _("Wastage"), "fieldname": "wastage_loss", "fieldtype": "Float", "width": 90},
		{"label": _("Moisture %"), "fieldname": "moisture_percent", "fieldtype": "Float", "width": 90},
		{"label": _("Warehouse"), "fieldname": "target_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
		{"label": _("Batch"), "fieldname": "batch_no", "fieldtype": "Data", "width": 130},
		{"label": _("Document"), "fieldname": "name", "fieldtype": "Link", "options": "Harvest Record", "width": 130}
	]


def get_data(filters):
	conditions = []
	if filters.get("farm"):
		conditions.append("AND farm = %(farm)s")
	if filters.get("field"):
		conditions.append("AND field = %(field)s")
	if filters.get("crop"):
		conditions.append("AND crop = %(crop)s")
	if filters.get("from_date"):
		conditions.append("AND harvest_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("AND harvest_date <= %(to_date)s")

	conditions_str = " ".join(conditions)

	data = frappe.db.sql(f"""
		SELECT
			harvest_date,
			farm,
			field,
			crop,
			area_harvested,
			quantity_harvested,
			uom,
			actual_yield_per_unit_area,
			wastage_loss,
			moisture_percent,
			target_warehouse,
			batch_no,
			name
		FROM
			`tabHarvest Record`
		WHERE
			docstatus = 1
			{conditions_str}
		ORDER BY
			harvest_date DESC
	""", filters, as_dict=1)

	return data


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.crop or row.field,
		[{"name": _("Quantity Harvested"), "value_getter": lambda row: row.quantity_harvested}],
		colors=["#CA8A04"],
	)


def get_summary(data):
	return [
		make_summary_item(_("Harvest Records"), len(data), "Int", "Blue"),
		make_summary_item(_("Area Harvested"), sum_field(data, "area_harvested"), "Float", "Green"),
		make_summary_item(_("Quantity Harvested"), sum_field(data, "quantity_harvested"), "Float", "Green"),
		make_summary_item(_("Wastage"), sum_field(data, "wastage_loss"), "Float", "Orange"),
	]
