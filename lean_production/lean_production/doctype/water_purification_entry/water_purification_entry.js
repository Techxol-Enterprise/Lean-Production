// Copyright (c) 2026, Techxol and contributors
// For license information, please see license.txt

frappe.ui.form.on("Water Purification Entry", {
	setup: function(frm) {
		// Filter mineral_water_item to Mineral Water branch
		frm.set_query("mineral_water_item", function() {
			return {
				query: "lean_production.stock_automation.item_group_query",
				filters: {
					"item_group": "Mineral Water"
				}
			};
		});

		// Filter BOMs to only submitted, active BOMs for the selected mineral water item
		frm.set_query("bom_no", function() {
			let filters = { is_active: 1, docstatus: 1 };
			if (frm.doc.mineral_water_item) {
				filters.item = frm.doc.mineral_water_item;
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
			} else {
				check_material_shortages(frm);
			}
		} else {
			check_material_shortages(frm);
		}
	},

	mineral_water_item: function(frm) {
		if (frm.doc.mineral_water_item) {
			frappe.db.get_value("BOM", { item: frm.doc.mineral_water_item, is_active: 1, is_default: 1, docstatus: 1 }, "name", function(r) {
				if (r && r.name) {
					frm.set_value("bom_no", r.name);
				} else {
					frappe.db.get_value("BOM", { item: frm.doc.mineral_water_item, is_active: 1, docstatus: 1 }, "name", function(r2) {
						if (r2 && r2.name) {
							frm.set_value("bom_no", r2.name);
						}
					});
				}
			});
		}
	},

	good_qty: function(frm) {
		frm.doc.litres_purified = frm.doc.good_qty;
		calculate_and_populate_materials(frm);
	},

	scrap_qty: function(frm) {
		calculate_and_populate_materials(frm);
	},

	bom_no: function(frm) {
		calculate_and_populate_materials(frm);
	},

	before_submit: function(frm) {
		let shortages = get_material_shortages(frm);
		if (shortages.length > 0) {
			frappe.validated = false;
			show_shortage_dialog(frm, shortages);
			return false;
		}
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
					check_material_shortages(frm);
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
					row.item_name = item.item_name || item.item_code;
					row.required_qty = flt(item.required_qty);
					row.uom = item.uom;
					row.source_warehouse = item.source_warehouse;
					row.available_stock = flt(item.available_stock);
				});
				frm.refresh_field("materials");
				check_material_shortages(frm);
			}
		}
	});
}

function get_material_shortages(frm) {
	let shortages = [];
	(frm.doc.materials || []).forEach(function(row) {
		const req = flt(row.required_qty);
		const avail = flt(row.available_stock);
		if (req > 0 && avail < req) {
			shortages.push({
				item_code: row.item_code,
				item_name: row.item_name || row.item_code,
				required: req,
				available: avail,
				shortage: req - avail,
				uom: row.uom || "",
				warehouse: row.source_warehouse || ""
			});
		}
	});
	return shortages;
}

function check_material_shortages(frm) {
	if (frm.doc.docstatus !== 0) {
		frm.dashboard.clear_headline();
		return;
	}
	let shortages = get_material_shortages(frm);
	if (shortages.length > 0) {
		let headline_html = `⚠️ <b>Stock Shortage:</b> Insufficient stock to submit this entry. <a href="#" onclick="show_shortage_dialog(cur_frm); return false;" style="text-decoration: underline; font-weight: bold; margin-left: 8px;">View Shortage Details</a>`;
		frm.dashboard.set_headline_alert(headline_html, "orange");
	} else {
		frm.dashboard.clear_headline();
	}
}

