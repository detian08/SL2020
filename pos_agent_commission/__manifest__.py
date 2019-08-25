# -*- coding: utf-8 -*-
{
    'name': 'Pos sale agent commission',
    'version': '1.1',
    'category': 'Point of Sale',
    'sequence': 1,
    "author": "",
    "mail": "",
    'summary': '',
    'description': """
    """,
    'depends': [
        'pos_sale','hr','point_of_sale','pos_sale_agent'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/agent_view.xml',
        'views/pos_config.xml',
        'views/pos_report.xml',
        'views/pos_session.xml',
        'views/report.xml',
        'wizard/pay_commission.xml',

    ],
    'qweb': [
        'static/src/xml/pos_ticket.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
