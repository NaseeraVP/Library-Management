frappe.ui.form.on("Library Transaction", {
    onload: function(frm) {
        frm.set_query('library_member', () => {
            return {
                filters: {
                    "docstatus": 1,

                }
            };
        });
    },
    refresh: function(frm) {
        if (frm.doc.total_amount > 0) {
            frm.add_custom_button('PAY FINE', () => {
                // Check if articles field has a value
                console.log("Articles:", frm.doc.articles); // Debugging: Check if the articles field has a value

                // let articles_value = frm.doc.articles || "No articles available"; // Provide a default message if empty
                // Fetch article names from the child tabldoce 'Articles'
               let articles = frm.doc.articles || [];
               let article_names = articles.map(row => row.article).join(', ');

               if (!article_names) {
                   article_names = "No articles available";
               }

                let d = new frappe.ui.Dialog({
                    title: 'Enter details',
                    fields: [
                        {
                            label: 'Return Article',
                            fieldname: 'return_article',
                            fieldtype: 'Data',
                            default: article_names
                        },
                        {
                            label: 'Receipt Date',
                            fieldname: 'receipt_date',
                            fieldtype: 'Date',
                            default: frm.doc.date
                        },
                        {
                            label: 'Member Name:',
                            fieldname: 'member_name',
                            fieldtype: 'Data',
                            default: frm.doc.library_member
                        },
                        {
                            label: 'Fine Amount',
                            fieldname: 'fine_amount',
                            fieldtype: 'Currency',
                            default: frm.doc.total_amount
                        },
                    ],
                    size: 'small',
                    primary_action_label: 'Submit',
                    primary_action(values) {
                        frappe.call({
                            method: 'library_management.library_management.doctype.library_transaction.library_transaction.create_receipt',
                            args: {
                                return_article: values.return_article,
                                receipt_date: values.receipt_date,
                                member_name: values.member_name,
                                fine_amount: values.fine_amount
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.msgprint(`Receipt created: ${r.message}`);
                                }
                            }
                        });
                        d.hide();
                    }
                });

                d.show();
            });
        }
    }
});
