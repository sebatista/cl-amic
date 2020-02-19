# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

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
    remito_proveedor = fields.Char(
        string='Remito Proveedor'
    )
    fecha_remito = fields.Date(
    )
    aceria = fields.Char(

    )
