# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class StockPrintStockVoucher(models.TransientModel):
    _inherit = 'stock.print_stock_voucher'

    next_voucher_number_manual = fields.Integer(
        string='Número del siguiente comprobante'
    )

    @api.onchange('book_id')
    def _onchange_book_id(self):
        _ = self.book_id.sequence_id.number_next_actual
        self.next_voucher_number_manual = _

    @api.multi
    def do_print_and_assign(self):
        self.book_id.sequence_id.number_next = self.next_voucher_number_manual
        self.assign_numbers()
        return {
            'actions': [
                {'type': 'ir.actions.act_window_close'},
                self.do_print_voucher(),
            ],
            'type': 'ir.actions.act_multi',
        }
