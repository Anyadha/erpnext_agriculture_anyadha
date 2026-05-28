// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Input ROI Analysis"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -6),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
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
				labels: result.map(d => d.project || 'Unknown'),
				datasets: [
					{
						name: __("Input Cost"),
						values: result.map(d => d.input_cost || 0)
					},
					{
						name: __("Revenue"),
						values: result.map(d => d.revenue || 0)
					}
				]
			},
			type: 'bar',
			height: 300,
			colors: ['#ff6384', '#36a2eb']
		};
	}
};
