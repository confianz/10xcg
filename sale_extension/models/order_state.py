# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class OrderState(models.Model):
    _name = "order.state"
    _description = "Sale Order State"

    _order = "sequence, name, id"


    name = fields.Char(string='State', required=True)
    description = fields.Char(string='Description')
    sequence = fields.Integer(string='Sequence', default=10)

OrderState()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
