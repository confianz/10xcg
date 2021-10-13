# # -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2020 (https://ingenieuxtech.odoo.com)
# info@ingenieuxtech.com
# ingenieuxtechnologies
#
##############################################################################
from odoo import api, fields, models
from .taxcloud_request import TaxCloudRequestExtendedSales


class SaleOrder(models.Model):
    _inherit = "sale.order"

    tax_exception_certificate_id = fields.Many2one("account.tax.certificate",
                                                   string="Tax Exception Certificate")

    @api.model
    def _get_TaxCloudRequest(self, api_id, api_key):
        return TaxCloudRequestExtendedSales(api_id, api_key)

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({'tax_exception_certificate_id': self.tax_exception_certificate_id.id})
        return res