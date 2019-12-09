# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api, _


class LotsWizard(models.TransientModel):
    _name = "lots.wizard"
    _description = 'Wizard para pedir lotes'

    product_id = fields.Many2one(
        'product.product',
        'Producto'
    )

    final_lot_id = fields.Many2one(
        'stock.production.lot', 'Lote',
        domain="[('product_id', '=', product_id)]"
    )

    caption = fields.Char(
    )

    def save(self):
        """ Salvar el lote en workorder
        """
        workorder_obj = self.env['mrp.workorder']
        id = self.env.context.get('workorder')
        workorder = workorder_obj.search([('id', '=', id)])
        workorder.final_lot_id = self.final_lot_id
