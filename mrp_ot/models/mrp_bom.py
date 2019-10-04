# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields
from odoo.exceptions import Warning


class ModelName(models.Model):
    _inherit = "mrp.bom"

    enable_ot = fields.Boolean(
        string="Habilitar OT",
        help="Si tilda este campo, se podra imprimir una OT para este producto"
    )

    def print_ot(self):
        """ Imprimir la OT
        """

        raise Warning('Todavia no esta implementada la impresion')
