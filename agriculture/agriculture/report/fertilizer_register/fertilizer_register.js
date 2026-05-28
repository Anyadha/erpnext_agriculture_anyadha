// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Fertilizer Register"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
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
			"fieldname": "field",
			"label": __("Field"),
			"fieldtype": "Link",
			"options": "Field"
		}
	],

	get_chart_data: function(columns, result) {
		let fertilizerData = {};
		result.forEach(d => {
			if (!fertilizerData[d.item]) {
				fertilizerData[d.item] = 0;
			}
			fertilizerData[d.item] += (d.quantity || 0);
		});

		return {
			data: {
				labels: Object.keys(fertilizerData),
				datasets: [{
					name: __("Quantity Used"),
					values: Object.values(fertilizerData)
				}]
			},
			type: 'bar',
			height: 300,
			colors: ['#98d85b']
		};
	}
};
