# -*- coding: utf-8 -*-

{
    'name': 'Pos analytic accounting',
    'version': '1.1',
    'category': 'accounting',
    'author': '',
    'sequence': 1,
    'depends': [
        'account',
        'point_of_sale',
    ],
    "data": [
        'views/pos_view.xml',
    ],
    'qweb': [
    ],
    'installable': True,
}
