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

    height = fields.Float(
        string='Height (cm)',
        help='Height of the contact in centimeters',
        tracking=True,
    )

    weight = fields.Float(
        string='Weight (kg)',
        help='Weight of the contact in kilograms',
        tracking=True,
    )

    eye_color = fields.Selection([
        ('brown', 'Brown'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('hazel', 'Hazel'),
        ('gray', 'Gray'),
        ('amber', 'Amber'),
        ('other', 'Other'),
    ], string='Eye Color', help='Eye color of the contact', tracking=True)

    hair_color = fields.Selection([
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('blonde', 'Blonde'),
        ('red', 'Red'),
        ('gray', 'Gray'),
        ('white', 'White'),
        ('other', 'Other'),
    ], string='Hair Color', help='Hair color of the contact', tracking=True)

    distinguishing_features = fields.Text(
        string='Other Distinguishing Features',
        help='Other distinguishing physical features or characteristics',
        tracking=True,
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

    @api.constrains('height')
    def _check_height(self):
        """Validate height is within reasonable bounds"""
        for partner in self:
            if partner.height:
                if partner.height < 50 or partner.height > 250:
                    raise models.ValidationError(
                        "Height must be between 50 and 250 centimeters."
                    )

    @api.constrains('weight')
    def _check_weight(self):
        """Validate weight is within reasonable bounds"""
        for partner in self:
            if partner.weight:
                if partner.weight < 20 or partner.weight > 300:
                    raise models.ValidationError(
                        "Weight must be between 20 and 300 kilograms."
                    ) 