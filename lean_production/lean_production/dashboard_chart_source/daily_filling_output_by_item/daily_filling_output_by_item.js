frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["Daily Filling Output by Item"] = {
	method: "lean_production.lean_production.dashboard_chart_source.daily_filling_output_by_item.daily_filling_output_by_item.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company") || "Wateena",
		},
	],
};
