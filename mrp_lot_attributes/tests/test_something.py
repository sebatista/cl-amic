# Copyright 2019  - jeo Software

#   Para correr los tests
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos para testing como sigue:
#   - Nombre sugerido: [nombre cliente]_test
#   - Debe ser creada con Load Demostration Data chequeado
#   - Usuario admin y password admin
#   - El modulo que se quiere testear debe estar instalado.
#
#   Arrancar el test con:
#
#   oe -Q mrp_lot_attributes -c amic -d amic_test
#

from odoo.tests.common import TransactionCase


class SomethingCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(SomethingCase, self).setUp(*args, **kwargs)

        # self.env['ir.config_parameter'].sudo().set_param(
        # 'stock.group_stock_production_lot', True)
        # self.env['ir.config_parameter'].sudo().get_param(
        # 'stock.group_stock_production_lot')

        # cr = self.env['res.config.settings']
        # cr = cr.create({})
        # cr.default_get()

        # cr.group_stock_production_lot = True
        # cr.execute()

    def test_01_something(self):
        """TEST 01 docstring appears in test logs.
        """

        self.assertEqual(1, 1)
