import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_article():
    try:
        # Fetch POST request data
        data = frappe.request.get_json()

        # Extract 'article' parameter from JSON data
        article = data.get('article')

        # Validate that 'article' parameter is provided
        if not article:
            return {"status": "Failed", "message": "Missing 'article' parameter"}

        # Fetch articles with the given title
        articles = frappe.get_all('Article', filters={'article': article}, fields=['*'])

        # Check if articles were found
        if not articles:
            return {"status": "Failed", "message": "No articles found"}

        return {
            "status": "success",
            "data": articles
        }

    except Exception as e:
        # Log the error message and return a failure response
        frappe.log_error(f"Error occurred in get_article method: {str(e)}", "get_article")
        return {"status": "Failed", "message": "An error occurred while retrieving the article"}
