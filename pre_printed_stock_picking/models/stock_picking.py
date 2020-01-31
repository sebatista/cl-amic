# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    internal = fields.Boolean(
        compute="_compute_internal"
    )

    def _compute_internal(self):
        for reg in self:
            reg.internal = reg.location_dest_id.usage == 'internal'
