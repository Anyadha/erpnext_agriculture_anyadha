# Copyright (c) 2026, Anyadha Technologies LLP
# For license information, please see license.txt

from __future__ import annotations

import frappe


DOCTYPE_ICONS = {
	"Agriculture Settings": "fa fa-sliders",
	"Equipment Usage Log": "fa fa-cogs",
	"Farm": "fa fa-map-marker",
	"Farm Soil Profile": "fa fa-flask",
	"Field": "fa fa-th-large",
	"Field Crop History": "fa fa-history",
	"Field Operation Log": "fa fa-clipboard",
	"Harvest Equipment": "fa fa-cogs",
	"Harvest Grade Distribution": "fa fa-pie-chart",
	"Harvest Record": "fa fa-archive",
	"Harvest Team Member": "fa fa-users",
}

SIDEBAR_ICONS = {
	"Home": "house",
	"Master Data": "database",
	"Farm": "landmark",
	"Field": "grid-2x2",
	"Operations & Logs": "clipboard-pen",
	"Field Operation Log": "clipboard-list",
	"Equipment Usage Log": "tractor",
	"Harvesting": "wheat",
	"Harvest Record": "package-check",
	"Planning & Inventory": "folder-kanban",
	"Project": "calendar-range",
	"Task": "list-todo",
	"Item": "package",
	"Stock Entry": "arrow-right-left",
	"Compliance Reports": "shield-check",
	"Spray Register": "spray-can",
	"Fertilizer Register": "flask-conical",
	"Operational Reports": "chart-column",
	"Field Utilization Report": "chart-pie",
	"Harvest Report": "wheat",
	"Labor Utilization Report": "users",
	"Machinery Usage Report": "truck",
	"Irrigation History Report": "droplets",
	"Sowing Progress Report": "sprout",
	"Input Consumption Report": "package-open",
	"Financial & Analytics": "chart-line",
	"Crop Profitability Report": "dollar-sign",
	"Yield Variance Report": "chart-column-big",
	"Input ROI Analysis": "percent",
	"Equipment Efficiency Report": "gauge",
	"Farm Budget Variance": "trending-up",
	"Settings": "settings",
	"Agriculture Settings": "sliders-horizontal",
}

WORKSPACE_LINKS = [
	{"hidden": 0, "icon": "database", "is_query_report": 0, "label": "Master Data", "link_count": 0, "onboard": 0, "type": "Card Break"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Farm", "link_count": 0, "link_to": "Farm", "link_type": "DocType", "onboard": 1, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Field", "link_count": 0, "link_to": "Field", "link_type": "DocType", "onboard": 1, "type": "Link"},
	{"hidden": 0, "icon": "clipboard-pen", "is_query_report": 0, "label": "Operations & Logs", "link_count": 0, "onboard": 0, "type": "Card Break"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Field Operation Log", "link_count": 0, "link_to": "Field Operation Log", "link_type": "DocType", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Equipment Usage Log", "link_count": 0, "link_to": "Equipment Usage Log", "link_type": "DocType", "onboard": 0, "type": "Link"},
	{"hidden": 0, "icon": "wheat", "is_query_report": 0, "label": "Harvesting", "link_count": 0, "onboard": 0, "type": "Card Break"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Harvest Record", "link_count": 0, "link_to": "Harvest Record", "link_type": "DocType", "onboard": 0, "type": "Link"},
	{"hidden": 0, "icon": "folder-kanban", "is_query_report": 0, "label": "Planning & Inventory", "link_count": 0, "onboard": 0, "type": "Card Break"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Project", "link_count": 0, "link_to": "Project", "link_type": "DocType", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Task", "link_count": 0, "link_to": "Task", "link_type": "DocType", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Item", "link_count": 0, "link_to": "Item", "link_type": "DocType", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Stock Entry", "link_count": 0, "link_to": "Stock Entry", "link_type": "DocType", "onboard": 0, "type": "Link"},
	{"hidden": 0, "icon": "shield-check", "is_query_report": 0, "label": "Compliance Reports", "link_count": 0, "onboard": 0, "type": "Card Break"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Spray Register", "link_count": 0, "link_to": "Spray Register", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Fertilizer Register", "link_count": 0, "link_to": "Fertilizer Register", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"hidden": 0, "icon": "chart-column", "is_query_report": 0, "label": "Operational Reports", "link_count": 0, "onboard": 0, "type": "Card Break"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Field Utilization Report", "link_count": 0, "link_to": "Field Utilization Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Harvest Report", "link_count": 0, "link_to": "Harvest Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Labor Utilization Report", "link_count": 0, "link_to": "Labor Utilization Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Machinery Usage Report", "link_count": 0, "link_to": "Machinery Usage Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Irrigation History Report", "link_count": 0, "link_to": "Irrigation History Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Sowing Progress Report", "link_count": 0, "link_to": "Sowing Progress Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Input Consumption Report", "link_count": 0, "link_to": "Input Consumption Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"hidden": 0, "icon": "chart-line", "is_query_report": 0, "label": "Financial & Analytics", "link_count": 0, "onboard": 0, "type": "Card Break"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Crop Profitability Report", "link_count": 0, "link_to": "Crop Profitability Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Yield Variance Report", "link_count": 0, "link_to": "Yield Variance Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Input ROI Analysis", "link_count": 0, "link_to": "Input ROI Analysis", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Equipment Efficiency Report", "link_count": 0, "link_to": "Equipment Efficiency Report", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Farm Budget Variance", "link_count": 0, "link_to": "Farm Budget Variance", "link_type": "Report", "onboard": 0, "type": "Link"},
	{"hidden": 0, "icon": "settings", "is_query_report": 0, "label": "Settings", "link_count": 0, "onboard": 0, "type": "Card Break"},
	{"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Agriculture Settings", "link_count": 0, "link_to": "Agriculture Settings", "link_type": "DocType", "onboard": 0, "type": "Link"},
]


def execute() -> None:
	_sync_doctype_icons()
	_sync_workspace_icon()
	_sync_workspace_links()
	_sync_sidebar_icons()


def _sync_doctype_icons() -> None:
	for doctype, icon in DOCTYPE_ICONS.items():
		if frappe.db.exists("DocType", doctype):
			frappe.db.set_value("DocType", doctype, "icon", icon, update_modified=False)


def _sync_workspace_icon() -> None:
	if frappe.db.exists("Workspace", "Agriculture"):
		frappe.db.set_value("Workspace", "Agriculture", "icon", "agriculture", update_modified=False)


def _sync_workspace_links() -> None:
	if not frappe.db.exists("Workspace", "Agriculture"):
		return

	workspace = frappe.get_doc("Workspace", "Agriculture")
	previous_in_patch = frappe.flags.in_patch
	frappe.flags.in_patch = True
	try:
		workspace.set("links", [])
		for idx, link in enumerate(WORKSPACE_LINKS, start=1):
			workspace.append("links", {"idx": idx, **link})
		workspace.save(ignore_permissions=True)
	finally:
		frappe.flags.in_patch = previous_in_patch


def _sync_sidebar_icons() -> None:
	if not frappe.db.exists("Workspace Sidebar", "Agriculture"):
		return

	for label, icon in SIDEBAR_ICONS.items():
		frappe.db.sql(
			"""
			update `tabWorkspace Sidebar Item`
			set icon = %(icon)s
			where parent = 'Agriculture' and label = %(label)s
			""",
			{"icon": icon, "label": label},
		)
