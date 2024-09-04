import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, nowdate

class LibraryMember(Document):
    def validate(self):
        self.validate_age()

    def validate_age(self):
        if self.date_of_birth:
            age = date_diff(nowdate(), self.date_of_birth) / 365.25
            if age < 13:
                frappe.throw("Member must be at least 13 years old.")
        else:
            frappe.throw("Date of Birth is required for age verification.")
