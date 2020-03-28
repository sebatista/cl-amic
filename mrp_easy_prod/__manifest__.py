# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mrp Easy Prod",
    "summary": "Presenta un wizard para usar con una tablet al pie de cada "
               "centro de produccion",
    "version": "11.0.0.0.0",
    "development_status": "Beta",  # "Alpha|Beta|Production/Stable|Mature"
    "category": "Manufacture",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "excludes": [],
    "depends": [
        'base',
        'mrp',
        'hr'
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/mrp_wizard_security.xml',
        'views/mrp_prod_menus.xml',
        'wizards/prod_wizard_view.xml',
        'wizards/prod_wizard_view_2.xml',
        'wizards/lots_wizard_form.xml',
        'views/mrp_workcenter_view.xml',
        'views/hr_employee_view.xml',
    ],
    "qweb": [
    ]
}
