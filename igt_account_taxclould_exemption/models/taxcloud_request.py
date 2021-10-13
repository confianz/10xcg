# # -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2020 (https://ingenieuxtech.odoo.com)
# info@ingenieuxtech.com
# ingenieuxtechnologies
#
##############################################################################


import logging
from zeep.exceptions import Fault
from odoo.addons.account_taxcloud.models.taxcloud_request import TaxCloudRequest
from odoo.addons.sale_account_taxcloud.models.taxcloud_request import TaxCloudRequest as SalesTaxClould
from odoo import modules, fields, _

_logger = logging.getLogger(__name__)


class TaxCloudRequestExtendedSales(SalesTaxClould):
    def set_order_items_detail(self, order):
        self.certificate_id = self.factory.ExemptionCertificate()
        self.certificate_id.CertificateID = order.tax_exception_certificate_id.certificate_id
        super(TaxCloudRequestExtendedSales, self).set_order_items_detail(order)

    def get_all_taxes_values(self):
        customer_id = hasattr(self, 'customer_id') and self.customer_id or 'NoCustomerID'
        cart_id = hasattr(self, 'cart_id') and self.cart_id or 'NoCartID'
        _logger.info('fetching tax values for cart %s (customer: %s)', cart_id, customer_id)
        _logger.info("Sales Order Certificate ID %s", self.certificate_id)
        formatted_response = {}
        if not self.api_login_id or not self.api_key:
            formatted_response['error_message'] = _("Please configure taxcloud credential on the current company"
                                                    "or use a different fiscal position")
            return formatted_response

        try:
            if self.certificate_id.CertificateID:
                response = self.client.service.Lookup(
                    self.api_login_id,
                    self.api_key,
                    customer_id,
                    cart_id,
                    self.cart_items,
                    self.origin,
                    self.destination,
                    False,
                    self.certificate_id
                )
            else:
                response = self.client.service.Lookup(
                    self.api_login_id,
                    self.api_key,
                    customer_id,
                    cart_id,
                    self.cart_items,
                    self.origin,
                    self.destination,
                    False
                )

            formatted_response['response'] = response
            if response.ResponseType == 'OK':
                formatted_response['values'] = {}
                for item in response.CartItemsResponse.CartItemResponse:
                    index = item.CartItemIndex
                    tax_amount = item.TaxAmount
                    formatted_response['values'][index] = tax_amount
            elif response.ResponseType == 'Error':
                formatted_response['error_message'] = response.Messages.ResponseMessage[0].Message
        except Fault as fault:
            formatted_response['error_message'] = fault.message
        except IOError:
            formatted_response['error_message'] = "TaxCloud Server Not Found"
        return formatted_response


class TaxCloudRequestExtended(TaxCloudRequest):
    """ Added exemption certificate details along with Invoice if there is exemption certificate
    it will update the tex in Low-level object intended to interface Odoo recordsets with TaxCloud,
        through appropriate SOAP requests """

    def set_invoice_items_detail(self, invoice):
        self.certificate_id = self.factory.ExemptionCertificate()
        self.certificate_id.CertificateID = invoice.tax_exception_certificate_id.certificate_id
        super(TaxCloudRequestExtended, self).set_invoice_items_detail(invoice)

    def get_all_taxes_values(self):
        customer_id = hasattr(self, 'customer_id') and self.customer_id or 'NoCustomerID'
        cart_id = hasattr(self, 'cart_id') and self.cart_id or 'NoCartID'
        _logger.info('fetching tax values for cart %s (customer: %s)', cart_id, customer_id)
        formatted_response = {}
        if not self.api_login_id or not self.api_key:
            formatted_response['error_message'] = _("Please configure taxcloud credential on the current company"
                                                    "or use a different fiscal position")
            return formatted_response

        try:
            if self.certificate_id.CertificateID:
                response = self.client.service.Lookup(
                    self.api_login_id,
                    self.api_key,
                    customer_id,
                    cart_id,
                    self.cart_items,
                    self.origin,
                    self.destination,
                    False,
                    self.certificate_id
                )
            else:
                response = self.client.service.Lookup(
                    self.api_login_id,
                    self.api_key,
                    customer_id,
                    cart_id,
                    self.cart_items,
                    self.origin,
                    self.destination,
                    False
                )

            formatted_response['response'] = response
            if response.ResponseType == 'OK':
                formatted_response['values'] = {}
                for item in response.CartItemsResponse.CartItemResponse:
                    index = item.CartItemIndex
                    tax_amount = item.TaxAmount
                    formatted_response['values'][index] = tax_amount
            elif response.ResponseType == 'Error':
                formatted_response['error_message'] = response.Messages.ResponseMessage[0].Message
        except Fault as fault:
            formatted_response['error_message'] = fault.message
        except IOError:
            formatted_response['error_message'] = "TaxCloud Server Not Found"
        return formatted_response
