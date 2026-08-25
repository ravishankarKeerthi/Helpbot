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
def search_help(query):
	"""
	Search Help Article records by title, keywords, content, and error fields.
	Returns best matches first. If nothing found, the widget will show
	a fallback link to search ERPNext's official docs site directly.
	"""
	query = (query or "").strip()
	if not query:
		return []

	like_query = f"%{query}%"

	results = frappe.db.sql(
		"""
		SELECT
			name, title, category, module, content,
			reference_url, is_official_erpnext_doc,
			error_message, root_cause,
			(
				(error_message LIKE %(like_query)s) * 4 +
				(title LIKE %(like_query)s) * 3 +
				(keywords LIKE %(like_query)s) * 2 +
				(root_cause LIKE %(like_query)s) * 2 +
				(content LIKE %(like_query)s) * 1
			) AS relevance
		FROM `tabHelp Article`
		WHERE
			title LIKE %(like_query)s
			OR keywords LIKE %(like_query)s
			OR content LIKE %(like_query)s
			OR error_message LIKE %(like_query)s
			OR root_cause LIKE %(like_query)s
		ORDER BY relevance DESC, modified DESC
		LIMIT 8
		""",
		{"like_query": like_query},
		as_dict=True,
	)

	return results


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
