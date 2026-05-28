// Copyright (c) 2026, Anyadha Technologies LLP
// For license information, please see license.txt

frappe.query_reports["Yield Variance Report"] = {
	"filters": [
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
			"options": "Field",
			"get_query": function() {
				var farm = frappe.query_report.get_filter_value('farm');
				if (farm) {
					return {
						"filters": {
							"farm": farm
						}
					};
				}
			}
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

	"onload": function(report) {
		// Add custom buttons if needed
	},

	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "variance_percent" && data) {
			if (data.variance_percent > 0) {
				value = "<span style='color:green'>" + value + "</span>";
			} else if (data.variance_percent < 0) {
				value = "<span style='color:red'>" + value + "</span>";
			}
		}

		if (column.fieldname == "status" && data) {
			if (data.status == "Above Target") {
				value = "<span style='color:green; font-weight:bold'>" + value + "</span>";
			} else if (data.status == "Below Target") {
				value = "<span style='color:red; font-weight:bold'>" + value + "</span>";
			}
		}

		return value;
	},

	get_chart_data: function(columns, result) {
		return {
			data: {
				labels: result.map(d => d.project || 'Unknown'),
				datasets: [
					{
						name: __("Expected Yield"),
						values: result.map(d => d.expected_yield || 0)
					},
					{
						name: __("Actual Yield"),
						values: result.map(d => d.actual_yield || 0)
					}
				]
			},
			type: 'bar',
			height: 300,
			colors: ['#7cd6fd', '#5e64ff']
		};
	}
};
