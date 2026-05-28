// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Equipment Efficiency Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
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
			"fieldname": "asset",
			"label": __("Equipment/Asset"),
			"fieldtype": "Link",
			"options": "Asset"
		}
	],

	get_chart_data: function(columns, result) {
		return {
			data: {
				labels: result.map(d => d.asset_name || d.asset || 'Unknown'),
				datasets: [
					{
						name: __("Operating Hours"),
						values: result.map(d => d.total_hours || 0)
					},
					{
						name: __("Fuel Consumed (L)"),
						values: result.map(d => d.total_fuel || 0)
					}
				]
			},
			type: 'bar',
			height: 300,
			colors: ['#ffa00a', '#ff6c5c']
		};
	}
};
