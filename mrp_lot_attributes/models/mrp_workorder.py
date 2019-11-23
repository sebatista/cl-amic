# For copyright and license notices, see __manifest__.py file in module root

from odoo import models, _
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def record_production(self):
        """ Propagar los atributos al siguiente lote.
        """

        if self.qty_producing <= 0:
            raise UserError(_('Please set the quantity you are currently '
                              'producing. It should be different from zero.'))

        if ((self.production_id.product_id.tracking != 'none') and
                not self.final_lot_id and self.move_raw_ids):
            raise UserError(_('You should provide a lot/serial number for '
                              'the final product'))

        for move_line in self.active_move_line_ids:
            if (move_line.product_id.tracking != 'none'
                    and not move_line.lot_id):
                raise UserError(_('You should provide a lot/serial number '
                                  'for a component'))

            if self.final_lot_id.colada:
                self.final_lot_id.colada += ', '+move_line.lot_id.colada
            else:
                self.final_lot_id.colada = move_line.lot_id.colada

            if self.final_lot_id.tt:
                self.final_lot_id.tt += ', '+move_line.lot_id.tt
            else:
                self.final_lot_id.tt = move_line.lot_id.tt

            if self.final_lot_id.paquete:
                self.final_lot_id.paquete += ', '+move_line.lot_id.paquete
            else:
                self.final_lot_id.paquete = move_line.lot_id.paquete

            if self.final_lot_id.ot:
                self.final_lot_id.ot += ', '+move_line.lot_id.ot
            else:
                self.final_lot_id.ot = move_line.lot_id.ot

        super(MrpWorkorder, self).record_production()
