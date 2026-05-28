from frappe import _


def get_data():
	return [
		{
			"label": _("Master Data"),
			"items": [
				{
					"type": "doctype",
					"name": "Farm",
					"description": _("Manage farms"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Field",
					"description": _("Manage fields within farms"),
					"onboard": 1,
				},
			]
		},
		{
			"label": _("Field Operations"),
			"items": [
				{
					"type": "doctype",
					"name": "Field Operation Log",
					"description": _("Record daily field operations"),
				},
				{
					"type": "doctype",
					"name": "Equipment Usage Log",
					"description": _("Track equipment usage and fuel consumption"),
				},
			]
		},
		{
			"label": _("Harvest & Production"),
			"items": [
				{
					"type": "doctype",
					"name": "Harvest Record",
					"description": _("Record harvest and create stock entries"),
				},
			]
		},
		{
			"label": _("Planning & Projects"),
			"items": [
				{
					"type": "doctype",
					"name": "Project",
					"description": _("Manage crop cycle projects"),
				},
				{
					"type": "doctype",
					"name": "Task",
					"description": _("Track field operation tasks"),
				},
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"name": "Spray Register",
					"doctype": "Field Operation Log",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Fertilizer Register",
					"doctype": "Field Operation Log",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Field Utilization Report",
					"doctype": "Field",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Harvest Report",
					"doctype": "Harvest Record",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Crop Profitability Report",
					"doctype": "Project",
					"is_query_report": True,
				},
			]
		},
	]
