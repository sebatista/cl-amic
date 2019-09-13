# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from lxml import etree


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    attribute_01 = fields.Char(
    )
    attribute_02 = fields.Char(
    )
    attribute_03 = fields.Char(
    )
    attribute_04 = fields.Char(
    )
    attribute_05 = fields.Char(
    )
    attribute_06 = fields.Char(
    )
    attribute_07 = fields.Char(
    )
    attribute_08 = fields.Char(
    )
    attribute_09 = fields.Char(
    )
    attribute_10 = fields.Char(
    )

    @api.model
    def fields_view_get(self, view_id=None, view_type='tree', context=None,
        toolbar=False, submenu=False):

        result = super(ProductionLot, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)

        if view_type == 'form' and view_id == 649:
            params = self.env['ir.config_parameter'].sudo()
            att01 = params.get_param('stock.lot_attrib_name_01', ' ')
            att02 = params.get_param('stock.lot_attrib_name_02', ' ')
            att03 = params.get_param('stock.lot_attrib_name_03', ' ')
            att04 = params.get_param('stock.lot_attrib_name_04', ' ')
            att05 = params.get_param('stock.lot_attrib_name_05', ' ')
            att06 = params.get_param('stock.lot_attrib_name_06', ' ')
            att07 = params.get_param('stock.lot_attrib_name_07', ' ')
            att08 = params.get_param('stock.lot_attrib_name_08', ' ')
            att09 = params.get_param('stock.lot_attrib_name_09', ' ')
            att10 = params.get_param('stock.lot_attrib_name_10', ' ')
            doc = etree.XML(result['arch'])

            for node in doc.xpath("//field[@name='attribute_01']"):
                node.set('string', att01)
            for node in doc.xpath("//field[@name='attribute_02']"):
                node.set('string', att02)
            for node in doc.xpath("//field[@name='attribute_03']"):
                node.set('string', att03)
            for node in doc.xpath("//field[@name='attribute_04']"):
                node.set('string', att04)
            for node in doc.xpath("//field[@name='attribute_05']"):
                node.set('string', att05)
            for node in doc.xpath("//field[@name='attribute_06']"):
                node.set('string', att06)
            for node in doc.xpath("//field[@name='attribute_07']"):
                node.set('string', att07)
            for node in doc.xpath("//field[@name='attribute_08']"):
                node.set('string', att08)
            for node in doc.xpath("//field[@name='attribute_09']"):
                node.set('string', att09)
            for node in doc.xpath("//field[@name='attribute_10']"):
                node.set('string', att10)

            result['arch'] = etree.tostring(doc)
        return result
