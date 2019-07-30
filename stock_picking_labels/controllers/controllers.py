# -*- coding: utf-8 -*-
from odoo import http

# class StockPickinLabels(http.Controller):
#     @http.route('/stock_picking_labels/stock_picking_labels/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_labels/stock_picking_labels/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_labels.listing', {
#             'root': '/stock_picking_labels/stock_picking_labels',
#             'objects': http.request.env['stock_picking_labels.stock_picking_labels'].search([]),
#         })

#     @http.route('/stock_picking_labels/stock_picking_labels/objects/<model("stock_picking_labels.stock_picking_labels"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_labels.object', {
#             'object': obj
#         })