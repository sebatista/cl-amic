# -----------------------------------------------------------------------------
#
#    Copyright (C) 2019  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------
{
    'name': 'scaffolding',
    'version': '11.0.0.0.0',
    'license': 'Other OSI approved licence',
    'category': 'Default Application',
    'summary': 'Customization for scaffolding',
    'author': 'jeo Software',
    'depends': [
        # basic applications
        'sale_management',
        'account_invoicing',
        'purchase',

        # minimum modules for argentinian localizacion + utilities + fixes
        'standard_depends_ce',

        # utilitarios adicionales
        'backend_theme',
    ],
    'data': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],

    #
    # Here begins docker-odoo-environment manifest
    # --------------------------------------------

    # if Enterprise it installs in a different directory than community
    'Enterprise': False,

    # port where odoo starts serving pages
    'port': '8069',

    # syntax version of repos and images
    'env_ver': 1,

    # example repos version 1
    'repos': [
        {'usr': 'jobiols', 'repo': 'cl-scaffolding', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'rafi16jan-backend-theme',
         'branch': '11.0'},

        {'usr': 'jobiols', 'repo': 'adhoc-odoo-argentina', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-argentina-sale', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-account-financial-tools',
         'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-account-payment', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-miscellaneous', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-argentina-reporting',
         'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-reporting-engine', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-aeroo_reports', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-sale', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-odoo-support', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-product', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'oca-partner-contact', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'oca-web', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'oca-server-tools', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'oca-social', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'oca-server-brand', 'branch': '11.0'},
    ],

    # example images version 1
    'docker': [
        {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-jeo', 'ver': '11.0'},
        {'name': 'postgres', 'usr': 'postgres', 'ver': '11.1-alpine'},
        {'name': 'nginx', 'usr': 'nginx', 'ver': 'latest'},
        {'name': 'aeroo', 'usr': 'adhoc', 'img': 'aeroo-docs'},
    ],

    # example repos version 2
    # Note that the branch of the repo to download is taken from the module
    # version
    'git-repos': [
        'https://github.com/jobiols/cl-scaffolding.git',
        'https://github.com/jobiols/odoo-addons.git',
        'https://github.com/jobiols/adhoc-odoo-argentina.git',
    ],

    # example images version 2
    'docker-images': [
        {'img': 'jobiols/odoo-jeo:11.0', 'name': 'odoo'},
        {'img': 'postgres:11.1-alpine', 'name': 'postgres'},
        {'img': 'adhoc/aeroo', 'name': 'aeroo'},
    ]
}
