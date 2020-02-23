# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp




class SaleOrderCost(models.Model):
    _inherit  = 'sale.order.line'

    is_cost_show_line = fields.Boolean('Display Margin', help='Indicates whether to show Margin and Cost or not.')

class SaleOrderMargin(models.Model):
    _inherit = "sale.order"
    is_cost_show = fields.Boolean('Display Margin', help='Indicates whether to show Margin and Cost or not.')





