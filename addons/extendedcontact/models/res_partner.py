# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # NIEM Core Person Elements - Basic Information
    birthdate = fields.Date(
        string='Date of Birth',
        help='Birth date of the contact (NIEM: nc:PersonBirthDate)',
        tracking=True,
    )
    
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=False,
        help='Age calculated from birth date (NIEM: nc:PersonAgeMeasure)',
    )

    # NIEM Core Person Elements - Physical Characteristics
    height = fields.Float(
        string='Height (cm)',
        help='Height of the contact in centimeters (NIEM: nc:PersonHeightMeasure)',
        tracking=True,
    )

    weight = fields.Float(
        string='Weight (kg)',
        help='Weight of the contact in kilograms (NIEM: nc:PersonWeightMeasure)',
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
    ], string='Eye Color', help='Eye color of the contact (NIEM: nc:PersonEyeColorText)', tracking=True)

    hair_color = fields.Selection([
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('blonde', 'Blonde'),
        ('red', 'Red'),
        ('gray', 'Gray'),
        ('white', 'White'),
        ('other', 'Other'),
    ], string='Hair Color', help='Hair color of the contact (NIEM: nc:PersonHairColorText)', tracking=True)

    hair_style = fields.Selection([
        ('short', 'Short'),
        ('medium', 'Medium'),
        ('long', 'Long'),
        ('bald', 'Bald'),
        ('shaved', 'Shaved'),
        ('other', 'Other'),
    ], string='Hair Style', help='Hair style of the contact (NIEM: nc:PersonHairStyleText)', tracking=True)

    distinguishing_features = fields.Text(
        string='Other Distinguishing Features',
        help='Other distinguishing physical features or characteristics (NIEM: nc:PersonPhysicalFeatureText)',
        tracking=True,
    )

    # NIEM Core Person Elements - Demographics
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unknown', 'Unknown'),
    ], string='Gender', help='Gender of the contact (NIEM: nc:PersonSexCode)', tracking=True)

    ethnicity = fields.Selection([
        ('hispanic', 'Hispanic or Latino'),
        ('not_hispanic', 'Not Hispanic or Latino'),
        ('unknown', 'Unknown'),
    ], string='Ethnicity', help='Ethnicity of the contact (NIEM: nc:PersonEthnicityText)', tracking=True)

    race = fields.Selection([
        ('white', 'White'),
        ('black', 'Black or African American'),
        ('asian', 'Asian'),
        ('native_american', 'American Indian or Alaska Native'),
        ('pacific_islander', 'Native Hawaiian or Other Pacific Islander'),
        ('other', 'Other'),
        ('unknown', 'Unknown'),
    ], string='Race', help='Race of the contact (NIEM: nc:PersonRaceText)', tracking=True)

    # NIEM Core Person Elements - Identification
    ssn = fields.Char(
        string='Social Security Number',
        help='Social Security Number (NIEM: nc:PersonSSNIdentification)',
        tracking=True,
    )

    driver_license_number = fields.Char(
        string='Driver License Number',
        help='Driver License Number (NIEM: nc:PersonDriverLicenseIdentification)',
        tracking=True,
    )

    driver_license_state = fields.Many2one(
        'res.country.state',
        string='Driver License State',
        help='State that issued the driver license (NIEM: nc:PersonDriverLicenseIdentification/nc:IdentificationJurisdictionText)',
        tracking=True,
    )

    passport_number = fields.Char(
        string='Passport Number',
        help='Passport Number (NIEM: nc:PersonPassportIdentification)',
        tracking=True,
    )

    passport_country = fields.Many2one(
        'res.country',
        string='Passport Country',
        help='Country that issued the passport (NIEM: nc:PersonPassportIdentification/nc:IdentificationJurisdictionText)',
        tracking=True,
    )

    # NIEM Core Person Elements - Physical Details
    build = fields.Selection([
        ('slim', 'Slim'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('athletic', 'Athletic'),
        ('other', 'Other'),
    ], string='Build', help='Physical build of the contact (NIEM: nc:PersonBuildText)', tracking=True)

    complexion = fields.Selection([
        ('fair', 'Fair'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('dark', 'Dark'),
        ('other', 'Other'),
    ], string='Complexion', help='Complexion of the contact (NIEM: nc:PersonComplexionText)', tracking=True)

    # NIEM Core Person Elements - Medical/Physical
    blood_type = fields.Selection([
        ('a_positive', 'A+'),
        ('a_negative', 'A-'),
        ('b_positive', 'B+'),
        ('b_negative', 'B-'),
        ('ab_positive', 'AB+'),
        ('ab_negative', 'AB-'),
        ('o_positive', 'O+'),
        ('o_negative', 'O-'),
        ('unknown', 'Unknown'),
    ], string='Blood Type', help='Blood type of the contact (NIEM: nc:PersonBloodTypeText)', tracking=True)

    medical_conditions = fields.Text(
        string='Medical Conditions',
        help='Medical conditions or allergies (NIEM: nc:PersonMedicalConditionText)',
        tracking=True,
    )

    # NIEM Core Person Elements - Language
    primary_language = fields.Char(
        string='Primary Language',
        help='Primary language spoken (NIEM: nc:PersonLanguageText)',
        tracking=True,
    )

    # NIEM Core Person Elements - Employment
    occupation = fields.Char(
        string='Occupation',
        help='Occupation or profession (NIEM: nc:PersonOccupationText)',
        tracking=True,
    )

    employer = fields.Char(
        string='Employer',
        help='Current employer (NIEM: nc:PersonEmployerText)',
        tracking=True,
    )

    # NIEM Core Person Elements - Education
    education_level = fields.Selection([
        ('none', 'No Formal Education'),
        ('elementary', 'Elementary School'),
        ('high_school', 'High School'),
        ('some_college', 'Some College'),
        ('associates', 'Associate Degree'),
        ('bachelors', 'Bachelor Degree'),
        ('masters', 'Master Degree'),
        ('doctorate', 'Doctorate'),
        ('other', 'Other'),
    ], string='Education Level', help='Highest education level (NIEM: nc:PersonEducationLevelText)', tracking=True)

    # NIEM Core Person Elements - Military
    military_service = fields.Boolean(
        string='Military Service',
        help='Has served in military (NIEM: nc:PersonMilitaryServiceIndicator)',
        tracking=True,
    )

    military_branch = fields.Selection([
        ('army', 'Army'),
        ('navy', 'Navy'),
        ('air_force', 'Air Force'),
        ('marines', 'Marines'),
        ('coast_guard', 'Coast Guard'),
        ('other', 'Other'),
    ], string='Military Branch', help='Military branch served in (NIEM: nc:PersonMilitaryBranchText)', tracking=True)

    # NIEM Core Person Elements - Citizenship
    citizenship_status = fields.Selection([
        ('citizen', 'U.S. Citizen'),
        ('permanent_resident', 'Permanent Resident'),
        ('visa_holder', 'Visa Holder'),
        ('undocumented', 'Undocumented'),
        ('other', 'Other'),
    ], string='Citizenship Status', help='Citizenship status (NIEM: nc:PersonCitizenshipStatusText)', tracking=True)

    country_of_birth = fields.Many2one(
        'res.country',
        string='Country of Birth',
        help='Country where person was born (NIEM: nc:PersonBirthLocation/nc:LocationCountryName)',
        tracking=True,
    )

    # NIEM Core Person Elements - Marital Status
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('other', 'Other'),
    ], string='Marital Status', help='Marital status (NIEM: nc:PersonMaritalStatusText)', tracking=True)

    # NIEM Core Person Elements - Emergency Contact
    emergency_contact_name = fields.Char(
        string='Emergency Contact Name',
        help='Name of emergency contact (NIEM: nc:PersonEmergencyContact/nc:PersonName)',
        tracking=True,
    )

    emergency_contact_phone = fields.Char(
        string='Emergency Contact Phone',
        help='Phone number of emergency contact (NIEM: nc:PersonEmergencyContact/nc:ContactTelephoneNumber)',
        tracking=True,
    )

    emergency_contact_relationship = fields.Char(
        string='Emergency Contact Relationship',
        help='Relationship to emergency contact (NIEM: nc:PersonEmergencyContact/nc:PersonRelationshipText)',
        tracking=True,
    )

    @api.depends('birthdate')
    def _compute_age(self):
        """
        Compute age based on birthdate
        NIEM Element: nc:PersonAgeMeasure
        Calculates age in years based on current date and birth date
        """
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
        """
        Validate birthdate is not in the future
        NIEM Element: nc:PersonBirthDate
        Ensures birth date follows ISO 8601 standard and is not in the future
        """
        today = date.today()
        for partner in self:
            if partner.birthdate and partner.birthdate > today:
                raise models.ValidationError(
                    "Birth date cannot be in the future."
                )

    @api.constrains('height')
    def _check_height(self):
        """
        Validate height is within reasonable bounds
        NIEM Element: nc:PersonHeightMeasure
        Validates height in centimeters (CMT unit code)
        """
        for partner in self:
            if partner.height:
                if partner.height < 50 or partner.height > 250:
                    raise models.ValidationError(
                        "Height must be between 50 and 250 centimeters."
                    )

    @api.constrains('weight')
    def _check_weight(self):
        """
        Validate weight is within reasonable bounds
        NIEM Element: nc:PersonWeightMeasure
        Validates weight in kilograms (KGM unit code)
        """
        for partner in self:
            if partner.weight:
                if partner.weight < 20 or partner.weight > 300:
                    raise models.ValidationError(
                        "Weight must be between 20 and 300 kilograms."
                    )

    @api.constrains('ssn')
    def _check_ssn(self):
        """
        Validate SSN format
        NIEM Element: nc:PersonSSNIdentification
        Validates Social Security Number format (XXX-XX-XXXX)
        """
        for partner in self:
            if partner.ssn:
                import re
                ssn_pattern = r'^\d{3}-\d{2}-\d{4}$'
                if not re.match(ssn_pattern, partner.ssn):
                    raise models.ValidationError(
                        "Social Security Number must be in format XXX-XX-XXXX"
                    )

    def to_niem_xml(self):
        """
        Convert partner data to NIEM-compliant XML format
        Returns XML string following NIEM Core schema
        """
        xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<nc:Person xmlns:nc="http://release.niem.gov/niem/niem-core/5.0/">
    <nc:PersonName>
        <nc:PersonFullName>{name}</nc:PersonFullName>
    </nc:PersonName>
    <nc:PersonBirthDate>{birthdate}</nc:PersonBirthDate>
    <nc:PersonAgeMeasure>{age}</nc:PersonAgeMeasure>
    <nc:PersonSexCode>{gender}</nc:PersonSexCode>
    <nc:PersonHeightMeasure>
        <nc:LengthMeasureValue>{height}</nc:LengthMeasureValue>
        <nc:LengthUnitCode>CMT</nc:LengthUnitCode>
    </nc:PersonHeightMeasure>
    <nc:PersonWeightMeasure>
        <nc:WeightMeasureValue>{weight}</nc:WeightMeasureValue>
        <nc:WeightUnitCode>KGM</nc:WeightUnitCode>
    </nc:PersonWeightMeasure>
    <nc:PersonEyeColorText>{eye_color}</nc:PersonEyeColorText>
    <nc:PersonHairColorText>{hair_color}</nc:PersonHairColorText>
    <nc:PersonHairStyleText>{hair_style}</nc:PersonHairStyleText>
    <nc:PersonBuildText>{build}</nc:PersonBuildText>
    <nc:PersonComplexionText>{complexion}</nc:PersonComplexionText>
    <nc:PersonPhysicalFeatureText>{distinguishing_features}</nc:PersonPhysicalFeatureText>
    <nc:PersonEthnicityText>{ethnicity}</nc:PersonEthnicityText>
    <nc:PersonRaceText>{race}</nc:PersonRaceText>
    <nc:PersonBloodTypeText>{blood_type}</nc:PersonBloodTypeText>
    <nc:PersonMedicalConditionText>{medical_conditions}</nc:PersonMedicalConditionText>
    <nc:PersonLanguageText>{primary_language}</nc:PersonLanguageText>
    <nc:PersonOccupationText>{occupation}</nc:PersonOccupationText>
    <nc:PersonEmployerText>{employer}</nc:PersonEmployerText>
    <nc:PersonEducationLevelText>{education_level}</nc:PersonEducationLevelText>
    <nc:PersonMaritalStatusText>{marital_status}</nc:PersonMaritalStatusText>
    <nc:PersonCitizenshipStatusText>{citizenship_status}</nc:PersonCitizenshipStatusText>
    <nc:PersonSSNIdentification>{ssn}</nc:PersonSSNIdentification>
    <nc:PersonDriverLicenseIdentification>
        <nc:IdentificationID>{driver_license_number}</nc:IdentificationID>
        <nc:IdentificationJurisdictionText>{driver_license_state}</nc:IdentificationJurisdictionText>
    </nc:PersonDriverLicenseIdentification>
    <nc:PersonPassportIdentification>
        <nc:IdentificationID>{passport_number}</nc:IdentificationID>
        <nc:IdentificationJurisdictionText>{passport_country}</nc:IdentificationJurisdictionText>
    </nc:PersonPassportIdentification>
    <nc:PersonMilitaryServiceIndicator>{military_service}</nc:PersonMilitaryServiceIndicator>
    <nc:PersonMilitaryBranchText>{military_branch}</nc:PersonMilitaryBranchText>
    <nc:PersonBirthLocation>
        <nc:LocationCountryName>{country_of_birth}</nc:LocationCountryName>
    </nc:PersonBirthLocation>
    <nc:PersonEmergencyContact>
        <nc:PersonName>{emergency_contact_name}</nc:PersonName>
        <nc:ContactTelephoneNumber>{emergency_contact_phone}</nc:ContactTelephoneNumber>
        <nc:PersonRelationshipText>{emergency_contact_relationship}</nc:PersonRelationshipText>
    </nc:PersonEmergencyContact>
