# # -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2020 (https://ingenieuxtech.odoo.com)
# info@ingenieuxtech.com
# ingenieuxtechnologies
#
##############################################################################
from odoo import api, fields, models, _


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        res.update({'tax_exception_certificate_id': order.tax_exception_certificate_id.id})
        return res
