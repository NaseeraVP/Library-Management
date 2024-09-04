frappe.ui.form.on('Library Membership', {
    refresh: function(frm) {
      frm.set_query("library_member", () => {
        return {
          filters: {
            'docstatus':1,
            // 'full_name': 'Hayack ',
            'email_address':['like', '%@gmail.com']
          }
        }
      })
    },
    onload: function(frm) {
        // Add custom button to trigger payment dialog
        frm.add_custom_button(__('Pay Membership Fee'), function() {
            frm.events.make_payment(frm);
        });
    },

    from_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date && (frm.doc.to_date < frm.doc.from_date)) {
            frappe.msgprint({
                message: __("To Date should be greater than From Date"),
                indicator: 'green'
            });
            frm.set_value('from_date', "");
        }
    },

    to_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date && (frm.doc.to_date < frm.doc.from_date)) {
            frappe.msgprint({
                message: __("To Date should be later than From Date"),
                indicator: 'red'
            });
            frm.set_value('to_date', "");
        }
    },

    before_save: function(frm) {
        // Check if the membership fee has been paid
        if (!frm.doc.paid) {
            // Trigger the payment dialog
            frm.events.make_payment(frm);

            // Throw an error to prevent saving until the fee is paid
            frappe.throw(__('You must pay the membership fee before saving.'));
        }
    },

    make_payment: function(frm) {
        let d = new frappe.ui.Dialog({
            title: __('Pay Membership Fee'),
            fields: [
                {
                    label: 'Amount',
                    fieldname: 'amount',
                    fieldtype: 'Currency',
                    default: frm.doc.membership_fee,
                },
                {
                    label: 'Payment Date',
                    fieldname: 'payment_date',
                    fieldtype: 'Date',
                    default: frappe.datetime.get_today()
                },
                {
                    label: 'Payment Method',
                    fieldname: 'payment_method',
                    fieldtype: 'Select',
                    options: ['Cash', 'Credit Card', 'Bank Transfer'],
                    default: 'Cash'
                }
            ],
            primary_action_label: __('Pay'),
            primary_action(values) {
                // Update the paid field and save the document locally
                frm.set_value('paid', 1);
                frm.save().then(() => {
                    frappe.msgprint(__('Payment successfully recorded'));
                }).catch(err => {
                    frappe.msgprint(__('An error occurred while saving the document'));
                });
                d.hide();
            }
        });
        d.show();
    }
});
