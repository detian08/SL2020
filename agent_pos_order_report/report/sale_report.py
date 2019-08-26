# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "report.pos.order"

    agent_id = fields.Many2one('sale.agent', string='Agent')

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            , s.agent_id
            """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", s.agent_id"
        return group_by_str
