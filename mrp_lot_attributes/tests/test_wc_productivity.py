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
from odoo.addons.mrp.tests.common import TestMrpCommon


class WorkcenterProductivity(TestMrpCommon):
    def setUp(self, *args, **kwargs):
        super(WorkcenterProductivity, self).setUp(*args, **kwargs)
        self.mo, _, _, _, _ = self.generate_mo()

    def test_01(self):
        """TEST 01 crear parte de horas
        """
        self.mo.button_plan()
        vals = {}
        vals['name'] = 'MO/0001'
        vals['workcenter_id'] = self.workcenter_1.id
        vals['production_id'] = self.mo.id
        wo = self.env['mrp.workorder'].create(vals)

        vals = {
            'workcenter_id': self.workcenter_1.id,
            'date': '2020-02-01',
            'time_start': 8,
            'time_end': 15,
            'operator_id': self.env['hr.employee'].search([], limit=1).id,
            'loss_id': self.env.ref('mrp.block_reason0').id,
            'qty': 20
        }
        wo_1 = wo.time_ids.create(vals)

        self.assertEqual(wo_1.qty, 20)
        self.assertEqual(wo_1.date_start, '2020-02-01 08:00:00')
        self.assertEqual(wo_1.date_end, '2020-02-01 15:00:00')

        wo_1.write({'time_end': 12.5})
        self.assertEqual(wo_1.date_end, '2020-02-01 12:30:00')
