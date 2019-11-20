# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductionLot(models.Model):
    _inherit = "ir.sequence"

    implementation = fields.Selection(
        selection_add=[('manual', 'Manual')]
    )
