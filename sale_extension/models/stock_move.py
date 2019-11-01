# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('sale_line_id', False):
                val.update({'procure_method': 'make_to_stock'})
        res = super(StockMove, self).create(vals)
        return res

StockMove()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
