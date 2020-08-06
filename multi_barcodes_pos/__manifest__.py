# -*- coding: utf-8 -*-

{
    'name': 'POS Product Multi Barcode',
    'summary': """Allows to create multiple barcode for a single product""",
    'description': """Allows to create multiple barcode for a single product""",
    'author': 'M.Shorbagy',
    'category': 'Point of Sale',
    'depends': ['product', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/pos_template.xml',
    ],
    'installable': True,
    'auto_install': False,
}
