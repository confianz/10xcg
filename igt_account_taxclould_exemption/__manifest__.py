# # -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2020 (https://ingenieuxtech.odoo.com)
# info@ingenieuxtech.com
# ingenieuxtechnologies
#
##############################################################################
{
    'name': 'Account Taxcloud Exemption Certificate',
    'version': '13.0.0.1',
    'category': 'Accounting/Accounting',
    'summary': 'TaxCloud Exemption Certificate.',
    'description': """
        Enter exemption certificate purchase details and Get Exemption Certificate Id from tax Cloud.
        Use the certificate on sales order to get exemption and pass the same details on Invoice 
        to get exemption.
    """,
    'author': 'Ingenieux Technologies',
    'website': 'ingenieuxtech.odoo.com',
    'depends': ['account_accountant', 'account_taxcloud', 'sale_account_taxcloud'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_tax_certificate_view.xml',
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
        'views/sale_order_view.xml',
    ],
    'license': 'OPL-1',
    'price': 149.00,
    'currency': 'USD',
    'images': ['static/description/1-1.png', 'static/description/1-2.png', 'static/description/1-3.png'
               'static/description/1-4.png', 'static/description/1-5.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
