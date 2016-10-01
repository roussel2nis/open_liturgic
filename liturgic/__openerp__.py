# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Liturgic',
    'version' : '1.0',
    'summary': 'Manage liturgic organizations',
    'sequence': 30,
    'description': """
Liturgic
========

    """,
    'category' : 'Liturgic',
    'images' : [],
    'depends' : ['calendar','web_calendar'],
    'data': ['security/liturgic_security.xml',
        'views/celebration_view.xml',
        'security/ir.model.access.csv'
        
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
