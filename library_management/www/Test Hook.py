
import frappe
from frappe import _  # Importing the translation function
from frappe.model.document import Document
from frappe.utils import nowdate, add_days

def after_migrate():
    print("Migrated successfully")

# from frappe import _  # Importing the translation function
#
# def validate_library_member_role(doc, method):
#     if "Library member" in [role.role for role in doc.get("roles")]:
#         frappe.msgprint(_("User created successfully"))
#     else:
#         frappe.throw(_("User must have the 'Library member' role."))
