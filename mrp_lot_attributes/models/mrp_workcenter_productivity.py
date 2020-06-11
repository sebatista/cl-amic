# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
import pytz


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    ot = fields.Char(
        related='workorder_id.ot',
        string='OT Amic'
    )
    workcenter = fields.Char(
        related='workcenter_id.code',
        string='Centro de produccion'
    )
    workorder = fields.Char(
        related='workorder_id.name',
        string='Orden de Trabajo'
    )
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

    def local2utc(self, dt):
        """ Convierte dt local --> UTC """
        tz = self.env.context.get('tz')
        tzone = pytz.timezone(tz) if tz else pytz.utc
        ret = tzone.localize(dt, is_dst=None).astimezone(pytz.utc)
        return ret

    def adjust_time(self, values):
        """ Ajusta el tiempo que esta en values, porque agregamos time que es
            un naive time y hay que pasarlo a UTC.

            Esto se llama siempre, asi que hay que diferenciar cuando el
            date_end esta en False eso significa que el operador sigue
            trabajando.
        """
        # caso en que registro el tiempo de inicio, el operador sigue
        # trabajando, sino no aparece el boton DONE
        if not values.get('time_start') and not values.get('time_end'):
            return values

        # datos que saca de aqui y de alla
        date = values.get('date') or self.date or fields.Datetime.now()
        time_start = values.get('time_start') or self.time_start or 0
        time_end = values.get('time_end') or self.time_end or 0

        dt = fields.Datetime.from_string(date)

        # pasa la hora a utc y crea el datetime
        dts = dt + timedelta(hours=time_start)
        dts = self.local2utc(dts)
        values['date_start'] = fields.Datetime.to_string(dts)

        dte = dt + timedelta(hours=time_end)
        dte = self.local2utc(dte)
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

    @api.multi
    def check_qty(self):
        """ Verificar las cantidades de piezas
        """
        for rec in self:
            # me traigo la wo del primer registro
            wo_id = rec.workorder_id

        # me traigo la cantidad total
        total_qty = wo_id.qty_produced

        # sumo la cantidad de todos los time_ids
        qty = sum(wo_id.time_ids.mapped('qty'))

        if qty > total_qty:
            raise UserError('La cantidad de piezas de las tareas supera '
                            'la cantidad de piezas de la orden')
