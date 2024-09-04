import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = [
        {
            'fieldname': 'name',
            'label': _('Member ID'),
            'fieldtype': 'Link',
            'options': 'Library Member',

        },
        {
            'fieldname': 'full_name',
            'label': _('Name'),
            'fieldtype': 'Data',
            'width': 250
        },
        {
            'fieldname': 'email_address',
            'label': _('Email'),
            'fieldtype': 'Data',
            'width': 250
        },
        {
            'fieldname': 'membership_count',
            'label': _('Membership Count'),
            'fieldtype': 'Int',
			'width':150
        },
        {
            'fieldname': 'late_membership',
            'label': _('Membership Status'),
            'fieldtype': 'Data',

        },
        {
            'fieldname': 'membership_from',
            'label': _('Membership From'),
            'fieldtype': 'Date',
            'width': 150
        },
        {
            'fieldname': 'membership_to',
            'label': _('Membership To'),
            'fieldtype': 'Date',
            'width': 150
        },
        {
            'fieldname': 'transaction_count',
            'label': _('Transaction Count'),
            'fieldtype': 'Data',

        },
        {
            'fieldname': 'transaction_date',
            'label': _('Last Transaction'),
            'fieldtype': 'Date',
            'width': 250
        },
        {
            'fieldname': 'issued_art',
            'label': _('Issued Article'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'returned_art',
            'label': _('Returned Article'),
            'fieldtype': 'Data',
        },
    ]

    member_list = frappe.db.get_all('Library Member', fields=['name', 'full_name', 'email_address'])

    for i in member_list:
        membership_count = frappe.db.count("Library Membership", {"library_member": i.name, 'docstatus': 1})
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": i.name,
                "docstatus": 1,
                "from_date": ("<=", frappe.utils.nowdate()),
                "to_date": (">=", frappe.utils.nowdate()),
            }
        )
        membership_status = "Valid Membership" if valid_membership else "No Membership"
        check_membership = frappe.db.exists("Library Membership", {"library_member": i.name, "docstatus": 1})
        from_date, to_date = None, None

        if check_membership:
            membership_from = frappe.get_last_doc("Library Membership", {"library_member": i.name}, order_by="from_date asc")
            from_date, to_date = membership_from.from_date, membership_from.to_date

        last_trans = None
        transaction_count = frappe.db.count("Library Transaction", {"library_member": i.name, 'docstatus': 1})
        check_transaction = frappe.db.exists("Library Transaction", {"library_member": i.name, "docstatus": 1})

        if check_transaction:
            last_trans = frappe.get_last_doc("Library Transaction", {"library_member": i.name}, order_by="date asc").date

        sub_trans = frappe.db.get_list("Library Transaction", {"library_member": i.name, "docstatus": 1}, pluck="name")
        books_issued = ""
        books_returned = ""
        for tran in sub_trans:
            issued_article = frappe.db.get_value("Articles", {"parent": tran, "type": "Issue"}, "article")
            return_article = frappe.db.get_value("Articles", {"parent": tran, "type": "Return"}, "article")
            if issued_article:
                books_issued += issued_article + ","
            if return_article:
                books_returned += return_article + ","

        data.append({
            'name': i.name,
            'full_name': i.full_name,
            'email_address': i.email_address,
            'membership_count': membership_count,
            'late_membership': membership_status,
            'membership_from': from_date,
            'membership_to': to_date,
            'transaction_count': transaction_count,
            'transaction_date': last_trans,
            'issued_art': books_issued.strip(','),  # Remove trailing comma
            'returned_art': books_returned.strip(','),  # Remove trailing comma
        })

    return columns, data
