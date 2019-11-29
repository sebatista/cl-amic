# Copyright 2019  - jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


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
        self.status = '02'

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.wizard',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
