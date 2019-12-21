# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    operator_id = fields.Many2one(
        'hr.employee',
        help='Operador'
    )


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    operator_id = fields.Many2one(
        'hr.employee',
        help='Operador'
    )

    def button_start(self):
        """ Arranca la orden de trabajo
        """
        ret = super().button_start()

        timeline_obj = self.env['mrp.workcenter.productivity']
        timeline = timeline_obj.search([], limit=1, order='id desc')
        timeline.operator_id = self.operator_id

        return ret

    def button_lots(self):
        """ Pide los lotes de a uno cuando ya estan todos no pide mas.
            este metodo esta depreciado
        """

        # verificar que tiene cargado el lote final y cargarlo si no lo tiene
        if ((self.production_id.product_id.tracking != 'none') and
                not self.final_lot_id and self.move_raw_ids):

            wizard_id = self.env['lots.wizard'].create({
                'caption': 'Lote de salida para:'
            })
            wizard_id.product_id = self.product_id.id

            return {
                'context': {
                    'workorder': self.id,
                },
                'res_model': 'lots.wizard',
                'view_type': 'form',
                'res_id': wizard_id.id,
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'view_id': self.env.ref(
                    'mrp_easy_prod.mrp_lot_wizard_form').id,
            }

        for move_line in self.active_move_line_ids:
            if (move_line.product_id.tracking != 'none'
                and not move_line.lot_id):
                pass
