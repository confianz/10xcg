# # -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2020 (https://ingenieuxtech.odoo.com)
# info@ingenieuxtech.com
# ingenieuxtechnologies
#
##############################################################################
from odoo import api, fields, models
import requests
from odoo.exceptions import UserError
import json


class AccountTaxCertificate(models.Model):
    _name = "account.tax.certificate"
    _rec_name = "certificate_id"

    res_id = fields.Many2one("res.partner", "customer Id")
    certificate_id = fields.Char("Certificate ID")
    exempt_states_ids = fields.One2many("exempt.states", "account_tax_certificate_id",
                                        string="Purchase ID")
    purchaser_ids = fields.One2many("purchaser.details", "account_tax_certificate_id",
                                    string="Purchase ID")

    @api.constrains("purchaser_ids")
    def check_purchaser_ids(self):
        if len(self.purchaser_ids) == 0:
            raise UserError("Please add a Purchaser Details.")
        if len(self.purchaser_ids) > 1:
            raise UserError("Please add only one Purchaser Details.")

    @api.model
    def create(self, vals):
        res = super(AccountTaxCertificate, self).create(vals)
        self.send_exeption_to_tax_clould()
        return res

    def send_exeption_to_tax_clould(self):
        if self.certificate_id:
            raise UserError("Certificate ID is already Set")

        res = self
        ExemptStates = []
        for line in res.exempt_states_ids:
            data_dict = {"IdentificationNumber": line.identification_number,
                         "ReasonForExemption": line.reason_for_exemption,
                         "StateAbbr": line.state_abbr_id.code}
            ExemptStates.append(data_dict)

        PurchaserAddress1 = PurchaserAddress2 = PurchaserBusinessType = PurchaserBusinessTypeOtherValue \
            = PurchaserCity = PurchaserExemptionReason = PurchaserExemptionReasonOtherValue = \
            PurchaserFirstName = PurchaserLastName = PurchaserState = IDNumber = StateOfIssue = \
            TaxType = PurchaserTitle = PurchaserZip = ""
        for rec in res.purchaser_ids:
            PurchaserAddress1 = rec.purchaser_address1
            PurchaserAddress2 = rec.purchaser_address2
            PurchaserBusinessType = rec.purchaser_business_type
            if rec.purchaser_business_type == "Other":
                PurchaserBusinessTypeOtherValue = rec.purchaser_business_type_other_value
            PurchaserCity = rec.purchaser_city
            PurchaserExemptionReason = rec.purchaser_exemption_reason
            if rec.purchaser_exemption_reason == 'Other':
                PurchaserExemptionReasonOtherValue = rec.purchaser_exemption_reason_other_value
            PurchaserFirstName = rec.purchaser_first_name
            PurchaserLastName = rec.purchaser_last_name
            PurchaserState = rec.purchaser_state
            IDNumber = rec.id_number
            StateOfIssue = rec.state_of_issue_id.code
            TaxType = rec.tax_type
            PurchaserTitle = rec.purchaser_title
            PurchaserZip = str(rec.purchaser_zip)

        address_to_verify = {
            "apiKey": self.env.user.company_id.taxcloud_api_key,
            "apiLoginID": self.env.user.company_id.taxcloud_api_id,
            "customerID": res.res_id.id,
            "exemptCert": {

                "Detail": {
                    "CreatedDate": "20-11-2020",
                    "ExemptStates": ExemptStates,
                    "PurchaserAddress1": PurchaserAddress1,
                    "PurchaserAddress2": PurchaserAddress2,
                    "PurchaserBusinessType": PurchaserBusinessType,
                    "PurchaserBusinessTypeOtherValue": PurchaserBusinessTypeOtherValue,
                    "PurchaserCity": PurchaserCity,
                    "PurchaserExemptionReason": PurchaserExemptionReason,
                    "PurchaserExemptionReasonOtherValue": PurchaserExemptionReasonOtherValue,
                    "PurchaserFirstName": PurchaserFirstName,
                    "PurchaserLastName": PurchaserLastName,
                    "PurchaserState": PurchaserState,
                    "PurchaserTaxID": {
                        "IDNumber": IDNumber,
                        "StateOfIssue": StateOfIssue,
                        "TaxType": TaxType
                    },
                    "PurchaserTitle": PurchaserTitle,
                    "PurchaserZip": PurchaserZip
                }
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }

        result = requests.post("https://api.taxcloud.net/1.0/TaxCloud/AddExemptCertificate",
                               data=json.dumps(address_to_verify), headers=headers)

        result = result.json()
        res.certificate_id = result.get('CertificateID')
        return res

    def unlink(self):
        for rec in self:
            delete_dict = {
                "apiKey": self.env.user.company_id.taxcloud_api_key,
                "apiLoginID": self.env.user.company_id.taxcloud_api_id,
                "certificateID": rec.certificate_id
            }
            requests.post("https://api.taxcloud.net/1.0/TaxCloud/DeleteExemptCertificate",
                          data=delete_dict)
        return super(AccountTaxCertificate, self).unlink()


class ExemptStates(models.Model):
    _name = "exempt.states"

    identification_number = fields.Char("IdentificationNumber")
    reason_for_exemption = fields.Char("ReasonForExemption")
    state_abbr_id = fields.Many2one("res.country.state", "StateAbbr")
    account_tax_certificate_id = fields.Many2one("account.tax.certificate",
                                                 string="Account Tax certificate")


class PurchaseTaxID(models.Model):
    _name = "purchaser.details"

    purchaser_address1 = fields.Char("PurchaserAddress1")
    purchaser_address2 = fields.Char("PurchaserAddress2")
    purchaser_business_type = fields.Selection([
        ("AccommodationAndFoodServices", "AccommodationAndFoodServices"),
        ("Agricultural_Forestry_Fishing_Hunting", "Agricultural_Forestry_Fishing_Hunting"),
        ("Construction", "Construction"),
        ("FinanceAndInsurance", "FinanceAndInsurance"),
        ("Information_PublishingAndCommunications", "Information_PublishingAndCommunications"),
        ("Manufacturing", "Manufacturing"),
        ("Mining", "Mining"),
        ("RealEstate", "RealEstate"),
        ("RentalAndLeasing", "RentalAndLeasing"),
        ("RetailTrade", "RetailTrade"),
        ("TransportationAndWarehousing", "TransportationAndWarehousing"),
        ("Utilities", "Utilities"),
        ("WholesaleTrade", "WholesaleTrade"),
        ("BusinessServices", "BusinessServices"),
        ("ProfessionalServices", "ProfessionalServices"),
        ("EducationAndHealthCareServices", "EducationAndHealthCareServices"),
        ("NonprofitOrganization", "NonprofitOrganization"),
        ("Government", "Government"),
        ("NotABusiness", "NotABusiness"),
        ("Other", "Other")], string="PurchaserBusinessType")
    purchaser_business_type_other_value = fields.Char("PurchaserBusinessTypeOtherValue")
    purchaser_city = fields.Char("PurchaserCity")
    purchaser_exemption_reason = fields.Selection([
        ("FederalGovernmentDepartment", "FederalGovernmentDepartment"),
        ("StateOrLocalGovernmentName", "StateOrLocalGovernmentName"),
        ("TribalGovernmentName", "TribalGovernmentName"),
        ("ForeignDiplomat", "ForeignDiplomat"),
        ("CharitableOrganization", "CharitableOrganization"),
        ("EducationalOrganization", "EducationalOrganization"),
        ("Resale", "Resale"),
        ("AgriculturalProduction", "AgriculturalProduction"),
        ("IndustrialProductionOrManufacturing", "IndustrialProductionOrManufacturing"),
        ("DirectPayPermit", "DirectPayPermit"),
        ("DirectMail", "DirectMail"),
        ("Other", "Other"),
        ("ReligiousOrganization", "ReligiousOrganization")], string="PurchaserExemptionReason")
    purchaser_exemption_reason_other_value = fields.Char("PurchaserExemptionReasonOtherValue")
    purchaser_first_name = fields.Char("PurchaserFirstName")
    purchaser_last_name = fields.Char("PurchaserLastName")
    purchaser_state = fields.Char("PurchaserState")
    purchaser_title = fields.Char("PurchaserTitle")
    purchaser_zip = fields.Char("PurchaserZip")
    id_number = fields.Char("IDNumber")
    state_of_issue_id = fields.Many2one("res.country.state", "State Of Issue")
    tax_type = fields.Selection([('SSN', 'SSN'), ('FEIN', 'FEIN'),
                                 ('StateIssued', 'StateIssued'),
                                 ('ForeignDiplomat', 'ForeignDiplomat')],
                                string="Tax Type")
    account_tax_certificate_id = fields.Many2one("account.tax.certificate",
                                                 string="Account Tax certificate")
