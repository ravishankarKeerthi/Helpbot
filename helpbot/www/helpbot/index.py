import frappe


def get_context(context):
	context.no_cache = 1
	if frappe.session.user == "Guest":
		frappe.throw("Please log in to use Docbot.", frappe.PermissionError)
	return context
