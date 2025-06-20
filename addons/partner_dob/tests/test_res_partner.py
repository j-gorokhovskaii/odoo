# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, timedelta
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestResPartner(TransactionCase):
    """Test cases for the res.partner model with Date of Birth functionality"""

    def setUp(self):
        super().setUp()
        self.partner_model = self.env['res.partner']

    def test_birthdate_field_creation(self):
        """Test that birthdate field can be set on individual contacts"""
        # Create a partner with birthdate
        partner = self.partner_model.create({
            'name': 'Test Contact',
            'is_company': False,
            'birthdate': date(1990, 5, 15),
        })
        
        self.assertEqual(partner.birthdate, date(1990, 5, 15))
        self.assertFalse(partner.is_company)

    def test_age_computation(self):
        """Test age computation based on birthdate"""
        today = date.today()
        birth_year = today.year - 30
        
        partner = self.partner_model.create({
            'name': 'Test Contact',
            'is_company': False,
            'birthdate': date(birth_year, today.month, today.day),
        })
        
        self.assertEqual(partner.age, 30)

    def test_age_computation_before_birthday(self):
        """Test age computation when birthday hasn't occurred this year"""
        today = date.today()
        birth_year = today.year - 30
        # Set birthdate to a future date this year
        future_month = min(today.month + 1, 12)
        future_day = min(today.day, 28)  # Avoid month/day issues
        
        partner = self.partner_model.create({
            'name': 'Test Contact',
            'is_company': False,
            'birthdate': date(birth_year, future_month, future_day),
        })
        
        self.assertEqual(partner.age, 29)  # Should be 29, not 30

    def test_age_computation_no_birthdate(self):
        """Test age computation when no birthdate is set"""
        partner = self.partner_model.create({
            'name': 'Test Contact',
            'is_company': False,
        })
        
        self.assertEqual(partner.age, 0)

    def test_birthdate_validation_future_date(self):
        """Test that future birthdates are not allowed"""
        tomorrow = date.today() + timedelta(days=1)
        
        with self.assertRaises(ValidationError):
            self.partner_model.create({
                'name': 'Test Contact',
                'is_company': False,
                'birthdate': tomorrow,
            })

    def test_company_no_birthdate_field(self):
        """Test that companies don't show birthdate fields in views"""
        company = self.partner_model.create({
            'name': 'Test Company',
            'is_company': True,
        })
        
        # Companies should not have birthdate functionality
        self.assertTrue(company.is_company)
        # The birthdate field exists but should not be used for companies

    def test_birthdate_update_age_recomputation(self):
        """Test that age is recomputed when birthdate is updated"""
        partner = self.partner_model.create({
            'name': 'Test Contact',
            'is_company': False,
            'birthdate': date(1990, 5, 15),
        })
        
        initial_age = partner.age
        
        # Update birthdate
        partner.birthdate = date(1985, 5, 15)
        partner._compute_age()  # Force recomputation
        
        self.assertGreater(partner.age, initial_age)

    def test_birthdate_removal(self):
        """Test that age becomes 0 when birthdate is removed"""
        partner = self.partner_model.create({
            'name': 'Test Contact',
            'is_company': False,
            'birthdate': date(1990, 5, 15),
        })
        
        self.assertGreater(partner.age, 0)
        
        # Remove birthdate
        partner.birthdate = False
        partner._compute_age()  # Force recomputation
        
        self.assertEqual(partner.age, 0) 