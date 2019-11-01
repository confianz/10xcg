# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class OrderState(models.Model):
    _name = "order.state"
    _description = "Sale Order State"

    name = fields.Char(string='State', required=True)
    description = fields.Char(string='Description')

OrderState()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
