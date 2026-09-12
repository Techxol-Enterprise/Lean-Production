$(document).on('app_ready', function() {
    // Add the manual link to the Help Dropdown
    setTimeout(function() {
        if (frappe.ui.toolbar) {
            frappe.ui.toolbar.add_dropdown_button('Help', __('Lean Production Manual'), function() {
                frappe.set_route('lean-production-manu');
            });
        }
    }, 1000);
});
