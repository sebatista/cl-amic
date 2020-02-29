# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MrpBom(models.Model):
    _inherit = "mrp.bom"

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

    def get_all_ids(self):
        ids = []

        def get_ids(bom):
            ids.append(bom.id)
            for mrp_bom_line in bom.bom_line_ids:
                if mrp_bom_line.child_bom_id:
                    bom = mrp_bom_line.child_bom_id
                    get_ids(bom)

        get_ids(self)

        return ids
