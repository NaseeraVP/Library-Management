import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {
            'fieldname': 'full_name',
            'label': _('Full Name'),
            'fieldtype': 'Data',
            'width': 250
        },
        {
            'fieldname': 'email_address',
            'label': _('Email Address'),
            'fieldtype': 'Data',
            'width': 250
        },
        {
            'fieldname': 'phone',
            'label': _('Phone'),
            'fieldtype': 'Data',
            'width': 150
        },
        {
            'fieldname': 'from_date',
            'label': _('Membership From'),
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'to_date',
            'label': _('Membership To'),
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'membership_status',
            'label': _('Membership Status'),
            'fieldtype': 'Data',
            'width': 150
        },
        {
            'fieldname': 'current_articles',
            'label': _('Current Articles Held'),
            'fieldtype': 'Data',
            'width': 250
        },
    ]

    today = frappe.utils.nowdate()

    query = """
    SELECT
        lm.full_name,
        lm.email_address,
        lm.phone,
        lm.name AS name,
        IF(membership.from_date IS NOT NULL, membership.from_date, NULL) AS from_date,
        IF(membership.to_date IS NOT NULL, membership.to_date, NULL) AS to_date,
        IF(membership.from_date IS NOT NULL, 'Valid Membership', 'No Membership') AS membership_status,
        GROUP_CONCAT(DISTINCT current_articles.article_name ORDER BY current_articles.article_name SEPARATOR ', ') AS current_articles
    FROM
        `tabLibrary Member` lm
    LEFT JOIN (
        SELECT
            lmem.library_member,
            lmem.from_date,
            lmem.to_date
        FROM
            `tabLibrary Membership` lmem
        WHERE
            lmem.docstatus = 1
            AND lmem.from_date <= %(today)s
            AND lmem.to_date >= %(today)s
        ORDER BY
            lmem.from_date DESC
    ) membership ON lm.name = membership.library_member
    LEFT JOIN (
        SELECT
            lt.library_member,
            la.name AS article_name
        FROM
            `tabLibrary Transaction` lt
        JOIN
            `tabArticles` la ON lt.article = la.name
        LEFT JOIN (
            SELECT
                library_member,
                article,
                MAX(date) AS last_return_date
            FROM
                `tabLibrary Transaction`
            WHERE
                type = 'Return'
                AND docstatus = 1
            GROUP BY
                library_member, article
        ) returns ON returns.library_member = lt.library_member
        AND returns.article = lt.article
        WHERE
            lt.type = 'Issue'
            AND lt.docstatus = 1
            AND (returns.last_return_date IS NULL OR lt.date > returns.last_return_date)
    ) current_articles ON lm.name = current_articles.library_member
    GROUP BY
        lm.full_name, lm.email_address, lm.phone, lm.name, membership.from_date, membership.to_date
    """

    members_data = frappe.db.sql(query, {"today": today}, as_dict=True)

    data = []

    for member in members_data:
        data.append({
            'full_name': member["full_name"],
            'email_address': member["email_address"],
            'phone': member["phone"],
            'from_date': member["from_date"],
            'to_date': member["to_date"],
            'membership_status': member["membership_status"],
            'current_articles': member["current_articles"] if member["current_articles"] else "No Articles Issued"
        })

    return columns, data
