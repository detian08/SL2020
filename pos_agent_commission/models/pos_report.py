from odoo import models,fields,api,tools

class PosOrderReport(models.Model):

    _inherit = "report.pos.order"

    total_commission = fields.Float(string='Total Commission')

    def _select(self):
        res = super(PosOrderReport, self)._select()
        line = res.find('p.product_tmpl_id,')
        output_line = res[:line] + 'SUM((l.qty * l.price_unit) * (ag.percentage) / 100) AS total_commission,' + res[line:]
        print(output_line)
        return output_line

    def _from(self):
        res = super(PosOrderReport, self)._from()
        line = res.find('LEFT JOIN pos_session ps ON (s.session_id=ps.id)')
        output_line = res[:line] + 'LEFT JOIN sale_agent ag ON (s.agent_id=ag.id)' + res[line:]
        print(output_line)
        return output_line


    def _group_by(self):
        return super(PosOrderReport, self)._group_by()
    #
    def _having(self):
        return super(PosOrderReport, self)._having()

    @api.model_cr
    def init(self):
        return super(PosOrderReport, self).init()