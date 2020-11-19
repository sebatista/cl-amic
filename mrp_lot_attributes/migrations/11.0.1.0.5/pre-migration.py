# For copyright and license notices, see __manifest__.py file in module root
from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):

    _logger.info('Recalculate invisible from stock.production.lot dropping the column')
    cr.execute("""
    ALTER TABLE stock_production_lot
    DROP COLUMN invisible;
    """)
