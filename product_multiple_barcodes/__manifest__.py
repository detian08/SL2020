# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Multiple Barcodes',
    "version": "13.0.1.0.0",
    'author': 'Yousuf Hussein',
    'license': 'LGPL-3',
    'installable': True,
    'images': ['static/description/main_banner.png'],
    'summary': 'Allows adding additional barcodes to your product.product and product.template models and search by these barcodes',
    'depends': [
       'product','point_of_sale','sale_management'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/point_of_sale_assets.xml',
    ],
}
