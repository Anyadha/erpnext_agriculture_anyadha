# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

from __future__ import annotations

import frappe


OLD_NAME = "Input Roi Analysis"
NEW_NAME = "Input ROI Analysis"


def execute() -> None:
	if frappe.db.exists("Report", OLD_NAME) and not frappe.db.exists("Report", NEW_NAME):
		frappe.rename_doc("Report", OLD_NAME, NEW_NAME, force=True, ignore_if_exists=True)

	if frappe.db.exists("Report", NEW_NAME):
		frappe.db.set_value(
			"Report",
			NEW_NAME,
			{"report_name": NEW_NAME, "is_standard": "Yes", "report_script": None},
			update_modified=False,
		)

	_update_workspace_links()


def _update_workspace_links() -> None:
	if frappe.db.exists("DocType", "Workspace Link"):
		frappe.db.sql(
			"""
			update `tabWorkspace Link`
			set link_to = %(new_name)s
			where link_type = 'Report' and link_to = %(old_name)s
			""",
			{"old_name": OLD_NAME, "new_name": NEW_NAME},
		)

	if frappe.db.exists("DocType", "Workspace Sidebar Item"):
		frappe.db.sql(
			"""
			update `tabWorkspace Sidebar Item`
			set link_to = %(new_name)s
			where link_type = 'Report' and link_to = %(old_name)s
			""",
			{"old_name": OLD_NAME, "new_name": NEW_NAME},
		)
