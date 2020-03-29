# For copyright and license notices, see __manifest__.py file in module root
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    """ Poner time_mode = 'manual'
        El calculo de la duracion standard de las operaciones debe ser manual
        Calcular piezas hora por primera vez.
    """
    wc = env['mrp.routing.workcenter'].search([])
    wc.write({'time_mode': 'manual'})

    for w in wc:
        w.pzs_hour = 60 / w.time_cycle_manual if w.time_cycle_manual else 0
