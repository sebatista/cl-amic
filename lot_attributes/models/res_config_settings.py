# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root


from openerp import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    lot_attrib_name_01 = fields.Char()
    lot_attrib_name_02 = fields.Char()
    lot_attrib_name_03 = fields.Char()
    lot_attrib_name_04 = fields.Char()
    lot_attrib_name_05 = fields.Char()
    lot_attrib_name_06 = fields.Char()
    lot_attrib_name_07 = fields.Char()
    lot_attrib_name_08 = fields.Char()
    lot_attrib_name_09 = fields.Char()
    lot_attrib_name_10 = fields.Char()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        name_01 = params.get_param('stock.lot_attrib_name_01', default=False)
        name_02 = params.get_param('stock.lot_attrib_name_02', default=False)
        name_03 = params.get_param('stock.lot_attrib_name_03', default=False)
        name_04 = params.get_param('stock.lot_attrib_name_04', default=False)
        name_05 = params.get_param('stock.lot_attrib_name_05', default=False)
        name_06 = params.get_param('stock.lot_attrib_name_06', default=False)
        name_07 = params.get_param('stock.lot_attrib_name_07', default=False)
        name_08 = params.get_param('stock.lot_attrib_name_08', default=False)
        name_09 = params.get_param('stock.lot_attrib_name_09', default=False)
        name_10 = params.get_param('stock.lot_attrib_name_10', default=False)
        res.update(
            lot_attrib_name_01=name_01,
            lot_attrib_name_02=name_02,
            lot_attrib_name_03=name_03,
            lot_attrib_name_04=name_04,
            lot_attrib_name_05=name_05,
            lot_attrib_name_06=name_06,
            lot_attrib_name_07=name_07,
            lot_attrib_name_08=name_08,
            lot_attrib_name_09=name_09,
            lot_attrib_name_10=name_10,
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('stock.lot_attrib_name_01', self.lot_attrib_name_01)
        params.set_param('stock.lot_attrib_name_02', self.lot_attrib_name_02)
        params.set_param('stock.lot_attrib_name_03', self.lot_attrib_name_03)
        params.set_param('stock.lot_attrib_name_04', self.lot_attrib_name_04)
        params.set_param('stock.lot_attrib_name_05', self.lot_attrib_name_05)
        params.set_param('stock.lot_attrib_name_06', self.lot_attrib_name_06)
        params.set_param('stock.lot_attrib_name_07', self.lot_attrib_name_07)
        params.set_param('stock.lot_attrib_name_08', self.lot_attrib_name_08)
        params.set_param('stock.lot_attrib_name_09', self.lot_attrib_name_09)
        params.set_param('stock.lot_attrib_name_10', self.lot_attrib_name_10)
