from odoo import models,fields,api,_

class PosOrder(models.Model):

    _inherit = 'pos.order'

    commission = fields.Float('Agent Commission', compute='get_commission')

    @api.depends('amount_total', 'agent_id')
    def get_commission(self):
        for data in self:
            if data.agent_id:
                data.commission = (data.agent_id.percentage / 100) * data.amount_total
            else:
                data.commission = 0.0



class PosConfig(models.Model):

    _inherit = 'pos.config'

    commission_account = fields.Many2one('account.account', string="Commission Account")