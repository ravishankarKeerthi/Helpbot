import frappe
import urllib.parse

# Direct routes for common topics — checked before falling back to search.
# Add more entries here anytime you notice a query that should route directly.
TOPIC_URL_MAP = {
    "stock reconciliation": "https://docs.frappe.io/erpnext/stock-reconciliation",
    "sales invoice": "https://docs.frappe.io/erpnext/sales-invoice",
    "purchase order": "https://docs.frappe.io/erpnext/purchase-order",
    "purchase invoice": "https://docs.frappe.io/erpnext/purchase-invoice",
    "delivery note": "https://docs.frappe.io/erpnext/delivery-note",
    "purchase receipt": "https://docs.frappe.io/erpnext/purchase-receipt",
    "stock entry": "https://docs.frappe.io/erpnext/stock-entry",
    "payment entry": "https://docs.frappe.io/erpnext/payment-entry",
    "gst": "https://docs.frappe.io/erpnext/gst-for-multiple-branches",
    "leave application": "https://docs.frappe.io/hr/leave-application",
    "leave approval": "https://docs.frappe.io/hr/leave-application",
    "bill of materials": "https://docs.frappe.io/erpnext/bill-of-materials",
    "bom": "https://docs.frappe.io/erpnext/bill-of-materials",
    "work order": "https://docs.frappe.io/erpnext/work-order",
    "quotation": "https://docs.frappe.io/erpnext/quotation",
    "sales order": "https://docs.frappe.io/erpnext/sales-order",
    "credit note": "https://docs.frappe.io/erpnext/credit-note",
    "debit note": "https://docs.frappe.io/erpnext/debit-note",
    "material request": "https://docs.frappe.io/erpnext/material-request",
    "opening stock": "https://docs.frappe.io/erpnext/opening-stock",
    "pricing rule": "https://docs.frappe.io/erpnext/pricing-rule",
    "price list": "https://docs.frappe.io/erpnext/price-lists",
    "chart of accounts": "https://docs.frappe.io/erpnext/chart-of-accounts",
    "journal entry": "https://docs.frappe.io/erpnext/journal-entry",
    "warehouse": "https://docs.frappe.io/erpnext/warehouse",
}


@frappe.whitelist()
def get_official_docs_search_url(query):
	"""
	Returns a direct link to the matching ERPNext docs page when the query
	matches a known topic. Otherwise falls back to a Google site-restricted
	search (docs.erpnext.com's own search has no working ?q= URL).
	"""
	q = (query or "").strip().lower()

	for topic, url in TOPIC_URL_MAP.items():
		if topic in q or q in topic:
			return url

	safe_query = urllib.parse.quote(f"site:docs.erpnext.com {query or ''}")
	return f"https://www.google.com/search?q={safe_query}"
