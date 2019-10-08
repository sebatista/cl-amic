# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models


class OTCoverReport(models.AbstractModel):
    """ Abstract Model for report template.

        for `_name` model, please use:
        `report.` as prefix then add `module_name.report_name`.
    """
    _name = 'report.mrp_ot.ot_cover_report_template'

    @api.multi
    def get_report_values(self, docids, data=None):
        
        #import wdb;wdb.set_trace()
        docs = []
        mrp_bom_obj = self.env['mrp.bom']
        
        docs.append({
            'campo1': '11',
            'campo2': '22',
            'campo3': '33'
        })
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'docs': docs
        }
