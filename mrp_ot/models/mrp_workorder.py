# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api


class MrpWorkOrder(models.Model):
    _inherit = "mrp.workorder"

    date_start1 = fields.Date(
        help="Fecha de inicio de la produccion"
    )
    time_start = fields.Float(
        help="Hora de inicio de la produccion",
        string="Hora inicial"
    )
    date_end = fields.Date(
        help="Fecha de finalizacion de la produccion",
        string="Fecha final"
    )
    time_end = fields.Float(
        help="Hora de finalizacion de la produccion",
        string="Hora final"
    )
    ot = fields.Char(
        compute='compute_ot',
        readonly=True,
        string='Orden de Trabajo'
    )

    @api.depends('worked_lot')
    def compute_ot(self):
        for rec in self:
            rec.ot = rec.worked_lot.ot if rec.worked_lot else False
