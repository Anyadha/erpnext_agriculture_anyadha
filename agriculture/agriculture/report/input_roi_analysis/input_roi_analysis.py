# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
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
		{
			"fieldname": "item",
			"label": _("Input Item"),
			"fieldtype": "Link",
			"options": "Item",
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
			"fieldname": "total_qty_consumed",
			"label": _("Total Qty Consumed"),
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "uom",
			"label": _("UOM"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "total_cost",
			"label": _("Total Input Cost"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "revenue_generated",
			"label": _("Revenue Generated"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "roi",
			"label": _("ROI"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "roi_percent",
			"label": _("ROI %"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "roi_status",
			"label": _("ROI Status"),
			"fieldtype": "Data",
			"width": 120
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)

	# Get input consumption data from Stock Entry
	data = frappe.db.sql(f"""
		SELECT
			sed.item_code as item,
			se.farm,
			SUM(sed.qty) as total_qty_consumed,
			sed.uom,
			SUM(sed.amount) as total_cost,
			0 as revenue_generated,
			0 as roi,
			0 as roi_percent,
			'Pending Revenue' as roi_status
		FROM `tabStock Entry Detail` sed
		JOIN `tabStock Entry` se ON se.name = sed.parent
		WHERE se.docstatus = 1
			AND se.farm IS NOT NULL
			AND se.purpose IN ('Material Issue', 'Material Consumption for Manufacture')
			{conditions}
		GROUP BY sed.item_code, se.farm
		ORDER BY total_cost DESC
	""", filters, as_dict=1)

	# Calculate ROI where revenue is available (from harvest/sales)
	for row in data:
		revenue = get_revenue_for_farm(row.farm, filters)
		if revenue:
			row.revenue_generated = revenue
			row.roi = revenue - row.total_cost
			if row.total_cost > 0:
				row.roi_percent = (row.roi / row.total_cost) * 100

			if row.roi_percent >= 100:
				row.roi_status = "Excellent"
			elif row.roi_percent >= 50:
				row.roi_status = "Good"
			elif row.roi_percent >= 0:
				row.roi_status = "Break Even"
			else:
				row.roi_status = "Loss"

	return data


def get_revenue_for_farm(farm, filters):
	"""Get total revenue from sales for the farm"""
	conditions = ""

	if filters.get("from_date"):
		conditions += " AND si.posting_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND si.posting_date <= %(to_date)s"

	result = frappe.db.sql(f"""
		SELECT SUM(si.grand_total) as revenue
		FROM `tabSales Invoice` si
		WHERE si.docstatus = 1
			{conditions}
	""", filters, as_dict=1)

	return result[0].revenue if result and result[0].revenue else 0


def get_conditions(filters):
	conditions = ""

	if filters.get("farm"):
		conditions += " AND se.farm = %(farm)s"

	if filters.get("item"):
		conditions += " AND sed.item_code = %(item)s"

	if filters.get("from_date"):
		conditions += " AND se.posting_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND se.posting_date <= %(to_date)s"

	return conditions


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.item,
		[
			{"name": _("Input Cost"), "value_getter": lambda row: row.total_cost},
			{"name": _("ROI"), "value_getter": lambda row: row.roi},
		],
		colors=["#EA580C", "#16A34A"],
		sort_index=0,
	)


def get_summary(data):
	profitable_items = len([row for row in data if flt(row.roi) > 0])
	total_roi = sum_field(data, "roi")

	return [
		make_summary_item(_("Items"), count_unique(data, lambda row: row.item), "Int", "Blue"),
		make_summary_item(_("Total Input Cost"), sum_field(data, "total_cost"), "Currency", "Orange"),
		make_summary_item(
			_("Total ROI"),
			total_roi,
			"Currency",
			"Green" if total_roi >= 0 else "Red",
		),
		make_summary_item(_("Profitable Items"), profitable_items, "Int", "Green"),
	]
