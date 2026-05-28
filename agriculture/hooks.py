app_name = "agriculture"
app_title = "Anyadha Agriculture 2026"
app_publisher = "Anyadha Technologies LLP"
app_description = "Anyadha Agriculture 2026 is a modern, scalable, operationally practical app for corporate farming businesses that manages the full crop lifecycle across multiple farms, fields, seasons, and crops, from planning and land preparation to sowing, irrigation, fertilization, spraying, harvesting, post-harvest handling, storage, sales, and profitability analysis."
app_email = "prasanna@anyadha.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "agriculture",
# 		"logo": "/assets/agriculture/logo.png",
# 		"title": "Agriculture",
# 		"route": "/agriculture",
# 		"has_permission": "agriculture.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/agriculture/css/agriculture.css"
# app_include_js = "/assets/agriculture/js/agriculture.js"

# include js, css files in header of web template
# web_include_css = "/assets/agriculture/css/agriculture.css"
# web_include_js = "/assets/agriculture/js/agriculture.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "agriculture/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
app_include_icons = [
	"/assets/agriculture/icons.svg"
]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "agriculture.utils.jinja_methods",
# 	"filters": "agriculture.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "agriculture.install.before_install"
after_install = "agriculture.install.after_install"

# Fixtures
# --------
fixtures = [
	{"dt": "Role", "filters": [["name", "in", ["Agriculture Manager", "Agriculture User"]]]},
	{"dt": "Workspace", "filters": [["module", "=", "Agriculture"]]},
	{"dt": "DocType", "filters": [["name", "=", "Jute Grower Registration"]]},
	{
		"dt": "Custom Field",
		"filters": [["name", "in", [
			"Project-farm", "Project-field", "Project-crop_item", "Project-season",
			"Project-area_under_cultivation", "Project-expected_yield_per_unit",
			"Project-expected_total_yield", "Project-actual_yield",
			"Project-total_costing_amount", "Project-total_sales_amount",
			"Stock Entry-farm", "Stock Entry-field", "Stock Entry-operation_type",
			"Stock Entry-harvest_record", "Timesheet-farm", "Timesheet-field",
			"Timesheet-operation_log", "Asset-farm", "Asset-asset_category",
			"Employee-primary_farm", "Employee-agriculture_role"
		]]]
	},
]

# Uninstallation
# ------------

# before_uninstall = "agriculture.uninstall.before_uninstall"
# after_uninstall = "agriculture.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "agriculture.utils.before_app_install"
# after_app_install = "agriculture.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "agriculture.utils.before_app_uninstall"
# after_app_uninstall = "agriculture.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "agriculture.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"agriculture.tasks.all"
# 	],
# 	"daily": [
# 		"agriculture.tasks.daily"
# 	],
# 	"hourly": [
# 		"agriculture.tasks.hourly"
# 	],
# 	"weekly": [
# 		"agriculture.tasks.weekly"
# 	],
# 	"monthly": [
# 		"agriculture.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "agriculture.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "agriculture.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "agriculture.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "agriculture.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["agriculture.utils.before_request"]
# after_request = ["agriculture.utils.after_request"]

# Job Events
# ----------
# before_job = ["agriculture.utils.before_job"]
# after_job = ["agriculture.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"agriculture.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# Require all whitelisted methods to have type annotations
require_type_annotated_api_methods = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []
