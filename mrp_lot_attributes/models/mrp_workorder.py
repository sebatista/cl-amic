# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, _
from odoo.exceptions import UserError
import datetime as dt


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    worked_lot = fields.Many2one(
        'stock.production.lot', 'Lote',
        help="lote que se trabajo en esta workorder, para poder buscar por OT"
    )

    def record_production(self):
        """ Crear un registro en mrp.workcenter.productivity
        """

        if self.qty_producing <= 0:
            raise UserError(_('Please set the quantity you are currently '
                              'producing. It should be different from zero.'))

        if ((self.production_id.product_id.tracking != 'none') and
                not self.final_lot_id):
            raise UserError(_('You should provide a lot/serial number for '
                              'the final product'))

        if not self.date_start1 or not self.time_start:
            raise UserError(_('Por favor indique fecha y hora de comienzo de '
                              'la produccion.'))

        if not self.date_end or not self.time_end:
            raise UserError(_('Por favor indique fecha y hora de finalizacion '
                              'de la produccion.'))

        if not self.operator_id:
            raise UserError(_('Por favor indique que operador realizo esta '
                              'produccion.'))

        for move_line in self.active_move_line_ids:
            if (move_line.product_id.tracking != 'none'
                    and not move_line.lot_id):
                raise UserError(_('You should provide a lot/serial number '
                                  'for a component'))

        # copio el lote de salida porque por alguna razon odoo luego lo borra
        self.worked_lot = self.final_lot_id

        # aca le sumo 3 a las horas para pasar a utc a lo bruto.
        hr = dt.timedelta(hours=self.time_start)
        dy = dt.datetime.strptime(self.date_start1, '%Y-%m-%d')
        ds = (hr+dy+dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')

        hr = dt.timedelta(hours=self.time_end)
        dy = dt.datetime.strptime(self.date_end, '%Y-%m-%d')
        de = (hr+dy+dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')

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
            'operator_id': self.operator_id.id,
            'qty': self.qty_producing,
            'workcenter_id': self.workcenter_id.id,
            'loss_id': loss_prod.id,
            'workorder_id': self.id
        })

        super(MrpWorkorder, self).record_production()

    def button_start(self):
        """ Al arrancar la produccion hacemos el movimiento de los datos de
            lotes y ademas si es el primer lote de una ot le ponemos la OT
        """
        self.ensure_one()
        if not self.ot:
            raise UserError(_('La Orden de trabajo no tiene OT no se puede'
                              'continuar.'))

        for move_line in self.active_move_line_ids:
            if (move_line.product_id.tracking != 'none'
                    and not move_line.lot_id):
                raise UserError(_('You should provide a lot/serial number '
                                  'for a component'))

        if ((self.production_id.product_id.tracking != 'none') and
                not self.final_lot_id and self.move_raw_ids):
            raise UserError(_('You should provide a lot/serial number for '
                              'the final product'))

        # ver si hay que ponerle la ot al lote, esto pasa solo si el producto
        # esta habilitado para ot
        if self.product_id and self.product_id.enable_ot:
            # si el lote tiene una ot y si es distinta aviso.
            if self.final_lot_id.ot and self.final_lot_id.ot != self.ot:
                raise UserError(_('El lote destino pertenece a la OT %s lo '
                                  'cual no parece '
                                  'correcto') % self.final_lot_id.ot)

            # le pongo la ot al lote final
            self.final_lot_id.ot = self.ot

        # mover atributos
        for move_line in self.active_move_line_ids:
            # si el producto tiene trazabilidad propagar atributos
            if move_line.product_id.tracking != 'none':
                self.final_lot_id.propagate_from(move_line.lot_id)

        super().button_start()
