# For copyright and license notices, see __manifest__.py file in module root

from odoo import models


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def button_start(self):
        """ Arranca la orden de trabajo.
            Esto no llama al super porque copie el metodo original
        """
        # volvemos al original porque no anduvo
        return super(MrpWorkorder, self).button_start()
