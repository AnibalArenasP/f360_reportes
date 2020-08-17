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
from odoo import fields,models,api
from datetime import date

# class LoanPaper(report_sxw.rml_parse):
class LoanPaper(models.AbstractModel):
    _name = 'report.pragtech_loan_advance.merge_letter'
    _description = "report.pragtech_loan_advance.merge_letter"
#     def __init__(self, name):
#         super(LoanPaper, self).__init__(name)
#         self.localcontext.update({
#             'time': time,
#             'merge' : self.__parse_paragraph__,
#         })
    @api.model
    def _get_report_values(self, docids, data=None):
        loan = self.env['account.loan'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.loan',
            'data': data,
            'docs': loan,
            'time': time,
            'merge' : self.__parse_paragraph__,
        }
#         return self.env['report'].render('account_loan.merge_letter', docargs)
        return docargs

    def __parse_paragraph__(self,content,loan):

        fetchval={
            '{p_name}':loan.name or '',
            '{p_loan_amount}':str(loan.loan_amount) or '',
            '{p_loan_period}':str(loan.loan_period) or '',
            '{p_process_fee}':str(loan.process_fee) or '',
            '{p_apply_date}':str(loan.apply_date) or '',
            '{p_approve_date}':str(loan.approve_date) or '',
            '{p_approve_amount}':str(loan.approve_amount) or '',
            '{p_contact}': str(loan.partner_id.name) + '\n' + str(loan.partner_id.street) + '\n ' + str(loan.partner_id.street2) + '\n ' + str(loan.partner_id.city) + '\n' + str(loan.partner_id.zip) or '',
        }
        for key in fetchval :
            content=content.replace(key,fetchval.get(key))
        return content;

# report_sxw.report_sxw('report.letter.letter_info', 'account.loan', 'addons/pragtech_loan/report/merge_letter.rml', parser=LoanPaper)
