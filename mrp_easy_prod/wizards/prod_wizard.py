# Copyright 2019  - jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class WizardModel(models.TransientModel):
    _name = "mrp.wizard"

    name = fields.Char(

    )
    state = fields.Selection(
        [('01', 'estado 01'),
         ('02', 'estado 02')],
        default='01'
    )

    def next(self):
        self.ensure_one()
        self.state = '02'
        return {
            'context': {
                'state': self.state,
            },
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

