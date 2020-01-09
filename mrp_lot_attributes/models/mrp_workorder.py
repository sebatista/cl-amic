# For copyright and license notices, see __manifest__.py file in module root

from odoo import models, _
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def record_production(self):
        """ Propagar los atributos al siguiente lote.
        """

        def propagate_attr(source, dest):
            """ Mover el atributo de un lote a otro teniendo en cuenta que si
                ya existe no lo tengo que copiar.
            """
            if not dest:
                return source

            if dest.find(source) == -1:
                return dest + ', ' + source
            else:
                return dest

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

        # mover atributos
        self.final_lot_id.colada = propagate_attr(
            move_line.lot_id.colada, self.final_lot_id.colada)
        self.final_lot_id.tt = propagate_attr(
            move_line.lot_id.tt, self.final_lot_id.tt)
        self.final_lot_id.paquete = propagate_attr(
            move_line.lot_id.paquete, self.final_lot_id.paquete)
        self.final_lot_id.ot = propagate_attr(
            move_line.lot_id.ot, self.final_lot_id.ot)

        super(MrpWorkorder, self).record_production()
