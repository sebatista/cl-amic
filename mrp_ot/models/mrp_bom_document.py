# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MrpBomDocument(models.Model):
    """ Extension of ir.attachment only used in MRP BOM to handle archivage
        of OT documents.
    """
    _name = 'mrp.bom.document'
    _description = "OT Document"
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }
    _order = "priority desc, id desc"

    ir_attachment_id = fields.Many2one(
        'ir.attachment',
        string='Adjuntos relacionados',
        required=True,
        ondelete='cascade'
    )
    active = fields.Boolean(
        'Active',
        default=True
    )
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Bajo'),
        ('2', 'Alto'),
        ('3', 'Muy alto')],
        string="Prioridad",
        help='Define el orden cuando se muestran los documentos de la OT.'
    )
