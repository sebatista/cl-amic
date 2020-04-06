# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
import math

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    def action_cancel(self):
        """ Cancels production order, unfinished stock moves and set procurement
        orders in exception and Cancels production order which is Done."""
        for production in self:
            if production.state == 'done':
                move_obj = self.env['stock.move']
                pick_obj = self.env["stock.picking"]
                if production.move_finished_ids:
                    production.move_finished_ids.action_cancel()
                if production.move_raw_ids:
                    production.move_raw_ids.action_cancel()
                all_moves = (production.move_finished_ids | production.move_raw_ids)
                # cancel routing picking
                pickings = pick_obj.search([('origin', '=', production.name)])
                if pickings:
                    pick_obj.action_cancel([x.id for x in pickings])

            else:
                if any(workorder.state == 'progress' for workorder in self.mapped('workorder_ids')):
                    raise UserError(_('You can not cancel production order, a work order is still in progress.'))
                for production in self:
                    production.workorder_ids.filtered(lambda x: x.state != 'cancel').action_cancel()

                    finish_moves = production.move_finished_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                    raw_moves = production.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                    (finish_moves | raw_moves)._action_cancel()

        self.write({'state': 'cancel', 'is_locked': True})

        return True

    def action_set_to_comfirmed(self):
        """ Cancels production order, unfinished stock moves and set procurement
        orders in exception """
        if not len(self.ids):
            return False
        move_obj = self.env['stock.move']
        for (ids, name) in self.name_get():
            message = _("Manufacturing Order '%s' has been set in confirmed state.") % name
            self.message_post(body = message)
        for production in self:
            all_moves = (production.move_finished_ids | production.move_raw_ids)
            all_moves.sudo().action_draft()
            production.write({'state': 'confirmed'})
        return True


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_cancel(self):
        return super(StockMove, self)._action_cancel()

    def action_draft(self):
        for move in self:
            res = move.write({'state': 'waiting'})
            move._do_unreserve()
        return res

    def _do_unreserve(self):
        Quant = self.env['stock.quant']
        if any(move.state in ('done',) for move in self):
            mlx = self.mapped('move_line_ids')
            if self.raw_material_production_id:
                for ml in mlx:
                    Quant._update_available_quantity(ml.product_id, ml.location_id, ml.qty_done, lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id)
            if self.production_id:
                for ml in mlx:
                    Quant._update_available_quantity(ml.product_id, ml.location_dest_id, -ml.qty_done, lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id)
            self._recompute_state()
        if any(move.state in ('cancel') for move in self):
            raise UserError(_('Cannot unreserve a done move'))
        self.mapped('move_line_ids').unlink()
        return True

    def action_cancel(self):
        """ Cancels the moves and if all moves are cancelled it cancels the picking. """
        # TDE DUMB: why is cancel_procuremetn in ctx we do quite nothing ?? like not updating the move ??
        Quant = self.env['stock.quant']
        if any(move.state == 'done' for move in self):
            for move in self:
                move._do_unreserve()
                siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
                if move.propagate_cancel:
                    # only cancel the next move if all my siblings are also cancelled
                    if all(state == 'cancel' for state in siblings_states):
                        move.move_dest_ids._action_cancel()
                else:
                    if all(state in ('done', 'cancel') for state in siblings_states):
                        move.move_dest_ids.write({'procure_method': 'make_to_stock'})
                        move.move_dest_ids.write({'move_orig_ids': [(3, move.id, 0)]})
            self.write({'state': 'cancel', 'move_orig_ids': [(5, 0, 0)]})

        if any(move.state == 'done' for move in self):
            raise UserError(_('You cannot cancel a stock move that has been set to \'Done\'.'))
            for move in self:
                if move.state == 'cancel':
                    continue
                move._do_unreserve()
                siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
                if move.propagate_cancel:
                    # only cancel the next move if all my siblings are also cancelled
                    if all(state == 'cancel' for state in siblings_states):
                        move.move_dest_ids._action_cancel()
                else:
                    if all(state in ('done', 'cancel') for state in siblings_states):
                        move.move_dest_ids.write({'procure_method': 'make_to_stock'})
                        move.move_dest_ids.write({'move_orig_ids': [(3, move.id, 0)]})
            self.write({'state': 'cancel', 'move_orig_ids': [(5, 0, 0)]})
        return True

