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
		{"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 150},
		{"label": _("Field"), "fieldname": "field", "fieldtype": "Link", "options": "Field", "width": 150},
		{"label": _("Crop"), "fieldname": "crop", "fieldtype": "Data", "width": 130},
		{"label": _("Season"), "fieldname": "season", "fieldtype": "Data", "width": 100},
		{"label": _("Planned Area"), "fieldname": "planned_area", "fieldtype": "Float", "width": 110},
		{"label": _("Sown Area"), "fieldname": "sown_area", "fieldtype": "Float", "width": 110},
		{"label": _("Progress %"), "fieldname": "progress_pct", "fieldtype": "Percent", "width": 100},
		{"label": _("Planned Date"), "fieldname": "expected_start_date", "fieldtype": "Date", "width": 110},
		{"label": _("Actual Date"), "fieldname": "actual_sowing_date", "fieldtype": "Date", "width": 110},
		{"label": _("Status"), "fieldname": "sowing_status", "fieldtype": "Data", "width": 100},
		{"label": _("Project"), "fieldname": "name", "fieldtype": "Link", "options": "Project", "width": 130}
	]


def get_data(filters):
	conditions = []
	if filters.get("farm"):
		conditions.append("AND farm = %(farm)s")
	if filters.get("season"):
		conditions.append("AND season = %(season)s")
	if filters.get("crop"):
		conditions.append("AND crop_item = %(crop)s")

	conditions_str = " ".join(conditions)

	data = frappe.db.sql(f"""
		SELECT
			p.farm,
			p.field,
			p.crop_item as crop,
			p.season,
			p.area_under_cultivation as planned_area,
			CASE
				WHEN f.current_status IN ('Sown', 'Growing', 'Harvested') THEN p.area_under_cultivation
				ELSE 0
			END as sown_area,
			CASE
				WHEN f.current_status IN ('Sown', 'Growing', 'Harvested') THEN 100
				ELSE 0
			END as progress_pct,
			p.expected_start_date,
			NULL as actual_sowing_date,
			CASE
				WHEN f.current_status IN ('Sown', 'Growing') THEN 'Sown'
				WHEN f.current_status = 'Harvested' THEN 'Completed'
				WHEN f.current_status = 'Under Preparation' THEN 'In Progress'
				ELSE 'Pending'
			END as sowing_status,
			p.name
		FROM
			`tabProject` p
		LEFT JOIN
			`tabField` f ON f.name = p.field
		WHERE
			p.farm IS NOT NULL
			AND p.status != 'Cancelled'
			{conditions_str}
		ORDER BY
			p.expected_start_date DESC
	""", filters, as_dict=1)

	return data


def get_summary(data):
	total_planned = sum_field(data, "planned_area")
	total_sown = sum_field(data, "sown_area")
	overall_progress = (total_sown / total_planned * 100) if total_planned > 0 else 0

	return [
		make_summary_item(_("Projects"), len(data), "Int", "Blue"),
		make_summary_item(_("Total Planned Area"), total_planned, "Float", "Blue"),
		make_summary_item(_("Total Sown Area"), total_sown, "Float", "Green"),
		make_summary_item(
			_("Overall Progress %"),
			overall_progress,
			"Percent",
			"Green" if overall_progress >= 75 else "Orange",
		),
	]


def get_chart_data(data):
	return build_grouped_chart(
		data,
		lambda row: row.field,
		[
			{"name": _("Planned Area"), "value_getter": lambda row: row.planned_area},
			{"name": _("Sown Area"), "value_getter": lambda row: row.sown_area},
		],
		colors=["#94A3B8", "#16A34A"],
	)
