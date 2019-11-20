# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Remito Pre-impreso Aeroo",
    "summary": "Permite imprimir sobre remitos pre impresos",
    "version": "11.0.0.0.0",
    "development_status": "Alpha",
    "category": "Stock",
    "website": "https://github.com/jobiols/odoo-addons",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'l10n_ar_aeroo_stock',
        'base'
    ],
    "data": [
        'views/ir_sequence_view.xml',
        'report/invoice_report.xml',
    ],
}
