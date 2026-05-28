import frappe


def execute():
	"""
	v0_0_5: Add Jute Grower Registration link to the Agriculture workspace Master Data section.
	Idempotent — safe to run multiple times.
	"""
	workspace_name = "Agriculture"

	if not frappe.db.exists("Workspace", workspace_name):
		return

	ws = frappe.get_doc("Workspace", workspace_name)

	# Already added — skip
	already_exists = any(
		getattr(row, "link_to", None) == "Jute Grower Registration"
		for row in ws.links
	)
	if already_exists:
		return

	# Find the index of "Operations & Logs" Card Break so we insert just before it
	insert_before_idx = None
	for i, row in enumerate(ws.links):
		if row.get("type") == "Card Break" and row.get("label") == "Operations & Logs":
			insert_before_idx = i
			break

	new_link = frappe.get_doc({
		"doctype": "Workspace Link",
		"dependencies": "",
		"hidden": 0,
		"is_query_report": 0,
		"label": "Jute Grower Registration",
		"link_count": 0,
		"link_to": "Jute Grower Registration",
		"link_type": "DocType",
		"onboard": 1,
		"type": "Link",
	})

	if insert_before_idx is not None:
		ws.links.insert(insert_before_idx, new_link)
	else:
		ws.append("links", new_link)

	ws.flags.ignore_permissions = True
	ws.save()
	frappe.db.commit()
