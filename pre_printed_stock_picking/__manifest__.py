# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Remito Pre-impreso Aeroo para AMIC",
    "summary": "Permite imprimir sobre remitos pre impresos",
    "version": "11.0.0.0.0",
    "development_status": "Beta",  # "Alpha|Beta|Production/Stable|Mature"
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
        'views/voucher_number_view.xml',
        'views/product_product_view.xml'
    ],
}
