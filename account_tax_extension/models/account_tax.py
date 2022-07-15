from odoo import fields, models, api


class AccountTaxGroup(models.Model):
    _inherit = "account.tax"

    @api.model
    def default_get(self, field_list=[]):
        res = super(AccountTaxGroup, self).default_get(field_list)
        account = self.env['account.account'].search([('is_account_tax', "=", True)], limit=1)
        if account:
            for refund_repartition_line in res['refund_repartition_line_ids']:
                if refund_repartition_line[2]['repartition_type'] == 'tax':
                    refund_repartition_line[2]['account_id'] = account.id
            for invoice_repartition_line in res['invoice_repartition_line_ids']:
                if invoice_repartition_line[2]['repartition_type'] == 'tax':
                    invoice_repartition_line[2]['account_id'] = account.id
        return res
