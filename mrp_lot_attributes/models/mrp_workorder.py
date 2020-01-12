# For copyright and license notices, see __manifest__.py file in module root

from odoo import models, _
from odoo.exceptions import UserError
import datetime


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def record_production(self):
        """ Crear un registro en mrp.workcenter.productivity y
            Propagar los atributos al siguiente lote.
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

        if not self.date_start1 or not self.time_start:
            raise UserError(_('Por favor indique fecha y hora de comienzo de '
                              'la produccion.'))

        if not self.date_end or not self.time_end:
            raise UserError(_('Por favor indique fecha y hora de finalizacion '
                              'de la produccion.'))

        if not self.user_id:
            raise UserError(_('Por favor indique que operador realizo esta '
                              'produccion.'))

        for move_line in self.active_move_line_ids:
            if (move_line.product_id.tracking != 'none'
                and not move_line.lot_id):
                raise UserError(_('You should provide a lot/serial number '
                                  'for a component'))

        ds = '%s %s' % (self.date_start1,
                        '{0:02.0f}:{1:02.0f}'.format(
                            *divmod(self.time_start * 60, 60)))
        de = '%s %s' % (self.date_end,
                        '{0:02.0f}:{1:02.0f}'.format(
                            *divmod(self.time_end * 60, 60)))

        if ds >= de:
            raise UserError(_('El fin de la produccion debe ser posterior al '
                              'inicio.'))

        loss = self.env['mrp.workcenter.productivity.loss']
        loss_prod = loss.search([('loss_type', '=', 'productive')], limit=1)

        # crear el registro de tiempo
        wcp = self.env['mrp.workcenter.productivity']
        wcp.create({
            'date_start': ds,
            'date_end': de,
            'user_id': self.user_id.id,
            'qty': self.qty_producing,
            'workcenter_id': self.workcenter_id.id,
            'loss_id': loss_prod.id,
            'workorder_id': self.id
        })

        self.date_start1 = False
        self.time_start = False
        self.date_end = False
        self.time_end = False

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
