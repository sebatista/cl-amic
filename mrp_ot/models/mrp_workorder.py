# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api
from datetime import datetime
from datetime import timedelta


class MrpWorkOrder(models.Model):
    _inherit = "mrp.workorder"

    date_start1 = fields.Date(
        help="Fecha de inicio de la produccion",
        default=fields.Date.context_today
    )
    time_start = fields.Float(
        help="Hora de inicio de la produccion",
        string="Hora inicial",
        default=8
    )
    time_end = fields.Float(
        help="Hora de finalizacion de la produccion",
        string="Hora final",
        default=18
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

    @api.depends('actual_ef', 'standard_ef')
    def _compute_efficiency(self):
        ae = self.actual_ef
        se = self.standard_ef
        self.efficiency = (ae / se) * 100 if se else 0

    @api.depends('qty_producing', 'date_start1', 'time_end', 'time_start')
    def _compute_actual_ef(self):
        """ Calcular la eficiencia real en piezas/hora
        """
        pz = self.qty_producing
        t = self.time_end - self.time_start

        # piezas / hora
        self.actual_ef = (pz / t) if t else 0

    @api.depends('operation_id.time_cycle_manual')
    def _compute_standard_ef(self):
        """ Calcular la eficiencia standard para esta operacion
        """
        tc = self.operation_id.time_cycle_manual
        self.standard_ef = 60 / tc if tc else 0
