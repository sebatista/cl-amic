# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    """ Linea del picking, es la linea del remito
    """
    _inherit = 'stock.move.line'

    product_lot_qty = fields.Float(
        related='lot_id.product_qty',
        help='Cantidad de stock que hay en el lote de esta linea.',
        string='Existencias'
    )

    lot_char = fields.Char(
        string="Lote",
        help="Campo técnico para quitar la posibilidad de elegir lotes"
    )

    @api.onchange('lot_char')
    def onchange_lot_char(self):
        lot_obj = self.env['stock.production.lot']
        domain = [('product_id', '=', self.product_id.id), ('name', '=', self.lot_char)]
        _lot = lot_obj.search(domain)
        if _lot:
            self.lot_id = _lot
        else:
            raise UserError(_('El producto %s no tiene un lote %s')
                           % (self.product_id.default_code, self.lot_char))