</nc:Person>"""
        
        return xml_template.format(
            name=self.name or '',
            birthdate=self.birthdate.strftime('%Y-%m-%d') if self.birthdate else '',
            age=self.age or 0,
            gender=self.gender or '',
            height=self.height or '',
            weight=self.weight or '',
            eye_color=self.eye_color or '',
            hair_color=self.hair_color or '',
            hair_style=self.hair_style or '',
            build=self.build or '',
            complexion=self.complexion or '',
            distinguishing_features=self.distinguishing_features or '',
            ethnicity=self.ethnicity or '',
            race=self.race or '',
            blood_type=self.blood_type or '',
            medical_conditions=self.medical_conditions or '',
            primary_language=self.primary_language or '',
            occupation=self.occupation or '',
            employer=self.employer or '',
            education_level=self.education_level or '',
            marital_status=self.marital_status or '',
            citizenship_status=self.citizenship_status or '',
            ssn=self.ssn or '',
            driver_license_number=self.driver_license_number or '',
            driver_license_state=self.driver_license_state.name if self.driver_license_state else '',
            passport_number=self.passport_number or '',
            passport_country=self.passport_country.name if self.passport_country else '',
            military_service=str(self.military_service).lower() if self.military_service else 'false',
            military_branch=self.military_branch or '',
            country_of_birth=self.country_of_birth.name if self.country_of_birth else '',
            emergency_contact_name=self.emergency_contact_name or '',
            emergency_contact_phone=self.emergency_contact_phone or '',
            emergency_contact_relationship=self.emergency_contact_relationship or ''
        ) 