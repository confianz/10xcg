# # -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2020 (https://ingenieuxtech.odoo.com)
# info@ingenieuxtech.com
# ingenieuxtechnologies
#
##############################################################################
from odoo import api,fields,models


class ResPartner(models.Model):
    _inherit = "res.partner"

    tax_exception_certificate_ids = fields.One2many("account.tax.certificate", "res_id",
                                                    string="Tax Exception Certificate")
