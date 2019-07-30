# -*- coding: utf-8 -*-

{
    'name': 'Inventory report with cost',
    'version': '1.1',
    'category': 'Inventory',
    'author': '',
    'sequence': 1,
    'depends': [
        'stock',
    ],
    "data": [
        'views/report_inventory.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
}
