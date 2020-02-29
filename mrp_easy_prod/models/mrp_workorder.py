# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


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
        """ Arranca la orden de trabajo.
            Esto no llama al super porque copie el metodo original
        """
        # volvemos al original porque no anduvo
        return super(MrpWorkorder, self).button_start()

        self.ensure_one()
        # As button_start is automatically called in the new view
        if self.state in ('done', 'cancel'):
            return True
