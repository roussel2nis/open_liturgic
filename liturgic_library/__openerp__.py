# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Liturgic Library',
    'version' : '1.0',
    'summary': 'Manage liturgic libraries',
    'sequence': 30,
    'description': """
Liturgic Libraries
==================

    """,
    'category' : 'Liturgic',
    'images' : [],
    'depends' : ['liturgic'],
    'data': [
        'views/library_view.xml',
        'security/ir.model.access.csv'
        
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
