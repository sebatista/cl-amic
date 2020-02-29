# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    accum_qty = fields.Float(
        help='Total requerido para consumir hasta la operacion corriente. '
             'Se compara con el stock del lote para prevenir que se consuma '
             'mas cantidad de la que hay en stock.',
        string='A consumir'
    )

    product_lot_qty = fields.Float(
        related='lot_id.product_qty',
        help='Exponemos la cantidad de stock que hay en el lote de esta linea',
        string='Existencias'
    )
