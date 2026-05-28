// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Labor Utilization Report"] = {
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
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		}
	],

	get_chart_data: function(columns, result) {
		return {
			data: {
				labels: result.map(d => d.employee_name || d.employee || 'Unknown'),
				datasets: [{
					name: __("Total Hours"),
					values: result.map(d => d.total_hours || 0)
				}]
			},
			type: 'bar',
			height: 300,
			colors: ['#5e64ff']
		};
	}
};
