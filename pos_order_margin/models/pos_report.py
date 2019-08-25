from odoo import models,fields,api,tools

class PosOrderReport(models.Model):

    _inherit = "report.pos.order"

    margin = fields.Float(string='Total Margin')

    def _select(self):
        res = super(PosOrderReport, self)._select()
        print(res)
        line = res.find('s.pricelist_id,')
        output_line = res[:line] + 'SUM((l.qty * l.price_unit) - (l.qty * l.product_cost)) AS margin,' + res[line:]
        print(output_line)
        return output_line

    def _from(self):
        res = super(PosOrderReport, self)._from()
        print(res)
        return res


    def _group_by(self):
        res = super(PosOrderReport, self)._group_by()
        print(res)
        return res


    def _having(self):
        return super(PosOrderReport, self)._having()

    @api.model_cr
    def init(self):
        return super(PosOrderReport, self).init()
