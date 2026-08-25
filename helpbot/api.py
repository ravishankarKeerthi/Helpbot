import frappe


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
	Builds a fallback link that lands on the actual matching ERPNext docs page.
	docs.erpnext.com's own search is an in-page widget (no working ?q= URL),
	so a Google site-restricted search is used instead - it reliably opens
	the specific docs.erpnext.com page instead of a generic homepage.
	"""
	import urllib.parse

	safe_query = urllib.parse.quote(f"site:docs.erpnext.com {query or ''}")
	return f"https://www.google.com/search?q={safe_query}"
