from odoo import models,fields,api,_

class PosOrder(models.Model):

    _inherit = 'pos.order'

    margin = fields.Float('Margin',compute='_amount_margin')

    @api.depends('lines.price_subtotal')
    def _amount_margin(self):

        for data in self:
            cost = 0.0
            sale_price = 0.0
            for line in data.lines:
                cost += (line.product_id.standard_price * line.qty)
                sale_price += line.price_subtotal

            data.margin = sale_price - cost


class PosOrderLine(models.Model):

    _inherit = 'pos.order.line'

    product_cost = fields.Float(string='Cost',compute='get_cost',store=True)

    @api.depends('product_id')
    def get_cost(self):

        for data in self:
            data.product_cost = data.product_id.standard_price


