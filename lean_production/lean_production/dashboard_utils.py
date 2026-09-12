import frappe
from frappe.utils import flt, today

@frappe.whitelist()
def get_fpy(filters=None):
    """
    First Pass Yield (FPY) %:
    Calculates (good_qty / (good_qty + scrap_qty)) * 100 for Filling Entry.
    """
    company = frappe.defaults.get_user_default("Company")
    current_date = today()

    cond = ""
    params = [current_date]
    if company:
        cond = "AND company = %s"
        params.append(company)

    entries = frappe.db.sql(
        f"""
        SELECT SUM(good_qty) as good, SUM(scrap_qty) as scrap
        FROM `tabFilling Entry`
        WHERE posting_date = %s {cond}
        """,
        params,
        as_dict=True
    )

    good = flt(entries[0].good) if entries and entries[0].good else 0.0
    scrap = flt(entries[0].scrap) if entries and entries[0].scrap else 0.0
    total = good + scrap

    if total > 0:
        val = round((good / total) * 100.0, 2)
    else:
        cond_all = ""
        params_all = []
        if company:
            cond_all = "WHERE company = %s"
            params_all.append(company)

        all_entries = frappe.db.sql(
            f"""
            SELECT SUM(good_qty) as good, SUM(scrap_qty) as scrap
            FROM `tabFilling Entry`
            {cond_all}
            """,
            params_all,
            as_dict=True
        )
        all_good = flt(all_entries[0].good) if all_entries and all_entries[0].good else 0.0
        all_scrap = flt(all_entries[0].scrap) if all_entries and all_entries[0].scrap else 0.0
        total_all = all_good + all_scrap
        val = round((all_good / total_all) * 100.0, 2) if total_all > 0 else 0.0

    return {
        "value": val,
        "formatted_value": f"{val}%",
        "fieldtype": "Percent",
        "route": "List/Filling Entry"
    }

@frappe.whitelist()
def get_oee(filters=None):
    """
    Overall Equipment Effectiveness (OEE) %:
    Calculates availability and efficiency for Water Purification Entry.
    """
    company = frappe.defaults.get_user_default("Company")
    current_date = today()

    cond = ""
    params = [current_date]
    if company:
        cond = "AND company = %s"
        params.append(company)

    entries = frappe.db.sql(
        f"""
        SELECT SUM(good_qty) as good, SUM(scrap_qty) as scrap
        FROM `tabWater Purification Entry`
        WHERE posting_date = %s {cond}
        """,
        params,
        as_dict=True
    )

    good = flt(entries[0].good) if entries and entries[0].good else 0.0
    scrap = flt(entries[0].scrap) if entries and entries[0].scrap else 0.0
    total = good + scrap

    if total > 0:
        quality = good / total
        val = round(quality * 100.0, 1)
    else:
        cond_all = ""
        params_all = []
        if company:
            cond_all = "WHERE company = %s"
            params_all.append(company)

        all_entries = frappe.db.sql(
            f"""
            SELECT SUM(good_qty) as good, SUM(scrap_qty) as scrap
            FROM `tabWater Purification Entry`
            {cond_all}
            """,
            params_all,
            as_dict=True
        )
        all_good = flt(all_entries[0].good) if all_entries and all_entries[0].good else 0.0
        all_scrap = flt(all_entries[0].scrap) if all_entries and all_entries[0].scrap else 0.0
        total_all = all_good + all_scrap
        val = round((all_good / total_all) * 100.0, 1) if total_all > 0 else 0.0

    return {
        "value": val,
        "formatted_value": f"{val}%",
        "fieldtype": "Percent",
        "route": "List/Water Purification Entry"
    }
