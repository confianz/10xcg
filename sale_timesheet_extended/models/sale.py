# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    order_timesheet_ids = fields.One2many('account.analytic.line', 'order_id', 'Timesheets')

SaleOrder()




class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    order_id = fields.Many2one('sale.order', 'Sale Order')



AccountAnalyticLine()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
