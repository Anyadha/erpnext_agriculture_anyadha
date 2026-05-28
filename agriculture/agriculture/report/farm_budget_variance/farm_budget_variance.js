// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Farm Budget Variance"] = {
	"filters": [
		{
			"fieldname": "farm",
			"label": __("Farm"),
			"fieldtype": "Link",
			"options": "Farm",
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.year_start(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		}
	],

	get_chart_data: function(columns, result) {
		return {
			data: {
				labels: result.map(d => d.project || 'Unknown'),
				datasets: [
					{
						name: __("Budgeted Cost"),
						values: result.map(d => d.budgeted_cost || 0)
					},
					{
						name: __("Actual Cost"),
						values: result.map(d => d.actual_cost || 0)
					}
				]
			},
			type: 'bar',
			height: 300,
			colors: ['#4bc0c0', '#ff9f40']
		};
	}
};
