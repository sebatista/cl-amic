# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


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


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    enable_ot = fields.Boolean(
        related='product_id.product_tmpl_id.enable_ot',
        help='campo tecnico para habilitar el boton de imprimir la ot'
    )

    ot = fields.Char(
        compute='compute_ot',
        readonly=True,
        store=True,
        string='Orden de Trabajo'
    )

    @api.depends('workorder_ids')
    def compute_ot(self):
        for rec in self:
            for wo in rec.workorder_ids:
                if wo.ot:
                    rec.ot = wo.ot
                    return
        rec.ot = False

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

        # lista de materiales
        # self.bom_id

        # ruta
        # self.routing_id
        # self.workorder_count

        # ordenes de trabajo
        # self.workorder_ids.time_ids.date_start
        # self.workorder_ids.time_ids.date_end
        # lote final
        # self.workorder_ids.final_lot_id

        # productos a consumir
        # self.workorder_ids.move_raw_ids

        # lotes de los productos a consumir.
        # self.workorder_ids.move_raw_ids.active_move_line_ids.lot_name

        # `module_name`.`action_report_name`
        return self.env.ref('mrp_ot.action_ot_cover_report').report_action(
            self, data=data)
