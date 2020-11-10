# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class StockMoveLine(models.Model):
    """ Linea del picking, es la linea del remito
    """
    _inherit = 'stock.move.line'

    product_weight = fields.Float(
        string='peso neto del producto',
        related='lot_id.unit_lot_weight',
        help='Campo tecnico para poder imprimir el peso del producto en el '
             'remito'
    )
    boxes = fields.Integer(
        help='Cantidad de cajas que hay en esta linea del remito.',
        compute='_compute_boxes'
    )
    client_description = fields.Char(
        help='El nombre del producto segun el cliente al que se le envia',
        string='Descripcion del producto para el cliente',
        related='move_id.name'
    )

    @api.multi
    def _compute_boxes(self):
        for rec in self:
            # unidad de medida para la venta del producto
            uom = rec.product_id.uom_id
            factor = uom.factor
            factor_inv = uom.factor_inv if uom.factor_inv else 1
            # la cantidad de cajas es la cantidad de producto dividido por la
            # cantidad de productos por caja
            rec.boxes = rec.qty_done * factor / factor_inv
