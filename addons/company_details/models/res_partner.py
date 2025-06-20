from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import re


class ResPartner(models.Model):
    """
    Extended Partner model with comprehensive company information.
    
    This model extends the standard res.partner model to include detailed company
    information fields that are NIEM-compliant and suitable for government integration.
    
    NIEM Mapping:
    - Company Registration: nc:Organization/nc:OrganizationIdentification
    - Tax Information: nc:Organization/nc:OrganizationTaxIdentification
    - Business Classification: nc:Organization/nc:OrganizationCategory
    - Financial Information: nc:Organization/nc:OrganizationFinancialInformation
    - Compliance Information: nc:Organization/nc:OrganizationComplianceInformation
    """
    _inherit = 'res.partner'

    # Company Registration Information
    company_registration_number = fields.Char(
        string='Company Registration Number',
        help='Official company registration number issued by regulatory authority',
        size=50
    )
    company_registration_date = fields.Date(
        string='Registration Date',
        help='Date when company was officially registered'
    )
    company_registration_authority = fields.Char(
        string='Registration Authority',
        help='Government authority that issued the registration',
        size=100
    )
    
    # Tax Information
    company_tax_id = fields.Char(
        string='Company Tax ID',
        help='Company tax identification number',
        size=50
    )
    company_vat_number = fields.Char(
        string='Company VAT Number',
        help='Value Added Tax registration number',
        size=50
    )
    company_tax_registration_date = fields.Date(
        string='Tax Registration Date',
        help='Date when company was registered for tax purposes'
    )
    
    # Business Classification
    company_industry = fields.Selection([
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance & Banking'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail & E-commerce'),
        ('construction', 'Construction'),
        ('education', 'Education'),
        ('government', 'Government'),
        ('non_profit', 'Non-Profit'),
        ('consulting', 'Consulting'),
        ('real_estate', 'Real Estate'),
        ('transportation', 'Transportation & Logistics'),
        ('energy', 'Energy & Utilities'),
        ('media', 'Media & Entertainment'),
        ('food_beverage', 'Food & Beverage'),
        ('automotive', 'Automotive'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('telecommunications', 'Telecommunications'),
        ('other', 'Other')
    ], string='Company Industry', help='Primary industry sector')
    
    company_business_type = fields.Selection([
        ('corporation', 'Corporation'),
        ('llc', 'Limited Liability Company (LLC)'),
        ('partnership', 'Partnership'),
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('non_profit', 'Non-Profit Organization'),
        ('government', 'Government Entity'),
        ('subsidiary', 'Subsidiary'),
        ('branch', 'Branch Office'),
        ('franchise', 'Franchise'),
        ('cooperative', 'Cooperative'),
        ('other', 'Other')
    ], string='Business Type', help='Legal structure of the business')
    
    company_size = fields.Selection([
        ('micro', 'Micro (1-10 employees)'),
        ('small', 'Small (11-50 employees)'),
        ('medium', 'Medium (51-250 employees)'),
        ('large', 'Large (251-1000 employees)'),
        ('enterprise', 'Enterprise (1000+ employees)')
    ], string='Company Size', help='Number of employees')
    
    # Financial Information
    company_annual_revenue = fields.Selection([
        ('under_1m', 'Under $1 Million'),
        ('1m_10m', '$1 Million - $10 Million'),
        ('10m_50m', '$10 Million - $50 Million'),
        ('50m_100m', '$50 Million - $100 Million'),
        ('100m_500m', '$100 Million - $500 Million'),
        ('500m_1b', '$500 Million - $1 Billion'),
        ('over_1b', 'Over $1 Billion'),
        ('not_disclosed', 'Not Disclosed')
    ], string='Annual Revenue', help='Annual revenue range')
    
    company_employee_count = fields.Integer(
        string='Employee Count',
        help='Total number of employees'
    )
    
    company_credit_rating = fields.Selection([
        ('aaa', 'AAA - Excellent'),
        ('aa', 'AA - Very Good'),
        ('a', 'A - Good'),
        ('bbb', 'BBB - Average'),
        ('bb', 'BB - Below Average'),
        ('b', 'B - Poor'),
        ('ccc', 'CCC - Very Poor'),
        ('cc', 'CC - Extremely Poor'),
        ('c', 'C - Default'),
        ('d', 'D - In Default'),
        ('not_rated', 'Not Rated')
    ], string='Credit Rating', help='Company credit rating')
    
    # Compliance Information
    company_iso_certifications = fields.Many2many(
        'company.iso.certification',
        string='ISO Certifications',
        help='ISO certifications held by the company'
    )
    
    company_industry_certifications = fields.Text(
        string='Industry Certifications',
        help='Industry-specific certifications and licenses'
    )
    
    company_compliance_status = fields.Selection([
        ('compliant', 'Fully Compliant'),
        ('partially_compliant', 'Partially Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending_review', 'Pending Review'),
        ('exempt', 'Exempt'),
        ('unknown', 'Unknown')
    ], string='Compliance Status', help='Overall compliance status')
    
    # Legal Information
    company_legal_structure = fields.Char(
        string='Legal Structure',
        help='Detailed legal structure description',
        size=100
    )
    
    company_incorporation_date = fields.Date(
        string='Incorporation Date',
        help='Date when company was incorporated'
    )
    
    company_legal_representative = fields.Char(
        string='Legal Representative',
        help='Name of legal representative or authorized signatory',
        size=100
    )
    
    company_legal_representative_title = fields.Char(
        string='Legal Representative Title',
        help='Title or position of legal representative',
        size=100
    )
    
    # Additional Company Information
    company_website = fields.Char(
        string='Company Website',
        help='Official company website URL'
    )
    
    company_linkedin = fields.Char(
        string='LinkedIn Profile',
        help='Company LinkedIn profile URL'
    )
    
    company_facebook = fields.Char(
        string='Facebook Page',
        help='Company Facebook page URL'
    )
    
    company_twitter = fields.Char(
        string='Twitter Handle',
        help='Company Twitter handle'
    )
    
    company_instagram = fields.Char(
        string='Instagram Profile',
        help='Company Instagram profile URL'
    )
    
    # Computed Fields
    company_age_years = fields.Integer(
        string='Company Age (Years)',
        compute='_compute_company_age',
        store=False,
        help='Number of years since company registration'
    )
    
    company_age_months = fields.Integer(
        string='Company Age (Months)',
        compute='_compute_company_age',
        store=False,
        help='Number of months since company registration'
    )
    
    company_age_days = fields.Integer(
        string='Company Age (Days)',
        compute='_compute_company_age',
        store=False,
        help='Number of days since company registration'
    )
    
    company_age_hours = fields.Integer(
        string='Company Age (Hours)',
        compute='_compute_company_age',
        store=False,
        help='Number of hours since company registration'
    )
    
    company_next_anniversary_days = fields.Integer(
        string='Days to Next Anniversary',
        compute='_compute_company_age',
        store=False,
        help='Days until next company anniversary'
    )

    @api.depends('company_registration_date')
    def _compute_company_age(self):
        """Compute detailed company age based on registration date."""
        today = datetime.now()
        
        for partner in self:
            if partner.company_registration_date:
                registration_date = datetime.combine(partner.company_registration_date, datetime.min.time())
                
                # Calculate time difference
                time_diff = today - registration_date
                
                # Calculate years, months, days
                years = today.year - registration_date.year
                months = today.month - registration_date.month
                days = today.day - registration_date.day
                
                # Adjust for negative months/days
                if days < 0:
                    months -= 1
                    # Get days in previous month
                    if today.month == 1:
                        prev_month = 12
                        prev_year = today.year - 1
                    else:
                        prev_month = today.month - 1
                        prev_year = today.year
                    days_in_prev_month = (datetime(prev_year, prev_month + 1, 1) - datetime(prev_year, prev_month, 1)).days
                    days += days_in_prev_month
                
                if months < 0:
                    years -= 1
                    months += 12
                
                # Calculate hours
                hours = int(time_diff.total_seconds() / 3600)
                
                # Calculate days to next anniversary
                next_anniversary = datetime(today.year, registration_date.month, registration_date.day)
                if next_anniversary < today:
                    next_anniversary = datetime(today.year + 1, registration_date.month, registration_date.day)
                
                days_to_anniversary = (next_anniversary - today).days
                
                partner.company_age_years = years
                partner.company_age_months = months
                partner.company_age_days = days
                partner.company_age_hours = hours
                partner.company_next_anniversary_days = days_to_anniversary
            else:
                partner.company_age_years = 0
                partner.company_age_months = 0
                partner.company_age_days = 0
                partner.company_age_hours = 0
                partner.company_next_anniversary_days = 0

    @api.constrains('company_registration_date', 'company_incorporation_date')
    def _check_dates(self):
        """Validate that dates are not in the future."""
        today = date.today()
        
        for partner in self:
            if partner.company_registration_date and partner.company_registration_date > today:
                raise ValidationError(_('Company registration date cannot be in the future.'))
            
            if partner.company_incorporation_date and partner.company_incorporation_date > today:
                raise ValidationError(_('Company incorporation date cannot be in the future.'))

    @api.constrains('company_employee_count')
    def _check_employee_count(self):
        """Validate employee count is positive."""
        for partner in self:
            if partner.company_employee_count and partner.company_employee_count < 0:
                raise ValidationError(_('Employee count must be a positive number.'))

    @api.constrains('company_registration_number')
    def _check_registration_number(self):
        """Validate registration number format."""
        for partner in self:
            if partner.company_registration_number:
                # Remove spaces and common separators for validation
                clean_number = re.sub(r'[\s\-_\.]', '', partner.company_registration_number)
                if not clean_number.isalnum():
                    raise ValidationError(_('Registration number can only contain letters, numbers, spaces, hyphens, underscores, and periods.'))

    def export_as_niem_xml(self):
        """
        Export company data in NIEM-compliant XML format.
        
        Returns:
            str: NIEM-compliant XML string containing company information
        """
        xml_parts = []
        xml_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
        xml_parts.append('<nc:Organization xmlns:nc="http://release.niem.gov/niem/niem-core/5.0/">')
        
        # Basic organization information
        if self.name:
            xml_parts.append(f'  <nc:OrganizationName>{self.name}</nc:OrganizationName>')
        
        # Organization identification (registration information)
        if self.company_registration_number or self.company_registration_date or self.company_registration_authority:
            xml_parts.append('  <nc:OrganizationIdentification>')
            if self.company_registration_number:
                xml_parts.append(f'    <nc:IdentificationID>{self.company_registration_number}</nc:IdentificationID>')
            if self.company_registration_date:
                xml_parts.append(f'    <nc:IdentificationIssuerDate>{self.company_registration_date}</nc:IdentificationIssuerDate>')
            if self.company_registration_authority:
                xml_parts.append(f'    <nc:IdentificationIssuerName>{self.company_registration_authority}</nc:IdentificationIssuerName>')
            xml_parts.append('  </nc:OrganizationIdentification>')
        
        # Tax identification
        if self.company_tax_id or self.company_vat_number:
            xml_parts.append('  <nc:OrganizationTaxIdentification>')
            if self.company_tax_id:
                xml_parts.append(f'    <nc:TaxIdentificationID>{self.company_tax_id}</nc:TaxIdentificationID>')
            if self.company_vat_number:
                xml_parts.append(f'    <nc:VATIdentificationID>{self.company_vat_number}</nc:VATIdentificationID>')
            xml_parts.append('  </nc:OrganizationTaxIdentification>')
        
        # Organization category (business classification)
        if self.company_industry or self.company_business_type or self.company_size:
            xml_parts.append('  <nc:OrganizationCategory>')
            if self.company_industry:
                xml_parts.append(f'    <nc:CategoryText>{self.company_industry}</nc:CategoryText>')
            if self.company_business_type:
                xml_parts.append(f'    <nc:BusinessTypeText>{self.company_business_type}</nc:BusinessTypeText>')
            if self.company_size:
                xml_parts.append(f'    <nc:OrganizationSizeText>{self.company_size}</nc:OrganizationSizeText>')
            xml_parts.append('  </nc:OrganizationCategory>')
        
        # Financial information
        if self.company_annual_revenue or self.company_employee_count or self.company_credit_rating:
            xml_parts.append('  <nc:OrganizationFinancialInformation>')
            if self.company_annual_revenue:
                xml_parts.append(f'    <nc:AnnualRevenueText>{self.company_annual_revenue}</nc:AnnualRevenueText>')
            if self.company_employee_count:
                xml_parts.append(f'    <nc:EmployeeCountNumeric>{self.company_employee_count}</nc:EmployeeCountNumeric>')
            if self.company_credit_rating:
                xml_parts.append(f'    <nc:CreditRatingText>{self.company_credit_rating}</nc:CreditRatingText>')
            xml_parts.append('  </nc:OrganizationFinancialInformation>')
        
        # Compliance information
        if self.company_iso_certifications or self.company_industry_certifications or self.company_compliance_status:
            xml_parts.append('  <nc:OrganizationComplianceInformation>')
            if self.company_iso_certifications:
                cert_names = ', '.join([cert.name for cert in self.company_iso_certifications])
                xml_parts.append(f'    <nc:ISOCertificationText>{cert_names}</nc:ISOCertificationText>')
            if self.company_industry_certifications:
                xml_parts.append(f'    <nc:IndustryCertificationText>{self.company_industry_certifications}</nc:IndustryCertificationText>')
            if self.company_compliance_status:
                xml_parts.append(f'    <nc:ComplianceStatusText>{self.company_compliance_status}</nc:ComplianceStatusText>')
            xml_parts.append('  </nc:OrganizationComplianceInformation>')
        
        xml_parts.append('</nc:Organization>')
        
        return '\n'.join(xml_parts)


class CompanyISOCertification(models.Model):
    """
    ISO Certification model for company certifications.
    
    This model stores ISO certifications that companies can hold.
    """
    _name = 'company.iso.certification'
    _description = 'ISO Certification'
    _order = 'name'

    name = fields.Char(
        string='Certification Name',
        required=True,
        help='Name of the ISO certification (e.g., ISO 9001, ISO 14001)'
    )
    
    code = fields.Char(
        string='Certification Code',
        help='ISO certification code'
    )
    
    description = fields.Text(
        string='Description',
        help='Detailed description of the certification'
    )
    
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this certification is currently active'
    )
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Certification name must be unique!')
    ] 