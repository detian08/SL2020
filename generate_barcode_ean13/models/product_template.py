# -*- encoding: utf-8 -*-
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

try:
    import barcode
except ImportError:
    _logger.debug("Cannot import 'viivakoodi' python library.")
    barcode = None


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_product_code(self,product_id):
        product_code=""
        if len(product_id)==1:
           product_code="00000"+product_id

        if len(product_id)==2:
           product_code="0000"+product_id

        if len(product_id)==3:
           product_code="000"+product_id

        if len(product_id)==4:
           product_code="00"+product_id

        if len(product_id)==5:
           product_code="0"+product_id

        if len(product_id)==6:
           product_code=product_id
        return product_code

    @api.multi
    def generate_barcode(self):
        if self.company_id.code_entreprise:
            pattern_code='624'+str(self.company_id.code_entreprise)+self.get_product_code(str(self.id))
            self.barcode = barcode.get('ean13', pattern_code)

    @api.multi
    def generate_barcode_server(self):
        for product in self:
            product.generate_barcode()


class ProductTemplate(models.Model):
    _inherit = "product.product"

    def get_product_code(self,product_id):
        product_code=""
        if len(product_id)==1:
           product_code="00000"+product_id

        if len(product_id)==2:
           product_code="0000"+product_id

        if len(product_id)==3:
           product_code="000"+product_id

        if len(product_id)==4:
           product_code="00"+product_id

        if len(product_id)==5:
           product_code="0"+product_id

        if len(product_id)==6:
           product_code=product_id
        return product_code

    @api.multi
    def generate_barcode(self):
        if self.company_id.code_entreprise:
            pattern_code='624'+str(self.company_id.code_entreprise)+self.get_product_code(str(self.id))
            self.barcode = barcode.get('ean13', pattern_code)

    @api.multi
    def generate_barcode_server(self):
        for product in self:
            product.generate_barcode()