# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from lxml import etree


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    colada = fields.Char(
    )
    tt = fields.Char(
    )
    paquete = fields.Char(
    )
