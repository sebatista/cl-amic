# For copyright and license notices, see __manifest__.py file in module root

from odoo import models, fields, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    enable_ot = fields.Boolean(
        related='product_id.product_tmpl_id.enable_ot',
        help='campo tecnico para habilitar el boton de imprimir la ot'
    )

    ot = fields.Char(
        string='OT Amic'
    )

    def clean_ot_amic(self):
        """ limpiar la ot
        """
        return self.write({'ot': ''})

    def assign_ot_amic(self):
        """ Al marcar ordenes de produccion y darle al accion / Asignar OT Amic
            se trae una nueva secuencia y se marcan todas las ot con ella.
        """
        for order in self:
            if order.ot:
                raise UserError(_('La orden de trabajo %s ya tiene una OT '
                                'asignada' % order.name))
            if order.state == 'done':
                raise UserError(_('La orden de trabajo %s esta terminada, no '
                                  'se le puede asignar otra OT' % order.name))

        seq = self.env['ir.sequence'].search([('code', '=', 'ot.amic')])
        return self.write({'ot': seq.next_by_id()})

    def print_ot(self):
        """ Imprimir la OT, se lanza desde un boton.
        """
        self.ensure_one()

        data = {
            'bom_id': self.bom_id.id,
            'ot': self.ot,
            'date_create': fields.Date.today(),
            'date_planned_start': self.date_planned_start,
            'product_qty': self.product_qty,
            'product_name': self.product_id.display_name,
        }
        # todas las ordenes de trabajo
        mos = self.env['mrp.production'].search([('ot', '=', self.ot)],
                                                order='create_date desc')
        lines = []
        for mo in mos:
            # MO y producto
            lines.append('>> %s // %s <<' % (mo.name, mo.product_id.name))
            lines.append('-')

            for wo in mo.workorder_ids:
                lines.append('-%s-' % wo.name)
                for al in wo.active_move_line_ids:
                    lines.append('----materia prima -> %s Lote -> %s %s' % (al.product_id.name, al.lot_id.name if al.lot_id else '', al.lot_id.attributes if al.lot_id else '')) # noqa
                if wo.worked_lot:
                    lines.append('----lote de salida: %s %s' % (wo.worked_lot.name if wo.worked_lot else '', wo.worked_lot.attributes if wo.worked_lot else '')) # noqa
                for tl in wo.time_ids:
                    if tl.operator_id:
                        lines.append('----%s - %s / %s / %s / %s' % (tl.date_start,tl.date_end,tl.workcenter_id.name,tl.operator_id.name,tl.loss_id.name)) # noqa

#            for sm in self.env['stock.move'].search([('ot', '=', self.ot)]):
#                lines.append(sm.name)
#                for ml in sp.move_lines:
#                    lines.append(ml.product_id.name,ml.name)

        data['lines'] = lines

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
