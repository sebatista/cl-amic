# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'MRP OT',
    'summary': 'Gestionar e Imprimir Ordenes de Trabajo',
    'version': '11.0.0.0.0',
    'development_status': 'Alpha',
    'category': 'Tools',
    'website': 'http://jeosoft.com.ar',
    'author': 'jeo Software',
    'maintainers': ['jobiols'],
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'preloadable': True,
    'depends': [
        'mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/bom_view.xml',
        'views/ot_cover_report.xml'
    ],
}
