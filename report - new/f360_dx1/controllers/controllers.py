# -*- coding: utf-8 -*-
from odoo import http

# class F360Pld(http.Controller):
#     @http.route('/f360_pld/f360_pld/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f360_pld/f360_pld/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('f360_pld.listing', {
#             'root': '/f360_pld/f360_pld',
#             'objects': http.request.env['f360_pld.f360_pld'].search([]),
#         })

#     @http.route('/f360_pld/f360_pld/objects/<model("f360_pld.f360_pld"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f360_pld.object', {
#             'object': obj
#         })