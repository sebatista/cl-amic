# For copyright and license notices, see __manifest__.py file in module root
from odoo import fields, models


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    time_cycle_manual = fields.Float(
        digits=(9, 9)
    )
