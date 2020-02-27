# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    ot = fields.Char(
        compute="_compute_ot"
    )

    def _compute_ot(self):
        """ exponer la ot del lote
        """
        for reg in self:
            reg.internal = reg.location_dest_id.usage == 'internal'
