# For copyright and license notices, see __manifest__.py file in module root

from datetime import datetime
from odoo import fields, models, api
from pytz import timezone, utc
from odoo.exceptions import UserError


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
        string="Operador"
    )
    date_start1 = fields.Date(
        help="Fecha de inicio de la produccion"
    )
    date_end1 = fields.Date(
        help="Fecha de fin de la produccion se usa solo para terceros",
        default=False
    )
    time_start = fields.Float(
        help="Hora de inicio de la produccion",
        string="Hora inicial",
        default=0.004
    )
    # NO BORRAMOS ESTO PORQUE ESTOS TIPOS EN CUALQUIER MOMENTO ME PIDEN
    # QUE LO VUELVA A PONER.
    # register_log = fields.Boolean(
    #     help="Al tildar esto se podrán registrar datos de produccion, horas, "
    #          "cantidades, operador desde aqui.",
    #     string="Registrar partes de producción"
    # )

    # @api.model
    # def _default_time_end(self):
    #     """ Devuelve la hora actual en punto flotante localizada segun tz
    #     """
    #     now_utc = datetime.now(utc)
    #     tz = timezone(self.env.user.tz) if self.env.user.tz else utc
    #     now_local = now_utc.astimezone(tz)
    #     return now_local.hour + now_local.minute / 60

    time_end = fields.Float(
        help="Hora de finalizacion de la produccion",
        string="Hora final",
        default=0.004
    )
    ot = fields.Char(
        related='production_id.ot',
        readonly=True,
        string='Orden de Trabajo'
    )
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
    department_id = fields.Many2one(
        'hr.department',
        related="operator_id.department_id",
        help="Campo tecnico para determinar como se cargan las horas en el parte"
    )

    @api.depends('actual_ef', 'standard_ef')
    def _compute_efficiency(self):
        ae = self.actual_ef
        se = self.standard_ef
        self.efficiency = (ae / se) * 100 if se else 0

    @api.depends('qty_producing', 'date_start1', 'time_end', 'time_start',
                 'department_id', 'date_end1')
    def _compute_actual_ef(self):
        """ Calcular la eficiencia real en piezas/hora teniendo en cuenta si son
            procesos de terceros o procesos internos.
        """
        pz = self.qty_producing
        if self.department_id.id == 23: # operarios
            t = self.time_end - self.time_start

        elif self.department_id.id == 25: # terceros
            try:
                ds = datetime.strptime(self.date_start1,"%Y-%m-%d")
                de = datetime.strptime(self.date_end1,"%Y-%m-%d")
                t = (de - ds).days * 24
            except:
                t = 0

            if t < 0:
                raise UserError('La fecha inicial debe ser anterior a la final')
        else:
            t = 0

        # piezas / hora
        self.actual_ef = (pz / t) if t else 0

    @api.depends('operation_id.time_cycle_manual')
    def _compute_standard_ef(self):
        """ Calcular la eficiencia standard para esta operacion
        """
        tc = self.operation_id.time_cycle_manual
        self.standard_ef = 60 / tc if tc else 0
