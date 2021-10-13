# # -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2020 (https://ingenieuxtech.odoo.com)
# info@ingenieuxtech.com
# ingenieuxtechnologies
#
##############################################################################
from odoo import api,fields,models
from .taxcloud_request import TaxCloudRequestExtended

class AccountMove(models.Model):
    _inherit = "account.move"

    tax_exception_certificate_id = fields.Many2one("account.tax.certificate",
                                                    string="Tax Exception Certificate")

    @api.model
    def _get_TaxCloudRequest(self, api_id, api_key):
        return TaxCloudRequestExtended(api_id, api_key)

