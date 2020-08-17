# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta

import urllib.parse
import requests
import math

#class ResTags(models.Model):
#    _name = 'res.partner.tag'
#    _description = 'Res Partner Tags'

#    name = fields.Char('Display Name')
#    email = fields.Char('Display email')
#    color = fields.Integer()

class Lead(models.Model):
    _inherit = "crm.lead"

    monto_sol = fields.Float(string="Monto")
    monto_solicitado = fields.Char(string='Monto Solicitado', help='Monto de crédito solicitado por el prospecto')
    periodo_meses = fields.Char(string='Periodo en Meses', help='Periodo elegido para pagar el crédito')
    pago_mensual = fields.Char(string='Pago Mensual', help='Monto a pagar mensualmente')

    @api.onchange('description')
    def get_amt(self):

        for rec in self:
            end = None
            mnt_sol = rec.description
            res = mnt_sol[18:end]

            print (res)

            rec.monto_sol = float(res)
