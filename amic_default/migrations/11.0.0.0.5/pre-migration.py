# For copyright and license notices, see __manifest__.py file in module root
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    """ Poner time_mode = 'manual'
        El calculo de la duracion standdard de las operaciones debe ser manual
    """
    wc = env['mrp.routing.workcenter'].search([])
    wc.write({'time_mode': 'manual'})
