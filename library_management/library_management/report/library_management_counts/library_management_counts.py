import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = [
        {
            'fieldname': 'name',
            'label': _('Article Name'),
            'fieldtype': 'Data',
            'width': 200
        },
        {
            'fieldname': 'author',
            'label': _('Author'),
            'fieldtype': 'Data',
            'width': 200
        },
        {
            'fieldname': 'status',
            'label': _('Status'),
            'fieldtype': 'Select',
            'options': ['Issued','Available'],
            'width': 100
        },
        {
            'fieldname': 'isbn',
            'label': _('ISBN'),
            'fieldtype': 'Data',
            'width': 150
        },
        {
            'fieldname': 'publisher',
            'label': _('Publisher'),
            'fieldtype': 'Data',
            'width': 100
        },
        {
            'fieldname': 'price',
            'label': _('Price'),
            'fieldtype': 'Currency',
            'width': 100
        },
        {
            'fieldname': 'issue_count',
            'label': _('Issue Count'),
            'fieldtype': 'Int',
            'width': 150
        },
        {
            'fieldname': 'return_count',
            'label': _('Return Count'),
            'fieldtype': 'Int',
            'width': 150
        }

    ]
    article_list = frappe.db.get_all('Article',fields=['article','author','status','isbn','publisher','price'])

    sub_trans_issue = frappe.db.get_list("Library Transaction",{"docstatus":1,"type":"Issue",},pluck="name")
    sub_trans_return = frappe.db.get_list("Library Transaction",{"docstatus":1,"type":"Return",},pluck="name")

    for i in article_list:
        Issue_count = frappe.db.count("Articles",{"article":i.article,"parent":["in",sub_trans_issue]})
        Return_count = frappe.db.count("Articles",{"article":i.article,"parent":["in",sub_trans_return]})
        data.append({
             'name': i.article,
             'author': i.author,
             'status': i.status,
             'isbn': i.isbn,
             'publisher': i.publisher,
             'price': i.price,
             'issue_count': Issue_count,
             'return_count': Return_count
        })


    return columns, data
