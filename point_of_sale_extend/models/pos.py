from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PosConfig(models.Model):
    _inherit = 'pos.config'

    
    invoicing_mnd = fields.Boolean(string="Invoicing Mandatory")
