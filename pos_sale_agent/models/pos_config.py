# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _, SUPERUSER_ID


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
        ('agent', _('Agent'))
    ])


class PosOrdrer(models.Model):
    _inherit = 'pos.order'

    agent_id = fields.Many2one(
        'sale.agent',
        'Agent',
    )

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrdrer, self)._order_fields(ui_order)
        res['agent_id'] = ui_order['agent_id']
        return res