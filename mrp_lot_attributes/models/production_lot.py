# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    colada = fields.Char(
        string='COLADA'
    )
    tt = fields.Char(
        string='TT',
        help='Tratamiento Termico'
    )
    paquete = fields.Char(
        string='PAQUETE'
    )
    ot = fields.Char(
        string='OT',
        help='Orden de Trabajo'
    )
    remito_proveedor = fields.Char(
        string='Remito Proveedor'
    )
    fecha_remito = fields.Date(
    )
    aceria = fields.Char(

    )

    def propagate_from(self, parent_lot):
        """ Mover los atributos de un lote a otro teniendo en cuenta que si
            ya existe no lo tengo que copiar.
        """
        def propagate_attr(source, dest):

            # no hay nada, escribo False en el atributo
            if not dest and not source:
                return False

            # hay algo en el lote origen y nada en el destino escribo origen
            if not dest and source:
                return source

            # hay algo en el lote destino y nada en el origen, no lo toco
            if dest and not source:
                return dest

            # hay cosas en los dos lotes, si en el atributo destino no esta el
            # atributo origen, si esta no toco el destino.
            if dest.find(source) == -1:
                return dest + ', ' + source
            else:
                return dest

        self.ot = propagate_attr(parent_lot.ot, self.ot)
        self.tt = propagate_attr(parent_lot.tt, self.tt)
        self.colada = propagate_attr(parent_lot.colada, self.colada)
        self.paquete = propagate_attr(parent_lot.paquete, self.paquete)
        self.remito_proveedor = propagate_attr(parent_lot.remito_proveedor,
                                               self.remito_proveedor)
        self.fecha_remito = propagate_attr(parent_lot.fecha_remito,
                                           self.fecha_remito)
        self.aceria = propagate_attr(parent_lot.aceria, self.aceria)
