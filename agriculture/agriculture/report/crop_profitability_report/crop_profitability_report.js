// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Crop Profitability Report"] = {
	"filters": [
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
		},
		{
			"fieldname": "season",
			"label": __("Season"),
			"fieldtype": "Select",
			"options": "\nRabi\nKharif\nZaid\nSummer\nWinter\nSpring\nFall"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -12)
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		}
	],

	get_chart_data: function(columns, result) {
		return {
			data: {
				labels: result.map(d => d.crop || 'Unknown'),
				datasets: [
					{
						name: __("Total Cost"),
						values: result.map(d => d.total_costing_amount || 0)
					},
					{
						name: __("Revenue"),
						values: result.map(d => d.total_sales_amount || 0)
					},
					{
						name: __("Gross Profit"),
						values: result.map(d => d.gross_profit || 0)
					}
				]
			},
			type: 'bar',
			height: 300,
			colors: ['#ff6384', '#36a2eb', '#4bc0c0']
		};
	}
};
