import frappe


@frappe.whitelist()
def search_help(query):
	"""
	Search Help Article records by title, keywords and content.
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
			(
				(title LIKE %(like_query)s) * 3 +
				(keywords LIKE %(like_query)s) * 2 +
				(content LIKE %(like_query)s) * 1
			) AS relevance
		FROM `tabHelp Article`
		WHERE
			title LIKE %(like_query)s
			OR keywords LIKE %(like_query)s
			OR content LIKE %(like_query)s
		ORDER BY relevance DESC, modified DESC
		LIMIT 8
		""",
		{"like_query": like_query},
		as_dict=True,
	)

	return results


@frappe.whitelist()
def get_official_docs_search_url(query):
	"""Builds a direct search URL into ERPNext's official docs site as a fallback."""
	import urllib.parse

	safe_query = urllib.parse.quote(query or "")
	return f"https://docs.erpnext.com/search?q={safe_query}"
