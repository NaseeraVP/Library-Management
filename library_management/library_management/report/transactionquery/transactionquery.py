import frappe
from frappe import _

def execute(filters=None):
    # Define columns for the report
    columns = [
        {
            'fieldname': 'library_member',
            'label': _('Library Member'),
            'fieldtype': 'Link',
            'options': 'Library Member',
            'width': 150
        },
        {
            'fieldname': 'member_name',
            'label': _('Member Name'),
            'fieldtype': 'Data',
            'width': 200
        },
        {
            'fieldname': 'article',
            'label': _('Article'),
            'fieldtype': 'Link',
            'options': 'Article',
            'width': 200
        },
        {
            'fieldname': 'issue_date',
            'label': _('Issue Date'),
            'fieldtype': 'Date',
            'width': 150
        }
    ]

    # Fetch the latest issued article for each library member
    data = frappe.db.sql("""
        SELECT
            lt.library_member AS library_member,
            lm.full_name AS member_name,
            a.article AS article,
            MAX(lt.date) AS issue_date  -- Get the most recent issue date
        FROM
            `tabLibrary Transaction` lt
        JOIN
            `tabLibrary Member` lm ON lt.library_member = lm.name
        JOIN
            `tabArticles` a ON lt.name = a.parent
        WHERE
            a.type = 'Issue'
            AND lt.docstatus = 1
        GROUP BY
            lt.library_member, a.article, lm.full_name  -- Group by member and article
        ORDER BY
            lt.library_member, issue_date DESC  -- Order by member and issue date
    """, as_dict=True)

    return columns, data
