# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    name = fields.Char(
        'Lote/Numero de Ingreso',
        default=lambda self: '%s.00' % self.env['ir.sequence'].next_by_code(
            'stock.lot.serial'),
        required=True,
        help="Numero unico de ingreso")

    colada = fields.Char(
        string='COLADA'
    )
    tt = fields.Char(
        string='TT',
        help='Tratamiento Termico'
    )
    paquete = fields.Char(
        string='PAQUETE'
    )
    ot = fields.Char(
        string='OT',
        help='Orden de Trabajo'
    )
