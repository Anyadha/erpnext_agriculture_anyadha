// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Spray Register"] = {
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
		let chemicalData = {};
		result.forEach(d => {
			if (!chemicalData[d.item]) {
				chemicalData[d.item] = 0;
			}
			chemicalData[d.item] += (d.quantity || 0);
		});

		return {
			data: {
				labels: Object.keys(chemicalData),
				datasets: [{
					name: __("Quantity Used"),
					values: Object.values(chemicalData)
				}]
			},
			type: 'bar',
			height: 300,
			colors: ['#ff6c5c']
		};
	}
};
