# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    accum_qty = fields.Float(
        help='Total acumulado para consumir incluida la operacion corriente. '
             'Se compara con las existencias para prevenir que se consuma '
             'mas cantidad de la que hay en el lote del producto.',
        string='A consumir'
    )

    product_lot_qty = fields.Float(
        related='lot_id.product_qty',
        help='Cantidad de stock que hay en el lote de esta linea',
        string='Existencias'
    )
