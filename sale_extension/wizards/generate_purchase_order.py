# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class GeneratePurchaseOrder(models.TransientModel):
    _name = "generate.purchase.order"

    line_ids = fields.One2many('generate.purchase.order.line', 'order_id')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")

    @api.model
    def default_get(self, fields):
        res = super(GeneratePurchaseOrder, self).default_get(fields)
        if self.env.context.get('active_model', '') == 'sale.order':
            for order in self.env['sale.order'].browse(self._context.get('active_ids', 0)):
                list_lines = []
                for line in order.order_line.filtered(lambda r: not r.purchase_order_id):
                    list_lines.append(
                        (0, 0, {'product_id': line.product_id.id,
                                'qty': line.product_uom_qty,
                                'product_uom': line.product_uom.id,
                                'sale_line_id': line.id,
                                'vendor_selector_ids' : [s.id for s in line.product_id.seller_ids] or [],
                                })
                    )
                res['line_ids'] = list_lines
                res['sale_order_id'] = self._context.get('active_ids', 0)[0]

        return res





    def generate_rfq(self):
        """
        This method creates purchase order based on sale order line
        and selected vendors.
        """
        for record in self:
            vendors = record.line_ids.mapped('vendor_id')
            rfq_lines = [record.line_ids.filtered(lambda r: r.vendor_id and r.vendor_id.id == vendor.id) for vendor in vendors]
            for lines in rfq_lines:
                vals = {
                    'company_id': record.sale_order_id.company_id.id,
                    'partner_id': lines[0].vendor_id and lines[0].vendor_id.name and lines[0].vendor_id.name.id or False,
                    'order_line':[(0,0,{
                        'name': line.product_id.display_name,
                        'date_planned': fields.Datetime.now(),
                        'product_id': line.product_id.id,
                        'product_qty': line.qty,
                        'product_uom': line.product_uom.id,
                        'price_unit': line.vendor_price,
                        'company_id': record.sale_order_id.company_id.id,
                    }) for line in lines]
                }
                po_id = self.env['purchase.order'].create(vals)
                lines.mapped('sale_line_id').write({'purchase_order_id': po_id.id})


GeneratePurchaseOrder()


class GeneratePurchaseOrderLine(models.TransientModel):
    _name = "generate.purchase.order.line"

    product_id = fields.Many2one('product.product', string="Product")
    qty = fields.Float('Quantity')
    product_uom = fields.Many2one('uom.uom', string="Unit Of Measure")
    order_id = fields.Many2one('generate.purchase.order', string="Order")
    vendor_id = fields.Many2one('product.supplierinfo', string='Vendor', copy=False)
    sale_line_id = fields.Many2one('sale.order.line', string='Sale Order Line')
    vendor_selector_ids = fields.Many2many('product.supplierinfo', string='Vendor Domain List', help='preset m2m field for domain forcing.')
    vendor_price = fields.Float(string='Vendor Price')

    @api.onchange('vendor_id')
    def onchange_vendor(self):
        for line in self:
            line.vendor_price = line.vendor_id.price


GeneratePurchaseOrderLine()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
