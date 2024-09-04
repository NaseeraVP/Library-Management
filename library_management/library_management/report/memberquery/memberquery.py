from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {
            'fieldname': 'library_member',
            'label': _('Library Member'),
            'fieldtype': 'Data',
            'width': 250
        },
        {
            'fieldname': 'from_date',
            'label': _('From Date'),
            'fieldtype': 'Date',
            'width': 150
        },
        {
            'fieldname': 'to_date',
            'label': _('To Date'),
            'fieldtype': 'Date',
            'width': 150
        },
    ]

    # Query to fetch data from Library Transaction and Library Membership
    data = frappe.db.sql("""
        SELECT
            lt.library_member,
            lm.from_date,
            lm.to_date
        FROM
            `tabLibrary Transaction` lt
        LEFT JOIN
            `tabLibrary Membership` lm ON lt.library_member = lm.library_member
    """, as_dict=True)

    return columns, data
