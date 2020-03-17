# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_weight = fields.Float(
        string='peso neto del producto',
        related='lot_id.produced_lot_weight',
        help='Campo tecnico para poder imprimir el peso del producto en el '
             'remito'
    )
