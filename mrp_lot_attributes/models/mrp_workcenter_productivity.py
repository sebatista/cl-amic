# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
import pytz


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    qty = fields.Float(
        string='Cantidad producida'
    )
    qty_total = fields.Float(
        related='workorder_id.qty_produced',
        readonly=True,
        string='Cantidad total producida',
        help='Cantidad total producida en la MO, debe ser igual a la suma de '
             'los partes de horas.'
    )
    date = fields.Date(
        string='Fecha de producción',
        help='Fecha en la que se hizo la produccion',
        default=fields.Datetime.now
    )
    time_start = fields.Float(
        string='Hora de inicio',
        help='Hora en la que inicio la producción'
    )
    time_end = fields.Float(
        string='Hora de fin',
        help='Hora en la que finalizó la producción'
    )

    @api.constrains('time_start', 'time_end')
    def check_time(self):
        for rec in self:
            if rec.time_start > rec.time_end:
                raise ValidationError('La hora de inicio debe sera anterior '
                                      'a la hora de fin.')

    def utc2local(self, dt):
        tz = self.env.context.get('tz')
        tzone = pytz.timezone(tz) if tz else pytz.utc
        ret = tzone.localize(dt, is_dst=None).astimezone(pytz.utc)
        return ret

    def adjust_time(self, values):
        date = values.get('date') or self.date 
        time_start = values.get('time_start') or self.time_start
        time_end = values.get('time_end') or self.time_end

        dt = fields.Datetime.from_string(date)
        dts = dt + timedelta(hours=time_start)
        dts = self.utc2local(dts)
        values['date_start'] = fields.Datetime.to_string(dts)

        dte = dt + timedelta(hours=time_end)
        dte = self.utc2local(dte)
        values['date_end'] = fields.Datetime.to_string(dte)
        return values

    @api.model
    def create(self, values):
        values = self.adjust_time(values)
        ret = super(MrpWorkcenterProductivity, self).create(values)
        self.check_qty()
        return ret

    @api.multi
    def write(self, values):
        values = self.adjust_time(values)
        ret = super(MrpWorkcenterProductivity, self).write(values)
        self.check_qty()
        return ret

    def check_qty(self):
        """ Verificar las cantidades de piezas
        """
        # me traigo la wo de un registro cualquiera
        wo_id = self.workorder_id

        # me traigo la cantidad total
        total_qty = wo_id.qty_produced

        # sumo la cantidad de todos los time_ids
        qty = sum(wo_id.time_ids.mapped('qty'))

        if qty > total_qty:
            raise UserError('La cantidad de piezas de las tareas supera la '
                            'cantidad de piezas de la orden')
