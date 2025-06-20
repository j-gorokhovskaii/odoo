# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthdate = fields.Date(
        string='Date of Birth',
        help='Birth date of the contact',
        tracking=True,
    )
    
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=False,
        help='Age calculated from birth date',
    )

    @api.depends('birthdate')
    def _compute_age(self):
        """Compute age based on birthdate"""
        today = date.today()
        for partner in self:
            if partner.birthdate:
                age = today.year - partner.birthdate.year
                # Adjust age if birthday hasn't occurred this year
                if today.month < partner.birthdate.month or (
                    today.month == partner.birthdate.month and 
                    today.day < partner.birthdate.day
                ):
                    age -= 1
                partner.age = age
            else:
                partner.age = 0

    @api.constrains('birthdate')
    def _check_birthdate(self):
        """Validate birthdate is not in the future"""
        today = date.today()
        for partner in self:
            if partner.birthdate and partner.birthdate > today:
                raise models.ValidationError(
                    "Birth date cannot be in the future."
                ) 