import frappe
from frappe import _
from frappe.utils import add_to_date, formatdate, getdate, nowdate
from frappe.utils.dashboard import cache_source
from frappe.utils.dateutils import get_from_date_from_timespan, get_period_ending


@frappe.whitelist()
@cache_source
def get(
	chart_name=None,
	chart=None,
	no_cache=None,
	filters=None,
	from_date=None,
	to_date=None,
	timespan=None,
	time_interval=None,
	heatmap_year=None,
):
	if chart_name and not chart:
		chart = frappe.get_doc("Dashboard Chart", chart_name)
	elif chart and isinstance(chart, str):
		chart = frappe._dict(frappe.parse_json(chart))
	elif not chart:
		chart = frappe._dict()

	timespan = timespan or getattr(chart, "timespan", None) or "Last Month"
	timegrain = time_interval or getattr(chart, "time_interval", None) or "Daily"

	if filters and isinstance(filters, str):
		filters = frappe.parse_json(filters)
	filters = filters or {}

	company = filters.get("company") or frappe.defaults.get_user_default("Company") or "Wateena"

	if not to_date:
		to_date = getattr(chart, "to_date", None) or nowdate()
	if not from_date or timespan != "Select Date Range":
		from_date = get_from_date_from_timespan(to_date, timespan)

	dates = get_dates_from_timegrain(from_date, to_date, timegrain)

	# Fetch all distinct items and their UOM from Filling Entry / Item
	items_query = frappe.db.sql("""
		SELECT DISTINCT fe.finished_good_item as item_code,
			COALESCE(i.stock_uom, fe.uom, 'Carton') as uom,
			COALESCE(i.item_name, fe.finished_good_item) as item_name
		FROM `tabFilling Entry` fe
		LEFT JOIN `tabItem` i ON fe.finished_good_item = i.name
		WHERE fe.company = %s AND fe.docstatus < 2
		ORDER BY fe.finished_good_item ASC
	""", (company,), as_dict=True)

	if not items_query:
		# Fallback if no company filter matched
		items_query = frappe.db.sql("""
			SELECT DISTINCT fe.finished_good_item as item_code,
				COALESCE(i.stock_uom, fe.uom, 'Carton') as uom,
				COALESCE(i.item_name, fe.finished_good_item) as item_name
			FROM `tabFilling Entry` fe
			LEFT JOIN `tabItem` i ON fe.finished_good_item = i.name
			WHERE fe.docstatus < 2
			ORDER BY fe.finished_good_item ASC
		""", as_dict=True)

	# Fetch daily aggregated sums per item
	records = frappe.db.sql("""
		SELECT posting_date, finished_good_item, SUM(good_qty) as total_qty
		FROM `tabFilling Entry`
		WHERE docstatus < 2
			AND posting_date >= %s
			AND posting_date <= %s
		GROUP BY posting_date, finished_good_item
	""", (getdate(from_date), getdate(to_date)), as_dict=True)

	# Build data matrix: {item_code: {date_obj: total_qty}}
	matrix = {}
	for row in records:
		item = row["finished_good_item"]
		p_date = getdate(row["posting_date"])
		if item not in matrix:
			matrix[item] = {}
		matrix[item][p_date] = float(row["total_qty"] or 0.0)

	# Format dates for x-axis
	labels = [formatdate(d.strftime("%Y-%m-%d")) for d in dates]

	# Ensure explicit stacking order:
	# Bottom block (Blue): FG-WATER-1.5L-06 [Pack]
	# Middle block (Pink): FG-WATER-0.5L-12 [Pack]
	# Top block (Purple): 19L-REFILL [Nos]
	desired_order = ["FG-WATER-1.5L-06", "FG-WATER-0.5L-12", "19L-REFILL"]
	sorted_items = []
	for item_key in desired_order:
		for it in items_query:
			if it["item_code"] == item_key:
				sorted_items.append(it)
				break
	for it in items_query:
		if it not in sorted_items:
			sorted_items.append(it)

	# Concise label mapping for existing standard items; any new item dynamically uses its item_name (or formatted item_code)
	known_labels = {
		"FG-WATER-1.5L-06": "1.5L",
		"FG-WATER-0.5L-12": "0.5L",
		"19L-REFILL": "19L Refill"
	}

	datasets = []
	for item_info in sorted_items:
		item_code = item_info["item_code"]
		uom = item_info.get("uom") or "Pack"
		# Dynamically derive concise label for any existing or newly introduced finished good
		if item_code in known_labels:
			item_label = known_labels[item_code]
		else:
			# If a new item is added, use its Item Name (shortened if needed) or Item Code
			raw_name = item_info.get("item_name") or item_code
			# Strip common prefixes like 'Bottled Water - ' or 'FG-' to keep legend compact
			item_label = raw_name.replace("Bottled Water - ", "").replace("FG-", "").strip()

		# Always appends the exact item UOM dynamically from the database
		series_name = f"{item_label} [{uom}]"
		values = []
		for d in dates:
			val = matrix.get(item_code, {}).get(d, 0.0)
			values.append(val)

		datasets.append({
			"name": series_name,
			"values": values
		})

	return {
		"labels": labels,
		"datasets": datasets,
	}


def get_dates_from_timegrain(from_date, to_date, timegrain):
	days = months = years = 0
	if "Daily" == timegrain:
		days = 1
	elif "Weekly" == timegrain:
		days = 7
	elif "Monthly" == timegrain:
		months = 1
	elif "Quarterly" == timegrain:
		months = 3

	dates = [getdate(from_date)]
	while dates[-1] < getdate(to_date):
		nxt = getdate(add_to_date(dates[-1], years=years, months=months, days=days))
		if nxt > getdate(to_date):
			break
		dates.append(nxt)
	return dates
