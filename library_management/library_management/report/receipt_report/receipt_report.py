import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {
            'fieldname': 'return_article',
            'label': _('Return Article'),
            'fieldtype': 'Data',
            'width': 250
        },
        {
            'fieldname': 'receipt_date',
            'label': _('Receipt Date'),
            'fieldtype': 'Date',
            'width': 250
        },
        {
            'fieldname': 'member_name',
            'label': _('Member Name'),
            'fieldtype': 'Data',
            'width': 150
        },
        {
            'fieldname': 'fine_amount',
            'label': _('Fine Amount'),
            'fieldtype': 'Currency',  # Updated to 'Currency' fieldtype
            'width': 250
        }
    ]

    data = frappe.db.sql("""
        SELECT
            lr.return_article,
            lr.receipt_date,
            lr.member_name,
            lr.fine_amount
        FROM
            `tabLibrary Receipt` lr
        JOIN
            (SELECT
                return_article,
                MAX(receipt_date) AS latest_receipt_date
             FROM
                `tabLibrary Receipt`
             GROUP BY
                return_article
            ) latest_lr
        ON
            lr.return_article = latest_lr.return_article
            AND lr.receipt_date = latest_lr.latest_receipt_date
    """, as_dict=True)

    return columns, data
