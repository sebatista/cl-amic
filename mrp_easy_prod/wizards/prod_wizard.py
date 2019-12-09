# Copyright 2019  - jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from odoo.exceptions import UserError


class MrpWizard(models.TransientModel):
    _name = "mrp.wizard"
    _description = 'Wizard para datos de producción'

    stock_warehouse_id = fields.Many2one(
        'stock.warehouse',
        help='Planta',
    )
    workcenter_id = fields.Many2one(
        'mrp.workcenter',
        help='centro de producción',
    )
    user_id = fields.Many2one(
        'hr.employee',
        help='Operador',
    )
    work_order_id = fields.Many2one(
        'mrp.workorder',
        help='orden de trabajo',
    )
    state = fields.Selection(
        [('01', 'estado 01'),
         ('02', 'estado 02')],
        default='01'
    )

    @api.multi
    def next(self):
        self.ensure_one()

        # traer los workcenters con ordenes listas o en proceso empezar por
        # la mas vieja. Si hay ordenes en progreso se supone que son mas viejas
        # que las ordenes ready.
        domain = [('workcenter_id', '=', self.workcenter_id.id),
                  ('workcenter_id.order_ids.state', 'in',
                   ['ready', 'progress'])]
        self.work_order_id = self.work_order_id.search(
            domain, order='date_planned_start')

        if not self.work_order_id:
            raise UserError(_('No hay ordenes de trabajo listas o en proceso '
                              'en el centro %s' % self.workcenter_id.code))

        if not self.workcenter_id:
            raise UserError(_('Debe indicar cual es el centro de produccion'))

        if not self.user_id:
            raise UserError(_('Debe indicar cual es el operador del centro de '
                              'produccion'))

        self.work_order_id.operator_id = self.user_id

        return {
            'context': {
                'state': self.state,
                'workcenter': self.workcenter_id,
                'user_id': self.user_id
            },
            'res_model': 'mrp.workorder',
            'res_id': self.work_order_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'view_id': self.env.ref(
                'mrp_easy_prod.mrp_wizard_model_view_form_2').id,
        }
