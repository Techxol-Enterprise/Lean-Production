app_name = "lean_production"
app_title = "Lean Production"
app_publisher = "Techxol"
app_description = "Streamlined Stage-Based Manufacturing"
app_email = "info@techxol.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "lean_production",
# 		"logo": "/assets/lean_production/logo.png",
# 		"title": "Lean Production",
# 		"route": "/lean_production",
# 		"has_permission": "lean_production.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lean_production/css/lean_production.css"
# app_include_js = "/assets/lean_production/js/lean_production.js"

# include js, css files in header of web template
# web_include_css = "/assets/lean_production/css/lean_production.css"
# web_include_js = "/assets/lean_production/js/lean_production.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lean_production/public/scss/website"

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
# app_include_icons = "lean_production/public/icons.svg"

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
# 	"methods": "lean_production.utils.jinja_methods",
# 	"filters": "lean_production.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "lean_production.install.before_install"
# after_install = "lean_production.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lean_production.uninstall.before_uninstall"
# after_uninstall = "lean_production.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lean_production.utils.before_app_install"
# after_app_install = "lean_production.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lean_production.utils.before_app_uninstall"
# after_app_uninstall = "lean_production.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "lean_production.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lean_production.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["lean_production.search.awesomebar_results"]

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
# 		"lean_production.tasks.all"
# 	],
# 	"daily": [
# 		"lean_production.tasks.daily"
# 	],
# 	"hourly": [
# 		"lean_production.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lean_production.tasks.weekly"
# 	],
# 	"monthly": [
# 		"lean_production.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "lean_production.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "lean_production.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lean_production.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lean_production.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lean_production.utils.before_request"]
# after_request = ["lean_production.utils.after_request"]

# Job Events
# ----------
# before_job = ["lean_production.utils.before_job"]
# after_job = ["lean_production.utils.after_job"]

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
# 	"lean_production.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []


doc_events = {
    
    "Sales Invoice": {
        "on_submit": "lean_production.lean_production.bottle_tracking.create_bottle_ledger_entry",
        "on_cancel": "lean_production.lean_production.bottle_tracking.cancel_bottle_ledger_entry"
    },
    "Water Purification Entry": {
        "on_submit": "lean_production.stock_automation.create_manufacture_stock_entry",
        "on_cancel": "lean_production.stock_automation.cancel_linked_stock_entry"
    },
    "Blow Molding Entry": {
        "on_submit": "lean_production.stock_automation.create_manufacture_stock_entry",
        "on_cancel": "lean_production.stock_automation.cancel_linked_stock_entry"
    },
    "Transaction Deletion Record": {
        "before_submit": "lean_production.lean_production.bottle_tracking.on_transaction_deletion_record_submit"
    },
    "Filling Entry": {
        "on_submit": "lean_production.stock_automation.create_manufacture_stock_entry",
        "on_cancel": "lean_production.stock_automation.cancel_linked_stock_entry"
    }
}



after_install = "lean_production.install.after_install"

app_include_js = "/assets/lean_production/js/help_menu.js"
