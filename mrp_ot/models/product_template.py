# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    enable_ot = fields.Boolean(
        string="Habilitar OT",
        help="Si tilda este campo, se podra imprimir una OT para este producto"
    )

    produce_one = fields.Boolean(
        string='Producir de a uno',
        help='Solo se puede producir de a uno por vez'
    )
