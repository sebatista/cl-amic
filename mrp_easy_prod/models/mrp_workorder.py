# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, _


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    operator_id = fields.Many2one(
        'hr.employee',
        help='Operador'
    )


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    operator_id = fields.Many2one(
        'hr.employee',
        help='Operador'
    )

    def button_start(self):
        ret = super().button_start()

        timeline_obj = self.env['mrp.workcenter.productivity']
        timeline = timeline_obj.search([], limit=1, order='id desc')
        timeline.operator_id = self.operator_id

        return ret
