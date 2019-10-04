# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models


class Name(models.AbstractModel):
    _name = "report.module.ot_report"

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env["report"]
        report = report_obj._get_report_from_name("mrp_ot.ot")
        docargs = {
            "doc_ids": self._ids,
            "mrp_ot": report.mrp_ot,
            "docs": self,
        }
        return report_obj.render("mrp_ot.ot", docargs)
