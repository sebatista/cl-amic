# -*- coding: utf-8 -*-
{
    'name': 'Manufacturing Order Cancel/Reverse in Odoo',
    'version': '13.0.0.0',
    'category': 'Manufacturing',
    'summary': 'This module helps reverse a Done Manufacturing Order, '
               'allow to cancel Manufacturing Order and set to draft.',
    'author': 'jeo Software',
    'depends': ['base', 'mrp'],
    'data': ["views/mrp_production_views.xml", ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images": ['static/description/Banner.png'],
    "live_test_url": 'https://youtu.be/FSyn6axMrhA',
}
