# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class MrpBomDocument(models.Model):
    """ Extension of ir.attachment only used in MRP BOM to handle archivage
        of OT documents.
    """
    _name = 'mrp.bom.document'
    _description = "OT Document"
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }
    _order = "sequence, id"

    ir_attachment_id = fields.Many2one(
        'ir.attachment',
        string='Adjuntos relacionados',
        required=True,
        ondelete='cascade'
    )
    active = fields.Boolean(
        'Activo',
        default=True
    )
    sequence = fields.Integer(
        default=10
    )
    product_code = fields.Char(
        compute="_compute_product_code",
        readonly=True,
        string='Codigo del Producto',
        store=True
    )

    @api.depends('res_id')
    def _compute_product_code(self):
        for rec in self:
            mrp_bom_obj = self.env['mrp.bom']
            mrp_bom = mrp_bom_obj.browse(rec.res_id)
            if mrp_bom:
                prod = mrp_bom.product_tmpl_id
                rec.product_code = prod.default_code
            else:
                rec.product_code = '??'
