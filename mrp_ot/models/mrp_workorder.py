# For copyright and license notices, see __manifest__.py file in module root

from datetime import datetime
from odoo import fields, models, api
from pytz import timezone, utc


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    operator_id = fields.Many2one(
        'hr.employee',
        help='Operador'
    )


class MrpWorkOrder(models.Model):
    _inherit = "mrp.workorder"

    operator_id = fields.Many2one(
        'hr.employee',
        help='Operador que esta a cargo de la producción',
        default=lambda self: self.env['hr.employee'].search(
            [('name', '=', 'Diferencia')], limit=1),
        string="Operador"
    )
    date_start1 = fields.Date(
        help="Fecha de inicio de la produccion",
        default=fields.Date.context_today
    )
    time_start = fields.Float(
        help="Hora de inicio de la produccion",
        string="Hora inicial",
        default=0.01
    )
    register_log = fields.Boolean(
        help="Al tildar esto se podrán registrar datos de produccion, horas, "
             "cantidades, operador desde aqui.",
        string="Registrar partes de producción"
    )

    @api.model
    def _default_time_end(self):
        """ Devuelve la hora actual en punto flotante localizada segun tz
        """
        now_utc = datetime.now(utc)
        tz = timezone(self.env.user.tz) if self.env.user.tz else utc
        now_local = now_utc.astimezone(tz)
        return now_local.hour + now_local.minute / 60

    time_end = fields.Float(
        help="Hora de finalizacion de la produccion",
        string="Hora final",
        default=_default_time_end
    )
    ot = fields.Char(
        related='production_id.ot',
        readonly=True,
        string='Orden de Trabajo'
    )
    """
        Se elimina la eficiencia que se calculaba al cargar los datos de prod
        porque ya no tiene sentido al no cargar las horas de inicio y fin.

    standard_ef = fields.Integer(
        help='Eficiencia standard para esta operacion en piezas por hora',
        string='Standard pz/h',
        readonly=True,
        compute='_compute_standard_ef'
    )
    actual_ef = fields.Integer(
        help='Eficiencia real para esta operacion en piezas por hora',
        string='Actual pz/h',
        compute='_compute_actual_ef',
        readonly=True
    )
    efficiency = fields.Float(
        help='Eficiencia porcentual relativa al standard',
        string='Eficiencia %',
        compute='_compute_efficiency',
        readonly=True
    )

    @api.depends('actual_ef', 'standard_ef')
    def _compute_efficiency(self):
        ae = self.actual_ef
        se = self.standard_ef
        self.efficiency = (ae / se) * 100 if se else 0

    @api.depends('qty_producing', 'date_start1', 'time_end', 'time_start')
    def _compute_actual_ef(self):
        "" " Calcular la eficiencia real en piezas/hora
        "" "
        pz = self.qty_producing
        t = self.time_end - self.time_start

        # piezas / hora
        self.actual_ef = (pz / t) if t else 0

    @api.depends('operation_id.time_cycle_manual')
    def _compute_standard_ef(self):
        "" " Calcular la eficiencia standard para esta operacion
        "" "
        tc = self.operation_id.time_cycle_manual
        self.standard_ef = 60 / tc if tc else 0
    """
