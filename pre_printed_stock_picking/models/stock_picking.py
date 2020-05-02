# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    internal = fields.Boolean(
        compute="_compute_internal"
    )

    @api.multi
    def _compute_internal(self):
        """ Si el deposito al que envio es una ubicacion interna pongo
            internal = True para permitir cambiar el layout del remito
        """
        for reg in self:
            reg.internal = reg.location_dest_id.usage == 'internal'
