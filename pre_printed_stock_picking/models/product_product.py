# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    att_ot = fields.Boolean(
        related='product_tmpl_id.att_ot',
        readonly=True
    )
    att_tt = fields.Boolean(
        related='product_tmpl_id.att_tt',
        readonly=True
    )
    att_colada = fields.Boolean(
        related='product_tmpl_id.att_colada',
        readonly=True
    )
    att_paquete = fields.Boolean(
        related='product_tmpl_id.att_paquete',
        readonly=True
    )
    att_aceria = fields.Boolean(
        related='product_tmpl_id.att_aceria',
        readonly=True
    )
    att_remito_proveedor = fields.Boolean(
        related='product_tmpl_id.att_remito_proveedor',
        readonly=True
    )
    att_fecha_remito = fields.Boolean(
        related='product_tmpl_id.att_fecha_remito',
        readonly=True
    )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    att_ot = fields.Boolean(
        help='Muestra este atributo en remito al cliente',
        string='OT',
        default=False
    )
    att_tt = fields.Boolean(
        help='Muestra este atributo en remito al cliente',
        string='TT',
        default=False
    )
    att_colada = fields.Boolean(
        help='Muestra este atributo en remito al cliente',
        string='Colada',
        default=False
    )
    att_paquete = fields.Boolean(
        help='Muestra este atributo en remito al cliente',
        string='Paquete',
        default=False
    )
    att_aceria = fields.Boolean(
        help='Muestra este atributo en remito al cliente',
        string='Proveedor',
        default=False
    )
    att_remito_proveedor = fields.Boolean(
        help='Muestra este atributo en remito al cliente',
        string='Remito del proveedor',
        default=False
    )
    att_fecha_remito = fields.Boolean(
        help='Muestra este atributo en remito al cliente',
        string='Fecha del remito',
        default=False
    )
