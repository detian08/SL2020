from odoo import models,fields,api,_

class SessionAgent(models.Model):

    _name = 'session.agents'

    session_id = fields.Many2one('pos.session',string='Session')
    agent_id =   fields.Many2one('sale.agent',string='Agent')
    commission_ids = fields.One2many('session.agent.lines','session_agent_id',string='Commission Lines')
    commision_paid = fields.Float('Commission Paid')

class SessionAgentLines(models.Model):

    _name = 'session.agent.lines'

    session_agent_id = fields.Many2one('session.agents',string='Session Agent')
    order_id = fields.Many2one('pos.order',string='Order')
    amount = fields.Float('Total Amount')
    total_commission = fields.Float('Total Commission')