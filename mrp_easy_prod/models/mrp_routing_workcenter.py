# For copyright and license notices, see __manifest__.py file in module root
from odoo import fields, models, api


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    time_cycle_manual = fields.Float(
        digits=(9, 9)
    )

    pzs_hour = fields.Integer(
        string="Piezas Hora"
    )

    @api.onchange('pzs_hour')
    def onchange_pzs_hour(self):
        self.time_cycle_manual = 60 / self.pzs_hour if self.pzs_hour else 0
