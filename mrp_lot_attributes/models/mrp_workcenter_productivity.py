# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    qty = fields.Integer(
        string='Cantidad producida'
    )
