# -*- coding: utf-8 -*-

{
    'name': 'Sale Extension',
    'version': '1.0',
    'category': 'Sales',
    'complexity': "easy",
    'description': """
 """,
    'author': 'Confianz Global',
    'website': 'http://www.confianzit.com',
    'depends': ['sale_management', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/generate_purchase_order.xml',
        'views/sale_views.xml',
        'views/order_state.xml',
        ],
    'qweb': [
    ],
    'installable': True,
    'application': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
