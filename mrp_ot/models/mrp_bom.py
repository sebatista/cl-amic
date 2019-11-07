# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    def print_ot(self):
        """ Imprimir la OT, se lanza desde un boton
        """
        self.ensure_one()
        data = {'id': self.id}

        #                   `module_name`.`action_report_name'
        return self.env.ref('mrp_ot.action_ot_cover_report').report_action(
            self, data=data)

    def action_see_attachments(self):
        """ Mostrar y dejar agregar los attach en la bom
        """
        domain = [('res_model', '=', 'mrp.bom'),
                  ('res_id', '=', self.id)]
        attachment_view = self.env.ref(
            'mrp_ot.view_document_file_kanban_mrp_ot')
        return {
            'name': 'Adjuntos',
            'domain': domain,
            'res_model': 'mrp.bom.document',
            'type': 'ir.actions.act_window',
            'view_id': attachment_view.id,
            'views': [(attachment_view.id, 'kanban'), (False, 'form')],
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': '''<p class="oe_view_nocontent_create">
                        Haga click aqui para subir los documentos de la OT.
                    </p><p>
                        Use esta caracteristica para almacenar documentos
                        tipo PDF.
                    </p>''',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" %
                       ('mrp.bom', self.id)
        }


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    enable_ot = fields.Boolean(
        related='product_id.product_tmpl_id.enable_ot',
        help='campo tecnico para habilitar el boton de imprimir la ot'
    )

    def print_ot(self):
        """ Imprimir la OT, se lanza desde un boton.
        """
        self.ensure_one()

        data = {
            'bom_id': self.bom_id.id,
            'ot': self.name,
            'date_create': fields.Date.today(),
            'date_planned_start': self.date_planned_start,
            'product_qty': self.product_qty,
            'product_name': self.product_id.display_name,
        }

        # `module_name`.`action_report_name`
        return self.env.ref('mrp_ot.action_ot_cover_report').report_action(
            self, data=data)
