# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    internal = fields.Boolean(
        compute="_compute_internal",
        help='Indica si el movimiento es interno o sea se mueve a un proceso '
             'tercerizado o si el movimiento es a un cliente.'
    )
    client_order_ref = fields.Char(
        string="Orden de compra del cliente",
        compute="_compute_client_order_ref",
        readonly=True
    )

    @api.multi
    def _compute_internal(self):
        """ Si el deposito al que envio es una ubicacion interna pongo
            internal = True para permitir cambiar el layout del remito
        """
        for reg in self:
            reg.internal = reg.location_dest_id.usage == 'internal'

    @api.multi
    def _compute_client_order_ref(self):
        """ Busco la referencia del cliente en la SO, si es que la encuentro
            y la pongo en la referencia de cliente de stock picking
        """
        so_obj = self.env['sale.order']
        for rec in self:
            if rec.origin:
                _so = so_obj.search([('name', '=', rec.origin.strip())])
                ref = 'OC: %s' % _so.client_order_ref if _so else "N/D"
                rec.client_order_ref = ref
