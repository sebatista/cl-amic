# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import datetime as dt


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    worked_lot = fields.Many2one(
        'stock.production.lot', 'Lote',
        help="lote que se trabajo en esta workorder, para poder buscar por OT"
    )

    """
    @api.multi
    def write(self, vals):
        import wdb;wdb.set_trace()
        super(MrpWorkorder,self).write(vals)

    @api.multi
    def create(self,write):
        import wdb;wdb.set_trace()
        super(MrpWorkorder,self).create(vals)
    """

    """
    @api.onchange('qty_producing')
    def _onchange_qty_producing_total(self):
        "" " Hay otro de estos que se llama _onchange_qty_producing y actualiza
            la cantidad actual a producir.

            Este actualiza la cantidad acumulada total y verifica que exista
            suficiente materia prima en el lote del cual se saca.
        "" "
        moves = self.move_raw_ids.filtered(
            lambda move: move.state not in ('done', 'cancel') and
                         move.product_id.tracking != 'none' and
                         move.product_id.id !=
                         self.production_id.product_id.id
        )
        for move in moves:
            move_lots = self.active_move_line_ids.filtered(
                lambda move_lot: move_lot.move_id == move
            )
            if not move_lots:
                continue
            rounding = move.product_uom.rounding
            accumulated_total = self.qty_produced + self.qty_producing
            new_qty = float_round(move.unit_factor * accumulated_total,
                                  precision_rounding=rounding)
            if move.product_id.tracking == 'lot':
                move_lots[0].accum_qty = new_qty
    """

    def validate_producing(self):
        """ TODO ver si se puede usar el qty_remaining
        """
        self.ensure_one()
        if self.qty_producing <= 0:
            raise UserError(_('Please set the quantity you are currently '
                              'producing. It should be different from zero.'))

        if self.qty_producing + self.qty_produced > self.qty_production:
            raise UserError(_('No se permite producir mas que la cantidad '
                              'planificada en la OT'))

        if self.qty_producing != 1 and self.product_id.produce_one:
            raise UserError(_('La cantidad a fabricar debe ser 1 para este '
                              'producto'))

    def validate_lots(self):
        if ((self.production_id.product_id.tracking != 'none') and
                not self.final_lot_id):
            raise UserError(_('You should provide a lot/serial number for '
                              'the final product'))

        if not self.date_start1 or not self.time_start:
            raise UserError(_('Por favor indique fecha y hora de comienzo de '
                              'la produccion.'))

        for line in self.active_move_line_ids:
            if line.product_id.tracking != 'none' and not line.lot_id:
                raise UserError(_('Por favor provea un lote para el '
                                  'componente'))

    def record_production(self):
        """ Crear un registro en mrp.workcenter.productivity
            Cargar el lote de salida con el peso de los lotes componentes
        """

        self.ensure_one()

        self.validate_producing()
        self.validate_lots()
        # self.validate_component_qty()

        if self.register_log:
            if not self.date_start1 or not self.time_start:
                raise UserError(_('Por favor indique fecha de la produccion.'))

            # aca le sumo 3 a las horas para pasar a utc a lo bruto.
            hr = dt.timedelta(hours=self.time_start)
            dy = dt.datetime.strptime(self.date_start1, '%Y-%m-%d')
            ds = (hr + dy + dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')

            hr = dt.timedelta(hours=self.time_end)
            dy = dt.datetime.strptime(self.date_start1, '%Y-%m-%d')
            de = (hr + dy + dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')

            if ds >= de:
                raise UserError(_('El fin de la produccion debe ser '
                                  'posterior al inicio.'))
        else:
            self.date_start = self.date_end = fields.Datetime.now()
            ds = False
            de = False

        # copio el lote de salida porque por alguna razon odoo luego lo borra
        self.worked_lot = self.final_lot_id

        # poner el lost tipe en productive
        loss = self.env['mrp.workcenter.productivity.loss']
        loss_prod = loss.search([('loss_type', '=', 'productive')], limit=1)

        # crear el registro de tiempo
        wcp = self.env['mrp.workcenter.productivity']
        wcp.create({
            'date_start': ds,
            'date_end': de,
            'operator_id': self.operator_id.id,
            'qty': self.qty_producing,
            'workcenter_id': self.workcenter_id.id,
            'loss_id': loss_prod.id,
            'workorder_id': self.id
        })

        # calcular el peso del producto fabricado, dejarlo en el lote
        weight = 0
        for line in self.active_move_line_ids:
            # si el producto de la linea tiene tracking
            if line.product_id.tracking != 'none':

                # Peso unitario del producto componente que esta en esta linea
                # Se obtiene del lote, que a su vez se calculo aqui o si el
                # producto tiene peso definido se toma del producto
                unit_lot_weight = line.lot_id.unit_lot_weight

                # cantidad a consumir del producto componente
                qty = line.qty_done

                # cantidad a producir del producto terminado
                prod = self.qty_producing

                # Calcular el peso unitario y acumular
                weight += unit_lot_weight * qty / prod

        # active_move_line_ids = False, no hacer nada, esto pasa cuando se
        # hace una operacion, en la primera se calcula el lote y en las demas
        # no se hace nada.
        # salvar el peso total del producto calculado en el lote
        if self.active_move_line_ids:
            self.worked_lot.produced_lot_weight = weight

        # mover atributos
        for move_line in self.active_move_line_ids:
            # si el producto tiene trazabilidad propagar atributos
            if move_line.product_id.tracking != 'none':
                self.final_lot_id.propagate_from(move_line.lot_id)

        super(MrpWorkorder, self).record_production()

        # poner el qty_producing en cero para obligar al operador a cargar el
        # dato sino, el sistema pone el total que falta. Si estamos en done no
        # se puede escribir porque odoo chequea que no le cambien una orden
        # terminada.
        if self.state != 'done':
            self.qty_producing = 0

    def _assign_default_final_lot_id(self):
        """ FIX Si el operador ejecuta la ultima WO de la MO y la termina
            poniendona en el estado 'done', cuando en la anterior se termina
            odoo intentara poner el default_final_lot y fallara miserablemente
            con la excepcion "No puede modificar la orden de trabajo
            terminada."

            Para arreglar eso sobreescribimos esta funcion y evitamos poner un
            lote si esta en estado done.
        """
        if self.state != 'done':
            spl_obj = self.env['stock.production.lot']
            domain = [('use_next_on_work_order_id', '=', self.id)]
            self.final_lot_id = spl_obj.search(domain,
                                               order='create_date, id',
                                               limit=1)

        #    def validate_component_qty(self):
        #        "" "
        #            Obtener la lista de materiales para el producto a producir
        #            Ver que cantidad de materia prima se requiere
        #            Verificar que en los lotes de los productos a consumir
        #            tenemos las
        #            cantidades requeridas.

        #            Esto se hace solo en la operacion inicial que es donde se
        #            consumen las manterias primas, en el resto de las
        #            operaciones, el active_move_line_ids esta en False.
        #        "" "

        #        self.ensure_one()
        #        for mp in self.active_move_line_ids:
        #            if mp.product_lot_qty < mp.accum_qty:
        #                raise UserError(_('No te alcanza!!\n'
        #                                'Intentas consumir %s del lote %s '
        #                                'que solo tiene %s' % (mp.accum_qty,
        #                                              mp.lot_id.name,
        #                                              mp.product_lot_qty)))

    def button_start(self):
        """ Al arrancar la produccion hacemos el movimiento de los datos de
            lotes y ademas si es el primer lote de una ot le ponemos la OT
        """
        self.ensure_one()

        self.validate_producing()
        self.validate_lots()

        # si el lote tiene una ot y si es distinta aviso.
        # TODO esto deberia chequear que sea el mismo producto, si es un
        # producto distinto se permite cambiar la OT
        #        if self.final_lot_id.ot and self.final_lot_id.ot != self.ot:
        #            raise UserError(_('Cuidado !!\n'
        #                              'El lote destino pertenece a la %s lo '
        #                             'cual no parece correcto ya que estamos '
        #                              'trabajando la %s.'
        #                              ' ') % (self.final_lot_id.ot, self.ot))

        # le pongo la ot al lote final
        self.final_lot_id.ot = self.ot

        super().button_start()
