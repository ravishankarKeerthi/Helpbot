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

# Common filler words that shouldn't count as meaningful search terms on their own.
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "in", "on", "at", "to",
    "of", "for", "and", "or", "if", "no", "not", "i", "it", "how", "what",
    "why", "do", "does", "did", "my", "me", "with", "from", "this", "that",
}


@frappe.whitelist()
def search_help(query):
	"""
	Search Help Article records by title, keywords, content, error_message,
	and root_cause — matching on individual words in the query rather than
	requiring the whole typed phrase to appear verbatim. This lets natural
	questions like "no camera in sadp" or "weight reversed" match articles
	that contain those words but not that exact sentence.
	"""
	query = (query or "").strip()
	if not query:
		return []

	# Break the query into individual meaningful words.
	raw_words = query.lower().split()
	words = [w for w in raw_words if w not in STOPWORDS and len(w) > 1]

	# Fallback: if everything got filtered out (e.g. query was just "is"),
	# use the raw words instead so we still search on something.
	if not words:
		words = raw_words

	if not words:
		return []

	# Build one OR'd relevance-scoring clause per word, then sum them all,
	# so articles matching more of the typed words rank higher.
	score_parts = []
	where_parts = []
	values = {}

	for i, word in enumerate(words):
		key = f"w{i}"
		values[key] = f"%{word}%"
		score_parts.append(f"""(
			(error_message LIKE %({key})s) * 4 +
			(title LIKE %({key})s) * 3 +
			(keywords LIKE %({key})s) * 2 +
			(root_cause LIKE %({key})s) * 2 +
			(content LIKE %({key})s) * 1
		)""")
		where_parts.append(f"""(
			title LIKE %({key})s
			OR keywords LIKE %({key})s
			OR content LIKE %({key})s
			OR error_message LIKE %({key})s
			OR root_cause LIKE %({key})s
		)""")

	score_sql = " + ".join(score_parts)
	where_sql = " OR ".join(where_parts)

	results = frappe.db.sql(
		f"""
		SELECT
			name, title, category, module, content,
			reference_url, is_official_erpnext_doc,
			error_message, root_cause,
			({score_sql}) AS relevance
		FROM `tabHelp Article`
		WHERE {where_sql}
		ORDER BY relevance DESC, modified DESC
		LIMIT 8
		""",
		values,
		as_dict=True,
	)

	# Filter out weak matches (e.g. a single word only found buried in
	# content) so genuinely unrelated articles don't block the fallback
	# to official ERPNext docs. Require at least a title or keyword hit,
	# or two-or-more weaker matches combined.
	MIN_RELEVANCE = 3
	results = [r for r in results if (r.get("relevance") or 0) >= MIN_RELEVANCE]

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
