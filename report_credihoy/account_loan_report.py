# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class AccountLoanReport(models.Model):
    _name = "account.loan.report"
    _description = "Loan Detail Statistics"
    _auto = False

    loan_id = fields.Char('Loan Number', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    loan_amt = fields.Float('Amount', readonly=True)
    approve_amount = fields.Float('Disbursement Amount', readonly=True)
    country_id = fields.Many2one('res.country', 'Partner Country', readonly=True)
    approve_date = fields.Date('Approve Date', readonly=True)
    duration = fields.Integer('Terms Duration', readonly=True)
    principle = fields.Float('Principle Amount', readonly=True)
    total_disbursed = fields.Float('Disbursed Amount', readonly=True)
    payment_freq = fields.Selection([('monthly','Monthly'), ('quarterly','Quarterly'), ('half_yearly','Half-Yearly'),('yearly','Yearly')], "Payment Frequency", readonly=True)
    state = fields.Selection([
       ('draft', 'Apply'),
       ('apply', 'Loan Sanctioned'),
       ('partial', 'Partially Disbursed'),
       ('approved', 'Loan Disbursed'),
       ('done', 'Closed'),
       ('cancel', 'Reject'),
    ], 'State', readonly=True )
    
    def _select(self):
        select_str = """
            
            SELECT min(al.id) as id,
            al.partner_id,
            al.company_id,
            al.loan_id,
            al.approve_date,
            al.approve_amount,
            al.req_amt,
            al.loan_amt,
            al.payment_freq,
            al.user_id,
            al.state,
            partner.country_id,
            sum(ail.capital) as principle
        """ 
        return select_str
#             count(*) as duration,
#             
#             sum(ald.disbursement_amt) as total_disbursed

#                     l.product_id as product_id,
#                     t.uom_id as product_uom,
#                     sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
#                     sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
#                     sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
#                     sum(l.qty_to_invoice / u.factor * u2.factor) as qty_to_invoice,
#                     sum(l.price_total / COALESCE(cr.rate, 1.0)) as price_total,
#                     sum(l.price_subtotal / COALESCE(cr.rate, 1.0)) as price_subtotal,
#                     sum(l.amt_to_invoice / COALESCE(cr.rate, 1.0)) as amt_to_invoice,
#                     sum(l.amt_invoiced / COALESCE(cr.rate, 1.0)) as amt_invoiced,
#                     count(*) as nbr,
#                     s.name as name,
#                     s.date_order as date,
#                     s.confirmation_date as confirmation_date,
#                     s.state as state,
#                     s.partner_id as partner_id,
#                     s.user_id as user_id,
#                     s.company_id as company_id,
#                     extract(epoch from avg(date_trunc('day',s.date_order)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
#                     t.categ_id as categ_id,
#                     s.pricelist_id as pricelist_id,
#                     s.analytic_account_id as analytic_account_id,
#                     s.team_id as team_id,
#                     p.product_tmpl_id,
#                     partner.country_id as country_id,
#                     partner.commercial_partner_id as commercial_partner_id,
#                     sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
#                     sum(p.volume * l.product_uom_qty / u.factor * u2.factor) as volume

    def _from(self):
        from_str = """
                account_loan_installment ail
                      join account_loan al on (ail.loan_id=al.id)
                      join res_partner partner on al.partner_id = partner.id
        """
#                       left join payment_schedule_line psl on (al.id=psl.loan_id)
#                       left join account_loan_disbursement ald on (al.id=ald.loan_id)


#                         left join product_product p on (l.product_id=p.id)
#                             left join product_template t on (p.product_tmpl_id=t.id)
#                     left join product_uom u on (u.id=l.product_uom)
#                     left join product_uom u2 on (u2.id=t.uom_id)
#                     left join product_pricelist pp on (s.pricelist_id = pp.id)
#                     left join currency_rate cr on (cr.currency_id = pp.currency_id and
#                         cr.company_id = s.company_id and
#                         cr.date_start <= coalesce(s.date_order, now()) and
#                         (cr.date_end is null or cr.date_end > coalesce(s.date_order, now())))
        return from_str

#             psl.loan_id,
    def _group_by(self):
        group_by_str = """
            GROUP BY ail.loan_id,
            al.partner_id,
            al.company_id,
            al.loan_id,
            al.approve_date,
            al.req_amt,
            al.approve_amount,
            al.loan_amt,
            al.payment_freq,
            al.user_id,
            al.state,
            partner.country_id
            
        """
#             l.product_id,
#                     l.order_id,
#                     t.uom_id,
#                     t.categ_id,
#                     s.name,
#                     s.date_order,
#                     s.confirmation_date,
#                     s.partner_id,
#                     s.user_id,
#                     s.state,
#                     s.company_id,
#                     s.pricelist_id,
#                     s.analytic_account_id,
#                     s.team_id,
#                     p.product_tmpl_id,
#                     partner.country_id,
#                     partner.commercial_partner_id
        return group_by_str

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by())
#         print(query)
        self.env.cr.execute(query)
        
        
#         SELECT min(ail.id) as id,
#             al.partner_id,
#             al.company_id,
#             al.loan_id,
#             al.approve_date,
#             al.approve_amount,
#             al.req_amt,
#             al.loan_amt,
#             al.payment_freq,
#             al.user_id,
#             al.state,
#             partner.country_id,
#             count(psl) as duration,
#             sum(ail.capital) as principle,
#             sum(ald.disbursement_amt) as total_disbursed
#             FROM ( 
#                 account_loan_installment ail
#                       join account_loan al on (ail.loan_id=al.id)
#                       join res_partner partner on al.partner_id = partner.id
#                       left join payment_schedule_line psl on (al.id=psl.loan_id)
#                       left join account_loan_disbursement ald on (al.id=ald.loan_id)
#          ) 
#             GROUP BY al.partner_id,
#             al.company_id,
#             al.loan_id,
#             al.approve_date,
#             al.req_amt,
#             al.approve_amount,
#             al.loan_amt,
#             al.payment_freq,
#             al.user_id,
#             al.state,
#             partner.country_id


