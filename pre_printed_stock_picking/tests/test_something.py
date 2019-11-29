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
#   oe -Q pre_printed_stock_picking -c amic -d amic_test
#

from odoo.tests.common import TransactionCase


class SomethingCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(SomethingCase, self).setUp(*args, **kwargs)

    def tearDown(self, *args, **kwargs):

        return super(SomethingCase, self).tearDown(*args, **kwargs)

    def test_01_something(self):
        """TEST 01 docstring appears in test logs.
        """
        self.assertEqual(1, 1)
