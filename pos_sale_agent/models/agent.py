# -*- coding: utf-8 -*-

from random import choice
from string import digits

from odoo import models, fields, api, exceptions, _, SUPERUSER_ID


class Agent(models.Model):
    _inherit = "hr.employee"
    _name = "sale.agent"
    _description = "Sale agent"
    _inherits = {'res.partner': 'partner_id'}
    
    

    def _default_random_pin(self):
        return ("".join(choice(digits) for i in range(4)))

    def _default_random_barcode(self):
        barcode = None
        while not barcode or self.env['sale.agent'].search([('barcode', '=', barcode)]):
            barcode = "027"+"".join(choice(digits) for i in range(6))
        return barcode

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True,
        string='Related Partner', help='Partner-related data of the agent')
    barcode = fields.Char(string="Badge ID", help="ID used for agent identification.", default=_default_random_barcode, copy=False)
    pin = fields.Char(string="PIN", default=_default_random_pin, help="PIN used to Check In/Out in Kiosk Mode (if enabled in Configuration).", copy=False)
    team_ids = fields.Many2many(
        'crm.team',
        'sale_agent_crm_rel',
        'agent_id',
        'team_id',
        string='Agents'
    )
    name = fields.Char(related='partner_id.name', inherited=True)
    code_agent= fields.Char("Code")

    _sql_constraints = [('barcode_uniq', 'unique (barcode)', "The Badge ID must be unique, this one is already assigned to another agent.")]

    @api.model_cr_context
    def _init_column(self, column_name):
        """ Initialize the value of the given column for existing rows.
            Overridden here because we need to have different default values
            for barcode and pin for every agent.
        """
        is_attendance_installed = None
        try:
            is_attendance_installed = self.env['ir.module.module'].sudo().search([('name', '=', 'hr_attendance')])
            is_attendance_installed = is_attendance_installed and (is_attendance_installed.state == 'installed')
        except:
            pass
        if is_attendance_installed or column_name not in ["barcode", "pin"]:
            super(Agent, self)._init_column(column_name)
        else:
            default_compute = self._fields[column_name].default

            query = 'SELECT id FROM "%s" WHERE "%s" is NULL' % (
                self._table, column_name)
            self.env.cr.execute(query)
            agent_ids = self.env.cr.fetchall()

            for agent_id in agent_ids:
                default_value = default_compute(self)

                query = 'UPDATE "%s" SET "%s"=%%s WHERE id = %s' % (
                    self._table, column_name, agent_id[0])
                self.env.cr.execute(query, (default_value,))
    @api.model
    def create(self, vals):
        agent = super(Agent, self).create(vals)
        agent.partner_id.active = agent.active
        agent.partner_id.employee = True
        agent.partner_id.customer = False
        agent.partner_id.email = agent.work_email
        return agent

class CrmTeam(models.Model):
    _inherit = "crm.team"

    agent_ids = fields.Many2many(
        'sale.agent',
        'sale_agent_crm_rel',
        'team_id',
        'agent_id',
        string='Agents'
    )
