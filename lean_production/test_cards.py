import frappe
import json
from frappe.desk.doctype.number_card.number_card import get_result

def test_cards():
    cards = [
        "Total Water Purified Today",
        "Water Purified Scrap Today",
        "Bottles Molded Today",
        "Bottle Scrap Today",
        "Finished Goods Filled Today",
        "19L Bottles Delivered (MTD)",
        "19L Bottles Received (MTD)",
        "First Pass Yield (FPY) %",
        "Overall Equipment Effectiveness (OEE)",
        "Finished Goods Current Stock",
        "Available Raw Material"
    ]
    for c in cards:
        doc = frappe.get_doc("Number Card", c)
        flts = json.loads(doc.filters_json or "[]")
        val = get_result(doc, filters=flts)
        print(f"Card '{c}': value = {val}")

if __name__ == "__main__":
    test_cards()
