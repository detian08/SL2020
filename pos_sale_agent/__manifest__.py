# -*- coding: utf-8 -*-
{
    'name': 'Pos sale agent',
    'version': '12.1',
    'category': 'Point of Sale',
    'sequence': 1,
    "author": "",
    "mail": "",
    'summary': '',
    'description': """
    """,
    'depends': [
        'pos_sale','hr','point_of_sale','aar_pos_ticket'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/agent_views.xml',
        'views/template.xml',
        'data/barcode_patterns.xml',
    ],
    'qweb': [
        'static/src/xml/pos_ticket.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
