# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models
from pdf2image import convert_from_bytes


class OTCoverReport(models.AbstractModel):
    """ Abstract Model for report template.

        for `_name` model, please use:
        `report.` as prefix then add `module_name.report_name`.
    """
    _name = 'report.mrp_ot.ot_cover_report_template'

    @api.model
    def _get_child_vals(self, record, level, qty, uom):
        """Get bom.line values.

        :param record: mrp.bom.line record
        :param level: level of recursion
        :param qty: quantity of the product
        :param uom: unit of measurement of a product
        """
        child = {
            'pname': record.product_id.name_get()[0][1],
            'pcode': record.product_id.default_code,
            'puom': record.product_uom_id,
            'uname': record.product_uom_id.name,
            'level': level,
            'code': record.bom_id.code,
        }
        qty_per_bom = record.bom_id.product_qty
        if uom:
            if uom != record.bom_id.product_uom_id:
                qty = uom._compute_quantity(qty, record.bom_id.product_uom_id)
            child['pqty'] = (record.product_qty * qty) / qty_per_bom
        else:
            # for the first case, the ponderation is right
            child['pqty'] = (record.product_qty * qty)
        return child

    def get_children(self, records, level=0):
        result = []

        def _get_rec(records, level, qty=1.0, uom=False):
            for l in records:
                child = self._get_child_vals(l, level, qty, uom)
                result.append(child)
                if l.child_line_ids:
                    level += 1
                    _get_rec(l.child_line_ids, level, qty=child['pqty'], uom=child['puom'])
                    if level > 0:
                        level -= 1
            return result

        children = _get_rec(records, level)

        return children

    def to_image(self, image):
        """ Si el mimetype es pdf lo convierte a imagen
        """
        if image == 'application/pdf':
            return convert_from_bytes(image.datas)
        return image

    @api.multi
    def get_report_values(self, docids, data=None):

        docids = [data['bom_id']]

        domain = [('res_model', '=', 'mrp.bom'),
                  ('res_id', '=', data['bom_id'])]
        attachs = self.env['ir.attachment'].search(domain)

        bom = self.env['mrp.bom'].browse(docids)
        #routing = bom.routing_id
        #operations = routing.operation_ids
        #time = 0
        #for operation in operations:
        #    time += operation.time_cycle.manual


        return {
            'doc_ids': docids,
            'doc_model': 'mrp.bom',
            'docs': bom,
            'get_children': self.get_children,
            'data': data,
            'attachs': attachs,
            'to_image': self.to_image
        }
