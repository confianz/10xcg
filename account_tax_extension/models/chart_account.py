from odoo import fields,models,api

class AccountAccount(models.Model):
      _inherit="account.account"

      is_account_tax = fields.Boolean(string="is tax account")

