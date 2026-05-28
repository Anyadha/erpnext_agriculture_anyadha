from frappe.utils import flt


DEFAULT_CHART_COLORS = [
	"#2F6FED",
	"#16A34A",
	"#F59E0B",
	"#D9485F",
	"#0EA5E9",
	"#8B5CF6",
]


def build_chart(labels, datasets, chart_type="bar", colors=None):
	chart_datasets = []

	for dataset in datasets:
		chart_dataset = {"values": dataset.get("values", [])}

		if dataset.get("name"):
			chart_dataset["name"] = dataset["name"]

		chart_datasets.append(chart_dataset)

	return {
		"data": {"labels": labels, "datasets": chart_datasets},
		"type": chart_type,
		"colors": colors or DEFAULT_CHART_COLORS[: max(1, len(chart_datasets))],
	}


def build_grouped_chart(
	data,
	label_getter,
	dataset_specs,
	chart_type="bar",
	colors=None,
	limit=10,
	sort_index=0,
	sort_desc=True,
):
	grouped_data = {}

	for row in data:
		label = label_getter(row)
		if label in (None, ""):
			continue

		label = str(label)
		if label not in grouped_data:
			grouped_data[label] = [0.0 for _ in dataset_specs]

		for idx, spec in enumerate(dataset_specs):
			grouped_data[label][idx] += flt(spec["value_getter"](row))

	items = list(grouped_data.items())
	items.sort(key=lambda item: item[1][sort_index], reverse=sort_desc)
	items = items[:limit]

	labels = [label for label, _values in items]
	datasets = []

	for idx, spec in enumerate(dataset_specs):
		dataset = {"values": [values[idx] for _label, values in items]}
		if spec.get("name"):
			dataset["name"] = spec["name"]
		datasets.append(dataset)

	return build_chart(labels, datasets, chart_type=chart_type, colors=colors)


def sum_field(data, fieldname):
	return sum(flt(row.get(fieldname)) for row in data)


def average_field(data, fieldname):
	return sum_field(data, fieldname) / len(data) if data else 0


def count_unique(data, value_getter):
	unique_values = set()

	for row in data:
		value = value_getter(row)
		if value not in (None, ""):
			unique_values.add(str(value))

	return len(unique_values)


def make_summary_item(label, value, datatype="Float", indicator="Blue"):
	return {
		"value": value,
		"label": label,
		"datatype": datatype,
		"indicator": indicator,
	}
