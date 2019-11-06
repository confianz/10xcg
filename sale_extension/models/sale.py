# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def _default_stage_id(self):
        lowest_sequence_stage = self.env['order.state'].search([], order='sequence', limit=1)
        return lowest_sequence_stage or False


    order_state = fields.Many2one('order.state', string='State', copy=False, default=lambda self: self._default_stage_id())
    po_count = fields.Integer(string='# of RFQ', compute='get_po_ids', readonly=True, store=True, copy=False)

    @api.depends('order_line.purchase_order_id')
    def get_po_ids(self):
        for rec in self :
            rec.update({'po_count': len(rec.order_line.mapped('purchase_order_id').ids)})

    def action_request_for_quotation(self):
        if self.po_count == 1:
            action = self.env.ref('purchase.purchase_order_action_generic').read()[0]
            action['res_id'] = self.order_line.mapped('purchase_order_id').id
        elif self.po_count >1:
            action = self.env.ref('purchase.purchase_rfq').read()[0]
            action['domain'] = [('id', 'in', self.order_line.mapped('purchase_order_id').ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

SaleOrder()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', copy=False)

SaleOrderLine()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
