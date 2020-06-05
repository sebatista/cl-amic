# https://apps.odoo.com/apps/modules/11.0/bi_mrp_production_cancel/
{
    'name': 'Manufacturing Order Cancel/Reverse in Odoo',
    'version': '11.0.0.0',
    'category': 'Manufacturing',
    "development_status": "Alpha",  # "Alpha|Beta|Production/Stable|Mature"
    'summary': 'Permite revertir una orden de trabajo (MO) terminada, '
               'ademas cancelar una MO y volverla a Borrador.',
    'author': 'jeo Software',
    'depends': [
        'base',
        'mrp'
    ],
    'data': [
        "views/mrp_production_views.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
