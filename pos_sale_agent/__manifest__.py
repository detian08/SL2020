# -*- coding: utf-8 -*-
{
    'name': 'Pos sale agent',
    'version': '1.1',
    'category': 'Point of Sale',
    'sequence': 1,
    "author": "",
    "mail": "",
    'summary': '',
    'description': """
    """,
    'depends': [
        'pos_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/agent_views.xml',
        'views/template.xml',
        'data/barcode_patterns.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
