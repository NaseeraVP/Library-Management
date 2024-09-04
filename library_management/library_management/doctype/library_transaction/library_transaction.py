import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate

class LibraryTransaction(Document):

    def before_save(self):
        lost_fine = frappe.db.get_single_value("Library Settings", "late_return_fine")
        damage_fine = frappe.db.get_single_value("Library Settings", "damage_fine_factor")
        lost_factor = frappe.db.get_single_value("Library Settings", "lost_fine_factor")
        borrow_period = frappe.db.get_single_value("Library Settings", "book_borrow_period")
        total_fine = 0

        for i in self.articles:
            total_return_fine = 0.0
            trans_type = i.get('type')
            article = frappe.get_doc("Article", i.article)
            price = article.price

            if trans_type == "Return":
                issued_transactions = frappe.get_all(
                    "Library Transaction",
                    filters={"library_member": self.library_member, "type": "Issue", "docstatus": 1},
                    fields=["name", "date"],
                    order_by="date desc"
                )

                issue_date = None
                for transaction in issued_transactions:
                    if frappe.db.exists("Articles", {"article": i.article, "parent": transaction["name"]}):
                        issue_date = transaction["date"]
                        break

                if issue_date:
                    overdue_days = date_diff(getdate(self.date), getdate(issue_date)) - borrow_period
                    overdue_days = max(0, overdue_days)  # Ensure non-negative overdue days
                    if overdue_days > 0:
                        fine = overdue_days * lost_fine
                        total_return_fine += fine

                fine_type = i.get('fine')
                if fine_type == "Damage Fine":
                    fine = damage_fine
                elif fine_type == "Lost Fine":
                    fine = price * lost_factor
                else:
                    fine = 0

                total_fine += fine + total_return_fine

        self.total_amount = total_fine

    def before_submit(self):
        self.validate_maximum_limit()  # Validate before submitting the transaction
        for i in self.articles:
            article = frappe.get_doc("Article", i.article)
            if i.type == "Issue":
                self.validate_issue(article)
                article.status = "Issued"
                article.save()

            elif i.type == "Return":
                self.validate_return(article)
                article.status = "Available"
                article.save()
    

    def validate_issue(self, article):
        self.validate_membership()
        if article.status == "Issued":
            frappe.throw(f"Article {article.name} is already issued by another member")

    def validate_return(self, article):
        if article.status == "Available":
            frappe.throw(f"Article {article.name} cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "type": "Issue", "docstatus": 1},
        )
        if count + len(self.articles) > max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # Make sure to validate with the correct field names
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<=", self.date),
                "to_date": (">=", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

@frappe.whitelist()
def create_receipt(return_article,receipt_date, member_name, fine_amount):
    receipt_doc = frappe.get_doc({
        'doctype': 'Library Receipt',
        'return_article': return_article,
        'receipt_date': receipt_date,
        'member_name': member_name,
        'fine_amount': fine_amount
    })
    receipt_doc.insert()
    frappe.db.commit()
    return receipt_doc.name
