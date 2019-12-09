# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string="Planta",
        help='Planta'
    )
