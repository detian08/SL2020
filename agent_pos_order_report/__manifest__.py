# -*- coding: utf-8 -*-
{
    'name': 'Agent in Point of Sale Orders Statistics',
    'version': '1.1',
    'author': 'DevTalents',
    'sequence': 1,
    'website': 'www.dev-talents.com',
    'summary': 'Sale Report Pos Agent',
    'description': """
Sale Report Pos Agent
    """,
    'depends': ['sale', 'pos_sale_agent'],
    'data': [
        'report/sale_report_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
