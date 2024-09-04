import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryMembership(Document):
    def validate(self):
        # Ensure that to_date is greater than from_date
        if self.to_date <= self.from_date:
            frappe.throw("To Date must be greater than From Date")

    # check before submitting this document
    def before_submit(self):

        # Check if there is an active membership for this member
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                # Check if the membership's end date is later than this membership's start date
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")

        # Get loan period and compute to_date by adding loan_period to from_date
        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)


@frappe.whitelist()
def create_receipt(membership_id, amount, payment_date, payment_method):
    # Create the receipt document
    receipt = frappe.get_doc({
        "doctype": "Receipt",
        "receipt_date": payment_date,
        "name1": membership_id,
        "amount": amount,
        # Add other necessary fields here
    })
    receipt.insert()

    # Mark the membership as paid
    membership = frappe.get_doc("Library Membership", membership_id)
    membership.fee_paid = 1
    membership.save()

    frappe.msgprint(__('Receipt created successfully'))
