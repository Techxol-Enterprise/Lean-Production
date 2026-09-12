// Copyright (c) 2026, Techxol and contributors
// For license information, please see license.txt

frappe.ui.form.on("Blow Molding Entry", {
	setup: function(frm) {
		// Filter bottle_item to Semi Finished Goods branch
		frm.set_query("bottle_item", function() {
			return {
				query: "lean_production.stock_automation.item_group_query",
				filters: {
					"item_group": "Semi Finished Goods"
				}
			};
		});

		// Filter BOMs to only submitted, active BOMs for the selected bottle item
		frm.set_query("bom_no", function() {
			let filters = { is_active: 1, docstatus: 1 };
			if (frm.doc.bottle_item) {
				filters.item = frm.doc.bottle_item;
			}
			return { filters: filters };
		});

		// Filter source warehouse in child table to warehouses belonging to company
		frm.set_query("source_warehouse", "materials", function() {
			return {
				filters: {
					company: frm.doc.company || frappe.defaults.get_default("company"),
					is_group: 0
				}
			};
		});

		// Filter destination warehouse
		frm.set_query("target_warehouse", function() {
			return {
				filters: {
					company: frm.doc.company || frappe.defaults.get_default("company"),
					is_group: 0
				}
			};
		});

		// Filter operator to company employees
		frm.set_query("operator", function() {
			return {
				filters: {
					company: frm.doc.company || frappe.defaults.get_default("company"),
					status: "Active"
				}
			};
		});
	},

	refresh: function(frm) {
		// Auto-populate child table if empty and BOM + Quantities exist in draft
		if (frm.doc.docstatus === 0 && frm.doc.bom_no && (flt(frm.doc.good_qty) > 0 || flt(frm.doc.scrap_qty) > 0)) {
			if (!frm.doc.materials || frm.doc.materials.length === 0) {
				calculate_and_populate_materials(frm);
			}
		}
	},

	bottle_item: function(frm) {
		if (frm.doc.bottle_item) {
			frappe.db.get_value("BOM", { item: frm.doc.bottle_item, is_active: 1, is_default: 1, docstatus: 1 }, "name", function(r) {
				if (r && r.name) {
					frm.set_value("bom_no", r.name);
				} else {
					frappe.db.get_value("BOM", { item: frm.doc.bottle_item, is_active: 1, docstatus: 1 }, "name", function(r2) {
						if (r2 && r2.name) {
							frm.set_value("bom_no", r2.name);
						}
					});
				}
			});
		}
	},

	good_qty: function(frm) {
		frm.doc.bottles_produced_qty = frm.doc.good_qty;
		calculate_and_populate_materials(frm);
	},

	scrap_qty: function(frm) {
		calculate_and_populate_materials(frm);
	},

	bom_no: function(frm) {
		calculate_and_populate_materials(frm);
	}
});

frappe.ui.form.on("Lean Material Consumption", {
	source_warehouse: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.item_code && row.source_warehouse) {
			frappe.call({
				method: "lean_production.stock_automation.get_item_available_stock",
				args: {
					item_code: row.item_code,
					warehouse: row.source_warehouse
				},
				callback: function(r) {
					frappe.model.set_value(cdt, cdn, "available_stock", flt(r.message) || 0.0);
				}
			});
		}
	}
});

function calculate_and_populate_materials(frm) {
	const good_qty = flt(frm.doc.good_qty) || 0;
	const scrap_qty = flt(frm.doc.scrap_qty) || 0;
	const total_qty = good_qty + scrap_qty;

	if (!frm.doc.bom_no || total_qty <= 0) {
		return;
	}

	frappe.call({
		method: "lean_production.stock_automation.get_bom_material_details",
		args: {
			bom_no: frm.doc.bom_no,
			total_qty: total_qty,
			company: frm.doc.company
		},
		freeze: true,
		freeze_message: __("Calculating BOM material requirements..."),
		callback: function(r) {
			const items = Array.isArray(r.message) ? r.message : ((r.message && r.message.items) || []);
			if (items.length > 0) {
				frm.clear_table("materials");
				items.forEach(function(item) {
					let row = frm.add_child("materials");
					row.item_code = item.item_code;
					row.required_qty = flt(item.required_qty);
					row.uom = item.uom;
					row.source_warehouse = item.source_warehouse;
					row.available_stock = flt(item.available_stock);
				});
				frm.refresh_field("materials");
			}
		}
	});
}