window.show_shortage_dialog = function(frm, shortages) {
	shortages = shortages || get_material_shortages(frm);
	if (!shortages || shortages.length === 0) {
		frappe.msgprint(__("All raw materials have sufficient stock."));
		return;
	}

	let rows_html = shortages.map(s => `
		<tr style="border-bottom: 1px solid var(--border-color, rgba(255,255,255,0.08));">
			<td style="padding: 10px 14px; vertical-align: middle;">
				<div style="font-weight: 600; color: var(--text-color, #e6edf3); font-size: 13px;">${frappe.utils.escape_html(s.item_code)}</div>
				${s.item_name && s.item_name !== s.item_code ? `<div style="font-size: 11px; color: var(--text-muted, #8b949e); margin-top: 2px;">${frappe.utils.escape_html(s.item_name)}</div>` : ""}
			</td>
			<td style="padding: 10px 14px; text-align: right; vertical-align: middle; color: var(--text-color, #e6edf3); font-variant-numeric: tabular-nums;">
				${s.required.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} ${s.uom}
			</td>
			<td style="padding: 10px 14px; text-align: right; vertical-align: middle; color: var(--text-muted, #8b949e); font-variant-numeric: tabular-nums;">
				${s.available.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} ${s.uom}
			</td>
			<td style="padding: 10px 14px; text-align: right; vertical-align: middle;">
				<span style="display: inline-block; padding: 3px 8px; border-radius: 4px; background: rgba(239, 68, 68, 0.15); color: #f87171; font-weight: 700; font-variant-numeric: tabular-nums;">
					-${s.shortage.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} ${s.uom}
				</span>
			</td>
			<td style="padding: 10px 14px; vertical-align: middle; color: var(--text-color, #e6edf3); font-size: 12px;">
				<span style="color: var(--text-muted, #8b949e); margin-right: 4px;">📍</span>${frappe.utils.escape_html(s.warehouse)}
			</td>
		</tr>
	`).join("");

	let dialog = new frappe.ui.Dialog({
		title: __("Insufficient Raw Material Stock"),
		size: "large",
		fields: [
			{
				fieldname: "shortage_html",
				fieldtype: "HTML",
				options: `
					<div style="font-family: inherit; margin: 4px 0;">
						<div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 6px; padding: 12px 14px; margin-bottom: 14px;">
							<div style="font-weight: 600; color: #f87171; font-size: 13px; margin-bottom: 3px;">⚠️ Cannot Submit ${frm.doc.doctype}</div>
							<div style="font-size: 12px; color: var(--text-color, #e6edf3); opacity: 0.9;">
								The following raw materials have insufficient stock in their assigned source warehouses to complete this batch:
							</div>
						</div>

						<div style="border: 1px solid var(--border-color, #30363d); border-radius: 6px; overflow: hidden; margin-bottom: 14px; background: var(--card-bg, rgba(255,255,255,0.02));">
							<table style="width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left;">
								<thead>
									<tr style="background: var(--table-header-bg, rgba(255,255,255,0.05)); border-bottom: 1px solid var(--border-color, #30363d); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted, #8b949e);">
										<th style="padding: 10px 14px; width: 32%;">Raw Material</th>
										<th style="padding: 10px 14px; text-align: right; width: 17%;">Required</th>
										<th style="padding: 10px 14px; text-align: right; width: 17%;">Available</th>
										<th style="padding: 10px 14px; text-align: right; width: 17%;">Shortage</th>
										<th style="padding: 10px 14px; width: 17%;">Source Warehouse</th>
									</tr>
								</thead>
								<tbody>${rows_html}</tbody>
							</table>
						</div>

						<div style="background: rgba(59, 130, 246, 0.08); border-left: 3px solid #3b82f6; border-radius: 4px; padding: 10px 14px; font-size: 12px; line-height: 1.5; color: var(--text-color, #e6edf3);">
							<strong>Action Required:</strong> Please receive incoming stock via <strong>Purchase Receipt</strong> or <strong>Stock Entry (Material Receipt)</strong>, initiate a <strong>Material Transfer</strong> to the source warehouse, or reduce the production quantity.
						</div>
					</div>
				`
			}
		],
		primary_action_label: __("Close"),
		primary_action: function() {
			dialog.hide();
		}
	});
	dialog.show();
};
