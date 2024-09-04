import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {
            'fieldname': 'article',
            'label': _('Article'),
            'fieldtype': 'Data',

            'width':250
        },
        {
            'fieldname': 'status',
            'label': _('Status'),
            'fieldtype': 'Select',
            'options': "\n Available\n Return"
        },

        {
            'fieldname': 'isbn',
            'label': _('ISBN'),
            'fieldtype': 'Data',

            'width':450
        },


        {
            'fieldname': 'publisher',
            'label': _('Publisher'),
            'fieldtype': 'Data',
            'width':450
        }
    ]


    data = frappe.db.get_list("Article", fields=["article","status","isbn","publisher"])

    return columns, data
