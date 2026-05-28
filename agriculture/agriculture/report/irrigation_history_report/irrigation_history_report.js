// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Irrigation History Report"] = {
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
			"fieldname": "field",
			"label": __("Field"),
			"fieldtype": "Link",
			"options": "Field"
		}
	],

	get_chart_data: function(columns, result) {
		let fieldData = {};
		result.forEach(d => {
			if (!fieldData[d.field]) {
				fieldData[d.field] = 0;
			}
			fieldData[d.field]++;
		});

		return {
			data: {
				labels: Object.keys(fieldData),
				datasets: [{
					name: __("Irrigation Count"),
					values: Object.values(fieldData)
				}]
			},
			type: 'bar',
			height: 300,
			colors: ['#63d0ff']
		};
	}
};
