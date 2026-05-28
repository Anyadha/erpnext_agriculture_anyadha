// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Harvest Report"] = {
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
			"fieldname": "crop",
			"label": __("Crop"),
			"fieldtype": "Link",
			"options": "Item"
		}
	],

	get_chart_data: function(columns, result) {
		let cropData = {};
		result.forEach(d => {
			if (!cropData[d.crop]) {
				cropData[d.crop] = 0;
			}
			cropData[d.crop] += (d.quantity_harvested || 0);
		});

		return {
			data: {
				labels: Object.keys(cropData),
				datasets: [{
					name: __("Total Harvested"),
					values: Object.values(cropData)
				}]
			},
			type: 'bar',
			height: 300,
			colors: ['#98d85b']
		};
	}
};
