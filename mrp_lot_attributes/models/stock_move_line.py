# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class StockMoveLine(models.Model):
    """ Linea del picking, es la linea del remito
    """
    _inherit = 'stock.move.line'

    product_lot_qty = fields.Float(
        related='lot_id.product_qty',
        help='Cantidad de stock que hay en el lote de esta linea.',
        string='Existencias'
    )
