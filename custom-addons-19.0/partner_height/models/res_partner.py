# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    height = fields.Float(
        string='Height (cm)',
        help='Height of the contact in centimeters',
        tracking=True,
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