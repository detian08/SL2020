# -*- coding: utf-8 -*-


from odoo import models, fields, api ,_
from odoo.osv import expression
from odoo.exceptions import UserError
from collections import Counter



class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_multi_barcodes = fields.One2many('multi.barcode.products', 'product_multi', string='Barcodes')

    _sql_constraints = [
        ('barcode_uniq', 'check(1=1)', 'No error')
    ]

    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        res.product_multi_barcodes.update({
            'template_multi': res.product_tmpl_id.id
        })
        return res

    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        self.product_multi_barcodes.update({
            'template_multi': self.product_tmpl_id.id
        })
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', ('name', operator, name), ('default_code', operator, name),
                      '|', ('barcode', operator, name), ('product_multi_barcodes', operator, name)]
        product_id = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(product_id).name_get()

    @api.constrains('barcode', 'product_multi_barcodes', 'active')
    def _check_unique_barcode(self):
        products = self.env['product.product'].search([
            '|',
            ('barcode', '!=', False),
            ('product_multi_barcodes', '!=', False),
        ])

        barcodes = products.mapped('barcode') + products.mapped('product_multi_barcodes.multi_barcode')

        duplicate_barcodes = Counter(barcodes)
        doubles_barcodes = {element: count for element, count in
                            duplicate_barcodes.items() if count > 1 and element}

        if doubles_barcodes:
            raise UserError(
                _('The following barcode(s) were found in other active products: {0}.'
                  '\nNote that product barcodes should not repeat themselves both in '
                  '"Barcode" field and "Barcodes Tab".').format(
                    ", ".join(doubles_barcodes.keys())
                )
            )
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    template_multi_barcodes = fields.One2many('multi.barcode.products', 'template_multi', string='Barcodes')

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        res.template_multi_barcodes.update({
            'product_multi': res.product_variant_id.id
        })
        return res

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if self.template_multi_barcodes:
            self.template_multi_barcodes.update({
                'product_multi': self.product_variant_id.id
            })
        return res

    _sql_constraints = [
        ('barcode_uniq', 'check(1=1)', 'No error')
    ]

    @api.constrains('barcode', 'template_multi_barcodes', 'active')
    def _check_unique_barcode(self):
        products = self.env['product.product'].search([
            '|',
            ('barcode', '!=', False),
            ('template_multi_barcodes', '!=', False),
        ])

        barcodes = products.mapped('barcode') + products.mapped('template_multi_barcodes.multi_barcode')

        duplicate_barcodes = Counter(barcodes)
        doubles_barcodes = {element: count for element, count in
                            duplicate_barcodes.items() if count > 1 and element}

        if doubles_barcodes:
            raise UserError(
                _('The following barcode(s) were found in other active products: {0}.'
                  '\nNote that product barcodes should not repeat themselves both in '
                  '"Barcode" field and "Barcodes Tab".').format(
                    ", ".join(doubles_barcodes.keys())
                )
            )


class ProductMultiBarcode(models.Model):
    _name = 'multi.barcode.products'

    multi_barcode = fields.Char(string="Barcode", help="Provide alternate barcodes for this product")
    product_multi = fields.Many2one('product.product')
    template_multi = fields.Many2one('product.template')

    def get_barcode_val(self, product):
        # returns barcode of record in self and product id
        return self.multi_barcode, product
