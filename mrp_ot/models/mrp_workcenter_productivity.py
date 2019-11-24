# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    user_id = fields.Many2one(
        'hr.employee', "Employee",
    )
