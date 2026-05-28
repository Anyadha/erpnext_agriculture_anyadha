// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Input Consumption Report"] = {
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
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group"
		}
	],

	get_chart_data: function(columns, result) {
		let itemData = {};
		result.forEach(d => {
			if (!itemData[d.item]) {
				itemData[d.item] = 0;
			}
			itemData[d.item] += (d.total_cost || 0);
		});

		return {
			data: {
				labels: Object.keys(itemData),
				datasets: [{
					name: __("Total Cost"),
					values: Object.values(itemData)
				}]
			},
			type: 'bar',
			height: 300,
			colors: ['#ff9f40']
		};
	}
};
