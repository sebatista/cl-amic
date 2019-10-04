# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "MRP Lot Attributes",
    "summary": "Add attributes to lot",
    "version": "11.0.0.0.0",
    "development_status": "Alpha",
    "category": "Stock",
    "website": "https://github.com/jobiols/cl-amic",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "preloadable": True,
    "depends": [
        'stock',
    ],
    "data": [
        "views/production_lot_views.xml",
        "views/stock_move_views.xml"
    ],
}
