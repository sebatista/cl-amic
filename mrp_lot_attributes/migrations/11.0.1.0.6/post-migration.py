# For copyright and license notices, see __manifest__.py file in module root
from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    _logger.info('Fill lot_char from lot_id in model stock.move.line')

    for lot in env['stock.move.line'].search([]):
        if lot.lot_id:
            lot.lot_char = lot.lot_id.name
