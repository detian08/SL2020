from odoo import models,fields,api,_


class SaleAgent(models.Model):

    _inherit = 'sale.agent'

    percentage = fields.Float('Commission %')
    commission_amount = fields.Float('Commission Amount')
    commission_payment = fields.One2many('agent.commission.pay','agent_id',string='Payment')


class AgentCommissionPay(models.Model):

    _name = 'agent.commission.pay'

    agent_id = fields.Many2one('sale.agent',string='Agent')
    session_id = fields.Many2one('pos.session',string='Session')
    commission = fields.Float('Amount')
