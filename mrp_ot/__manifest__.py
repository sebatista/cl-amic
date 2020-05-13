# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'MRP OT',
    'summary': 'Gestionar e Imprimir Ordenes de Trabajo',
    'version': '11.0.0.0.0',
    "development_status": "Beta",  # "Alpha|Beta|Production/Stable|Mature"
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
        'product',
        'web_widget_timepicker',
        'mrp_easy_prod',
        'stock'
    ],
    'data': [
        'data/ot_sequence_data.xml',
        'security/ir.model.access.csv',
        'report/ot_cover_report.xml',
        'views/product_view.xml',
        'views/bom_view.xml',
        'views/mrp_production_view.xml',
        'views/ot_production_workcenter_view.xml',
        'views/ot_amic.xml',
        'views/stock_scheduler_compute_view.xml'
    ],
    'external_dependencies': {
        'python': [
            'pdf2image',
        ],
    },
}
