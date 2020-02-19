# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


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

"""
        # Need a loss in case of the real time exceeding the expected
        # timeline = self.env['mrp.workcenter.productivity']
        if self.duration < self.duration_expected:
            loss_id = self.env['mrp.workcenter.productivity.loss'].search(
                [('loss_type', '=', 'productive')], limit=1)
            if not len(loss_id):
                raise UserError(
                    _("You need to define at least one productivity loss in "
                      "the category 'Productivity'. Create one from the "
                      "Manufacturing app, menu: Configuration / Productivity "
                      "Losses."))
        else:
            loss_id = self.env['mrp.workcenter.productivity.loss'].search(
                [('loss_type', '=', 'performance')], limit=1)
            if not len(loss_id):
                raise UserError(
                    _("You need to define at least one productivity loss in "
                      "the category 'Performance'. Create one from the "
                      "Manufacturing app, menu: Configuration / Productivity "
                      "Losses."))
        for workorder in self:
            if workorder.production_id.state != 'progress':
                workorder.production_id.write({
                    'state': 'progress',
                    'date_start': datetime.now(),
                })


# Esto ponia un timeline para iniciar con la fecha hora de inicio, pero como
# cargamos en diferido no lo usamos.

#            timeline.create({
#                'workorder_id': workorder.id,
#                'workcenter_id': workorder.workcenter_id.id,
#                'description': _('Time Tracking: ')+self.env.user.name,
#                'loss_id': loss_id[0].id,
#                'date_start': datetime.now(),
#                'user_id': self.env.user.id
#            })

        return self.write({'state': 'progress',
                           'date_start': datetime.now(),
                           })

# no se para que estaba esto
#        timeline_obj = self.env['mrp.workcenter.productivity']
#        timeline = timeline_obj.search([], limit=1, order='id desc')
#        timeline.operator_id = self.operator_id
#        return ret

"""