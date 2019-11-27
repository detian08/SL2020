# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp





class PosConfig(models.Model):
    _inherit = 'pos.config'

    hide_search = fields.Boolean("Hide Search")

