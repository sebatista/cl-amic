# For copyright and license notices, see __manifest__.py file in module root

import math
from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    enable_ot = fields.Boolean(
        related='product_id.product_tmpl_id.enable_ot',
        help='campo tecnico para habilitar el boton de imprimir la ot'
    )
    ot = fields.Char(
        string='OT Amic'
    )

    @api.model
    def create(self, vals):
        """ Cuando creamos una MO con los productos tildados make to order,
            se crean al mismo tiempo las MO dependientes.
            No se puede usar en onchange asi que lo parchamos aqui
            Se le fuerza el location_dest_id y location_src_id a lo que dice
            en el routing.
        """
        bom_id = self.env['mrp.bom'].search([('id', '=', vals.get('bom_id'))])
        if bom_id and bom_id.routing_id:
            routing_id = bom_id.routing_id
            vals['location_dest_id'] = routing_id.location_id.id
            vals['location_src_id'] = routing_id.location_id.id
        return super(MrpProduction, self).create(vals)

    def clean_ot_amic(self):
        """ limpiar la ot
        """
        return self.write({'ot': False})

    def assign_ot_amic(self):
        """ Al marcar ordenes de produccion y darle al accion / Asignar OT Amic
            se trae una nueva secuencia y se marcan todas las ot con ella.

            Si algunas estan en blanco y otras tienen ot iguales, entonces no
            se trae una nueva secuencia sino que se marcan las que estan en
            blanco con la secuencia comun
        """
        # lista con todas las ot que han sido marcadas (incluso blancos)
        ots = self.mapped('ot')

        # removemos las que son iguales
        ots = set(ots)

        # esperamos que haya 2 y que una sea vacia
        # La vacia lee como False, antes estaba como '' porque en un momento venia asi
        # no se porque.
        if len(ots) == 2 and False in ots:
            # elimino la ot vacia
            ots.discard(False)
            # me queda la ot que no es vacia
            _ot = ots.pop()
            return self.write({'ot': _ot})

        # no quedaron 2 o una no es False entonces sigo como antes
        for order in self:
            if order.ot:
                raise UserError(_('La orden de trabajo %s ya tiene una OT '
                                  'asignada') % order.name)
            if order.state == 'done':
                raise UserError(_('La orden de trabajo %s esta terminada, no '
                                  'se le puede asignar otra OT') % order.name)

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
            'final_product_name': self.routing_id.name,
            'final_product_uom': self.product_uom_id.name
        }

        # NO QUEREMOS DATOS SOLO EL ENCABEZADO
        # todas las ordenes de trabajo
        # mos = self.env['mrp.production'].search([('ot', '=', self.ot)],
        #                                         order='create_date desc')
        # lines = []
        # for _mo in mos:
        #     # MO y producto
        #     lines.append('>> %s // %s <<' % (_mo.name, _mo.product_id.name))
        #     lines.append('-')

        #     for _wo in _mo.workorder_ids:
        #         lines.append('-%s-' % _wo.name)
        #         for _al in _wo.active_move_line_ids:
        #             lines.append('----materia prima -> %s Lote -> %s %s' % (
        #                 _al.product_id.name,produc        #                 _al.lot_id.name if _al.lot_id else '',
        #                 _al.lot_id.get_attributes() if _al.lot_id else ''))
        #         if _wo.worked_lot:
        #             lines.append('----lote de salida: %s %s' % (
        #                 _wo.worked_lot.name if _wo.worked_lot else '',
        #                 _wo.worked_lot.get_attributes() if _wo.worked_lot else ''))  # noqa
        #         for _tl in _wo.time_ids:
        #             if _tl.operator_id:
        #                 lines.append('----%s - %s / %s / %s / %s' % (
        #                     _tl.date_start, _tl.date_end,
        #                     _tl.workcenter_id.name, _tl.operator_id.name,
        #                     _tl.loss_id.name))

        # for sm in self.env['stock.move'].search([('ot', '=', self.ot)]):
        #     lines.append(sm.name)
        #     for ml in sp.move_lines:
        #       lines.append(ml.product_id.name,ml.name)

        # data['lines'] = lines

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
        data['raw_data'] = []
        for wo in self.workorder_ids:
            for raw_prod in wo.move_raw_ids:
                data['raw_data'].append({
                    'product_name': raw_prod.product_id.name,
                    'product_qty': raw_prod.product_uom_qty,
                    'product_uom': raw_prod.product_uom.name
                })

        # lotes de los productos a consumir.
        # self.workorder_ids.move_raw_ids.active_move_line_ids.lot_name

        # `module_name`.`action_report_name`
        return self.env.ref('mrp_ot.action_ot_cover_report').report_action(
            self, data=data)

    def _workorders_create(self, bom, bom_data):
        """
        :param bom: in case of recursive boms: we could create work orders for
                    child BoMs

            Se copio este metodo para sobreescribirlo y poner qty_producing=0
        """
        workorders = self.env['mrp.workorder']
        bom_qty = bom_data['qty']

        # Initial qty producing
        if self.product_id.tracking == 'serial':
            quantity = 1.0
        else:
            quantity = self.product_qty - sum(
                self.move_finished_ids.mapped('quantity_done'))
            quantity = quantity if (quantity > 0) else 0

        for operation in bom.routing_id.operation_ids:
            # create workorder
            cycle_number = math.ceil(
                bom_qty / operation.workcenter_id.capacity)  # TODO: float_round UP # noqa
            duration_expected = (operation.workcenter_id.time_start +
                                 operation.workcenter_id.time_stop +
                                 cycle_number * operation.time_cycle * 100.0 / operation.workcenter_id.time_efficiency)  # noqa
            workorder = workorders.create({
                'name': operation.name,
                'production_id': self.id,
                'workcenter_id': operation.workcenter_id.id,
                'operation_id': operation.id,
                'duration_expected': duration_expected,
                'state': len(workorders) == 0 and 'ready' or 'pending',
                'qty_producing': 0,  # antes aca decia quantity
                'capacity': operation.workcenter_id.capacity,
            })
            if workorders:
                workorders[-1].next_work_order_id = workorder.id
            workorders += workorder

            # assign moves; last operation receive all unassigned moves
            # (which case ?)
            moves_raw = self.move_raw_ids.filtered(
                lambda move: move.operation_id == operation)
            if len(workorders) == len(bom.routing_id.operation_ids):
                moves_raw |= self.move_raw_ids.filtered(
                    lambda move: not move.operation_id)
            # TODO: code does nothing, unless maybe by_products?
            moves_finished = self.move_finished_ids.filtered(
                lambda move: move.operation_id == operation)
            moves_raw.mapped('move_line_ids').write(
                {'workorder_id': workorder.id})
            (moves_finished + moves_raw).write({'workorder_id': workorder.id})

            workorder._generate_lot_ids()
        return workorders
