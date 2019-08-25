from odoo import models,fields,api,_
from odoo.exceptions import UserError, ValidationError


class PosSession(models.Model):

    _inherit = 'pos.session'

    session_commission_ids = fields.One2many('session.agents','session_id',string='Session Agent Ids')


    @api.multi
    def print_quotation(self):
        return self.env.ref('pos_agent_commission.action_report_sale_agent').report_action(self)


    def _confirm_orders(self):
        for session in self:
            company_id = session.config_id.journal_id.company_id.id
            orders = session.order_ids.filtered(lambda order: order.state == 'paid')
            journal_id = self.env['ir.config_parameter'].sudo().get_param(
                'pos.closing.journal_id_%s' % company_id, default=session.config_id.journal_id.id)
            if not journal_id:
                raise UserError(_("You have to set a Sale Journal for the POS:%s") % (session.config_id.name,))

            move = self.env['pos.order'].with_context(force_company=company_id)._create_account_move(session.start_at, session.name, int(journal_id), company_id)
            orders.with_context(force_company=company_id)._create_account_move_line(session, move)

            agents = session.order_ids.mapped('agent_id')
            for agent in agents:
                lines =[]
                amount = 0.0
                orders = session.order_ids.filtered(lambda o: o.agent_id.id == agent.id)
                for order in orders:
                    amount += order.commission

                data_c = {
                    'name': _("Agent Commission:%s" % session.name),  # order.name,
                    'account_id': session.config_id.commission_account.id,
                    'credit': 0.0,
                    'debit': float(amount) or 0.0,
                    'partner_id': agent.partner_id.id,
                    'analytic_account_id': session.config_id.analytic_account_id.id,
                    'move_id': move.id
                }


                data_d = {
                    'name': _("Agent Commission:%s" % session.name),  # order.name,
                    'account_id': agent.partner_id.property_account_payable_id.id,
                    'credit': float(amount) or 0.0,
                    'debit': 0.0,
                    'partner_id': agent.partner_id.id,
                    'analytic_account_id': session.config_id.analytic_account_id.id,
                    'move_id': move.id
                }

                lines.append((0, 0, data_c), )
                lines.append((0, 0, data_d), )
                move.write({'line_ids': lines})
                agent.commission_amount += float(amount)
                self.env['agent.commission.pay'].create(
                    {'agent_id': agent.id, 'session_id': session.id, 'commission': float(amount)})

            # commission_vals = self.get_commission_vals(orders)
            # if commission_vals:
            #     print(commission_vals)
            #     for key, val in commission_vals.items():
            #         partner_id = int(key)
            #         lines = []
            #         print("account",session.config_id.commission_account.id)
            #         data_c = {
            #             'name': _("Agent Commission:%s"%session.name),  # order.name,
            #             'account_id': session.config_id.commission_account.id,
            #             'credit': 0.0,
            #             'debit': float(val) or 0.0,
            #             'partner_id': self.env['res.partner'].browse(int(key)).id,
            #             'analytic_account_id': session.config_id.analytic_account_id.id,
            #             'move_id':move.id
            #         }
            #         print("partner+++++", self.env['res.partner'].browse(int(key)))
            #         print("account+++++", self.env['res.partner'].browse(int(key)).property_account_payable_id.id)
            #         data_d = {
            #             'name': _("Agent Commission:%s" % session.name),  # order.name,
            #             'account_id':self.env['res.partner'].browse(int(key)).property_account_payable_id.id ,
            #             'credit': float(val) or 0.0,
            #             'debit': 0.0,
            #             'partner_id': self.env['res.partner'].browse(int(key)).id,
            #             'analytic_account_id': session.config_id.analytic_account_id.id,
            #             'move_id': move.id
            #         }
            #
            #         lines.append((0, 0, data_c),)
            #         lines.append((0, 0, data_d),)
            #         move.write({'line_ids': lines})
            #         agent = self.env['sale.agent'].search([('partner_id','=',partner_id)],limit=1)
            #         agent.commission_amount += float(val)
            #         self.env['agent.commission.pay'].create({'agent_id':agent.id,'session_id':session.id,'commission':float(val)})



            for order in session.order_ids.filtered(lambda o: o.state not in ['done', 'invoiced']):
                if order.state not in ('paid'):
                    raise UserError(
                        _("You cannot confirm all orders of this session, because they have not the 'paid' status.\n"
                          "{reference} is in state {state}, total amount: {total}, paid: {paid}").format(
                            reference=order.pos_reference or order.name,
                            state=order.state,
                            total=order.amount_total,
                            paid=order.amount_paid,
                        ))
                order.action_pos_order_done()
            orders_to_reconcile = session.order_ids._filtered_for_reconciliation()
            orders_to_reconcile.sudo()._reconcile_payments()

    @api.multi
    def action_pos_session_closing_control(self):
        self._check_pos_session_balance()
        for session in self:
            session.write({'state': 'closing_control', 'stop_at': fields.Datetime.now()})
            if not session.config_id.cash_control:
                session.action_pos_session_close()

            agents = session.order_ids.mapped('agent_id')
            print(agents)
            for agent in agents:
                session_agent = self.env['session.agents'].create({'session_id':session.id,'agent_id':agent.id})
                print(session_agent)
                orders = session.order_ids.filtered(lambda order: order.agent_id.id == agent.id)
                for order in orders:
                    self.env['session.agent.lines'].create({'session_agent_id':session_agent.id,'order_id':order.id,'amount':order.amount_total,'total_commission':order.commission})



    def get_commission_vals(self,orders):

        result = {}
        for order in orders:
            if order.agent_id:
                if order.agent_id.partner_id in result:
                    result[order.agent_id.partner_id.id] += order.commission

                else:
                    result[order.agent_id.partner_id.id] = order.commission


        return result


    @api.multi
    def pay_commission(self):
        # edited by hanish
        # agent_commission = {}
        list=[]

        agents = self.order_ids.mapped('agent_id')
        for agent in agents:
            amount=0.0
            orders = self.order_ids.filtered(lambda order: order.agent_id.id == agent.id)
            for order in orders:
                amount += order.commission

            to_pay = self.env['agent.commission.pay'].search([('agent_id','=',agent.id),('session_id','=',self.id)])
            print("to pay",to_pay.commission)
            if to_pay.commission >0.0:

                list.append((0, 0, {'agent_name': agent.id,'total_commission': amount,'commissin_to_pay':to_pay.commission}))

        # print("current id",self.id)
        # order_ids = self.env['pos.order'].search([])
        # for order in order_ids:





        # for order in order_ids:
        #     if self.id == order.session_id.id :
        #         if not order.agent_id.id in agent_commission:
        #             agent_commission[order.agent_id.id]=order.commission
        #             list.append((0, 0, {'agent_name': order.agent_id.name,
        #                                 'total_commission': order.commission}))
        #         else:
        #             commission_sum=agent_commission.get(order.agent_id.id)
        #             agent_commission[order.agent_id.id]=(order.commission+commission_sum)
        #             print(agent_commission[order.agent_id.id])
        # print(list)
        # for line in self.env['pay.commission.wizard'].commission_line_ids:
        #     print("enter into the loop")
        #     print(line)
        # lines=self.env['pay.commission.wizard'].search([])
        # print(lines.commission_line_ids.agent_name)



        return {'type': 'ir.actions.act_window',
                'name': 'Pay Commission',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'pay.commission.wizard',
                # 'context': {'default_saleOrderRef': self.id}
                'context': {'default_session_id': self.id,
                            'default_commission_line_ids': list}
                }

