from odoo import models,fields,api,_
from odoo.exceptions import UserError, ValidationError

class PayCommissionWizard(models.TransientModel):

    _name = 'pay.commission.wizard'

    session_id = fields.Many2one('pos.session',string='Session')
    pay_journal = fields.Many2one('account.journal',string='Payment Journal',required=True)
    agent = fields.Many2one('sale.agent',string='Agent')
    amount = fields.Float('Payable Amount',compute='get_amount')

    commission_line_ids = fields.One2many('pay.commission.line','commission_id')


    @api.onchange('pay_journal')
    def _default_journals(self):
        session = self.env['pos.session'].browse(self._context.get('active_id'))
        journals = []
        res = {}
        for journal in session.config_id.journal_ids:
            print(journal)
            if journal.type == 'cash':
                journals.append(journal.id)

        if journals:
            res['domain'] = {'pay_journal': [('id', 'in', journals)]}
        else:
            res['domain'] = {'pay_journal': [('id', '=', False)]}

        return res

    @api.depends('commission_line_ids.commissin_to_pay')
    def get_amount(self):
        for data in self:
            amount= 0.0
            for line in data.commission_line_ids:
                amount += line.commissin_to_pay

            data.amount = amount


    @api.multi
    def validate_payment(self):

        if self.amount <= 0:
            raise UserError(_("The Amount must be greater than zero"))


        agents = self.commission_line_ids.mapped('agent_name')
        print(self.commission_line_ids)
        for agent in self.commission_line_ids:


            date_tz_user = fields.Datetime.context_timestamp(self, fields.Datetime.from_string(fields.Datetime.now()))
            date_tz_user = fields.Date.to_string(date_tz_user)
            move = self.env['account.move'].sudo().create({'ref': self.session_id.name, 'journal_id': self.pay_journal.id, 'date': date_tz_user})
            print(agent.agent_name)
            lines = []
            data_c = {
                'name': _("Agent Commission:%s" % self.session_id.name),  # order.name,
                'account_id': self.pay_journal.default_credit_account_id.id,
                'credit': float(agent.commissin_to_pay),
                'debit': 0.0,
                'partner_id': agent.agent_name.partner_id.id,
                'analytic_account_id': self.session_id.config_id.analytic_account_id.id,
                'move_id': move.id
            }
            data_d = {
                'name': _("Agent Commission:%s" % self.session_id.name),  # order.name,
                'account_id': agent.agent_name.partner_id.property_account_payable_id.id,
                'credit': 0.0,
                'debit': float(agent.commissin_to_pay),
                'partner_id': agent.agent_name.partner_id.id,
                'analytic_account_id': self.session_id.config_id.analytic_account_id.id,
                'move_id': move.id
            }

            lines.append((0, 0, data_c), )
            lines.append((0, 0, data_d), )
            move.write({'line_ids': lines})
            move.sudo().post()
            agent.agent_name.commission_amount -= float(self.amount)
            agent_line = self.session_id.session_commission_ids.filtered(lambda a: a.agent_id.id == agent.agent_name.id)
            to_pay = self.env['agent.commission.pay'].search([('agent_id','=',agent.agent_name.id),('session_id','=',self.session_id.id)])
            to_pay.commission -= float(agent.commissin_to_pay)
            agent_line.commision_paid += float(agent.commissin_to_pay)


class PayCommissionLine(models.TransientModel):
    _name = 'pay.commission.line'

    commission_id= fields.Many2one('pay.commission.wizard')
    agent_name=fields.Many2one('sale.agent')
    total_commission=fields.Float('Total Commision')
    commissin_to_pay = fields.Float('Commission To Pay')

    @api.onchange('commissin_to_pay')
    def onchange_commissin_to_pay(self):
        if self.commissin_to_pay > self.total_commission:
            raise UserError(_('The amount should be less than total amount'))