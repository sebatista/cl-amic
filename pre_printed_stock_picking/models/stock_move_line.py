# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_weight = fields.Float(
        string='peso neto del producto',
        related='lot_id.produced_lot_weight',
        help='Campo tecnico para poder imprimir el peso del producto en el '
             'remito'
    )

    client_order_ref = fields.Char(
        string="Orden de compra del cliente",
        compute="_compute_client_order_ref",
        readonly=True
    )

    def _compute_client_order_ref(self):
        """ Busco la referencia del cliente en la SO, si es que la encuentro
            y la pongo en la referencia de cliente de stock picking
        """
        so_obj = self.env['sale.order']
        for rec in self:
            origin = rec.move_id.origin.strip()
            so = so_obj.search([('name', '=', origin)])
            ref = 'Ref: %s' % so.client_order_ref if so else "N/D"
            rec.client_order_ref = ref
