# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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
#   oe -Q mrp_easy_prod -c amic -d amic_test
#

from openerp.tests.common import HttpCase, TransactionCase


class SomethingCase(TransactionCase):
    def test_something(self):
        """First line of docstring appears in test logs.
        """
        self.assertEqual(1, 1)
