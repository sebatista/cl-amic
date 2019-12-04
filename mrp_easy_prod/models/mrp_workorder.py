# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, _


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    operator_id = fields.Many2one(
        'hr.employee',
        help='Operador'
    )
