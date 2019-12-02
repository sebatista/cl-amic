# Copyright 2019  - jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class MrpWizard(models.TransientModel):
    _name = "mrp.wizard"
    _description = 'Wizard para datos de produccion'

    workcenter_id = fields.Many2one(
        'mrp.workcenter',
        help='centro de produccion',
    )
    user_id = fields.Many2one(
        'hr.employee',
        help='Operador',
    )
    state = fields.Selection(
        [('01', 'estado 01'),
         ('02', 'estado 02')],
        default='01'
    )

    @api.multi
    def next(self):
        self.ensure_one()

        print(self.workcenter_id.name)

        self.state = '02'
        return {
            'context': {
                'state': self.state,
                'workcenter': self.workcenter_id,
                'user_id': self.user_id
            },
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
