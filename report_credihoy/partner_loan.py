# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

# from odoo.report import report_sxw
import time
import datetime
# from openerp import pooler
# from openerp.osv import osv
from odoo import fields, api, models
from datetime import date
# import mx.DateTime
# from mx.DateTime import RelativeDateTime, now, DateTime, localtime

# class PartnerLoan(report_sxw.rml_parse):
class PartnerLoan(models.AbstractModel):
    _name = 'report.pragtech_loan_advance.partner_loan'
    _description = "Report pragtech_loan_advance partner_loan"
    s=0.0
    _capital=0.0
    _interest=0.0
    _subtotal=0.0

#     def __init__(self, name):
# 
#         super(PartnerLoan, self).__init__(name)
#         self.localcontext.update({
#             'time': time,
#             'get_loan':self.__get_loan__,
#             'ending_date' : self.__ending_date__,
#             'installment': self.__installment__,
#             #'amount_total' : self.__amount_total__,
#             'get_capital': self.__get_capital__,
#             'get_interest':self.__get_interest__,
#             'get_subtotal':self.__get_subtotal__,
#         })
    @api.multi
    def _get_report_values(self, docids, data=None):
        loan = self.env['account.loan'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.loan',
            'data': data,
            'docs': loan,
            'time': time,
            'get_loan':self.__get_loan__,
            'ending_date' : self.__ending_date__,
            'installment': self.__installment__,
            'get_capital': self.__get_capital__,
            'get_interest':self.__get_interest__,
            'get_subtotal':self.__get_subtotal__,
        }
        # return self.env['report'].render('account_loan.partner_loan', docargs)
        # return self.env.ref('pragtech_loan_advance.payment_receipt_report_document').report_action(self,data=docargs)
        return docargs

    def __get_loan__(self, partner_id):

        tc = self.env['account.loan']
        ids = tc.search(self._cr, self._uid, [('partner_id','=',partner_id)])
        res = []
        for loan in tc.browse(self._cr, self._uid, ids, {'partner_id':partner_id}):
            res.append(loan)

        return res

    def __installment__(self,install):

        self._capital=self._capital+ install.capital
        self._interest= self._interest+install.interest
        self._subtotal= self._subtotal + install.capital + install.interest

        return install.total

#    def __amount_total__(self,install):
#        self.s = self.s + install.capital
#        return self.s

    def __get_capital__(self,loan):
        self.cr.execute("SELECT SUM(capital) from account_loan_installment where \
                        account_loan_installment.loan_id=" +str(loan.id))
        return self.cr.fetchone()[0] or 0.0

        #return self._capital

    def __get_interest__(self,loan):
        self.cr.execute("SELECT SUM(interest) from account_loan_installment where \
                        account_loan_installment.loan_id=" +str(loan.id))
        return self.cr.fetchone()[0] or 0.0

        #return self._interest

    def __get_subtotal__(self,loan):
        self.cr.execute("SELECT SUM(total) from account_loan_installment where \
                        account_loan_installment.loan_id=" +str(loan.id))
        return self.cr.fetchone()[0] or 0.0

#        self.cr.execute("SELECT SUM(total) from account_loan_installment, account_loan where \
#        account_loan_installment.loan_id=account_loan.id and account_loan.id=" +str(loan.id)+" group by account_loan_installment.loan_id")

        #return self._subtotal

    def __ending_date__(self,loan):

        start_date = loan.approve_date
        total_inst = loan.total_installment

        i = 366
        j = 12
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].search([('code', '=', lang_code)])
        if j == total_inst:
#             end_date = mx.DateTime.strptime(start_date, '%Y-%m-%d') + RelativeDateTime(days=i)
            if start_date:
                    # d = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    d = start_date
                    date_1 = datetime.date.strftime(d, str(lang.date_format))
                    end_date = datetime.datetime.strptime(date_1, str(lang.date_format)) + datetime.timedelta(days=i)
                    end_date = datetime.date.strftime(end_date, str(lang.date_format))
        else:
            while j < total_inst:
                j = j + 12
                i = i + 365

                if start_date:
                    # d = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    d = start_date
                    date_1 = datetime.date.strftime(d, str(lang.date_format))
                    end_date = datetime.datetime.strptime(date_1, str(lang.date_format)) + datetime.timedelta(days=i)
                    end_date = datetime.date.strftime(end_date, str(lang.date_format))
        return end_date

#    def __amount_total__(self,loan):
#
#         self.cr.execute("SELECT SUM(total) from account_loan_installment where loan_id=%d" % (1))
#         self.cr.execute("SELECT SUM(total) from account_loan_installment, account_loan where \
#                        account_loan_installment.loan_id=account_loan.id and account_loan.id=" +str(loan.id)+" group by account_loan_installment.loan_id")
#         res = self.cr.fetchone()[0]
#         return res

# report_sxw.report_sxw('report.account.partner.loan',
#                        'account.loan',
#                         'addons/pragtech_loan/report/partner_loan.rml',
#                         parser=PartnerLoan)
