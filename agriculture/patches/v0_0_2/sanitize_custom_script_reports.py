# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

from __future__ import annotations

import frappe


REPORT_NAMES = (
	"Yield Variance Report",
	"Input ROI Analysis",
	"Equipment Efficiency Report",
	"Farm Budget Variance",
)

def execute() -> None:
	for report_name in REPORT_NAMES:
		if not frappe.db.exists("Report", report_name):
			continue

		frappe.db.set_value(
			"Report",
			report_name,
			{"is_standard": "Yes", "report_script": None},
			update_modified=False,
		)
