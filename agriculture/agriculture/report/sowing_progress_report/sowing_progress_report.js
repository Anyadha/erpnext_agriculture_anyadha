// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Sowing Progress Report"] = {
	"filters": [
		{
			"fieldname": "season",
			"label": __("Season"),
			"fieldtype": "Select",
			"options": "\nRabi\nKharif\nZaid\nSummer\nWinter\nSpring\nFall",
			"reqd": 1
		},
		{
			"fieldname": "farm",
			"label": __("Farm"),
			"fieldtype": "Link",
			"options": "Farm"
		},
		{
			"fieldname": "crop",
			"label": __("Crop"),
			"fieldtype": "Link",
			"options": "Item"
		}
	],

	get_chart_data: function(columns, result) {
		return {
			data: {
				labels: result.map(d => d.field || 'Unknown'),
				datasets: [
					{
						name: __("Planned Area"),
						values: result.map(d => d.planned_area || 0)
					},
					{
						name: __("Sown Area"),
						values: result.map(d => d.sown_area || 0)
					}
				]
			},
			type: 'bar',
			height: 300,
			colors: ['#36a2eb', '#98d85b']
		};
	}
};
