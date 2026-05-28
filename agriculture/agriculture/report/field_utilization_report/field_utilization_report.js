// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Field Utilization Report"] = {
	"filters": [
		{
			"fieldname": "farm",
			"label": __("Farm"),
			"fieldtype": "Link",
			"options": "Farm"
		},
		{
			"fieldname": "season",
			"label": __("Season"),
			"fieldtype": "Select",
			"options": "\nRabi\nKharif\nZaid\nSummer\nWinter\nSpring\nFall"
		}
	],

	get_chart_data: function(columns, result) {
		let statusData = {};
		result.forEach(d => {
			if (!statusData[d.current_status]) {
				statusData[d.current_status] = 0;
			}
			statusData[d.current_status]++;
		});

		return {
			data: {
				labels: Object.keys(statusData),
				datasets: [{
					name: __("Number of Fields"),
					values: Object.values(statusData)
				}]
			},
			type: 'pie',
			height: 300,
			colors: ['#63d0ff', '#ffa00a', '#98d85b', '#ff6c5c', '#5e64ff']
		};
	}
};
