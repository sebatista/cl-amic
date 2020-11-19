# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# traceability
# https://www.youtube.com/watch?v=X8YY3FfVHF8

{
    "name": "MRP Lot Attributes",
    "summary": "Agregar atributos a lote.",
    "version": "11.0.1.0.5",
    "development_status": "Beta",  # "Alpha|Beta|Production/Stable|Mature"
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
        'mrp',
        'mrp_ot'
    ],
    "data": [
        "views/production_lot_views.xml",
        "views/mrp_workorder_view.xml",
        "views/mrp_workcenter_productivity.xml",
    ],
    "demo": [
        "demo/mrp_demo.xml",
    ],
    "sequence": 1
}
