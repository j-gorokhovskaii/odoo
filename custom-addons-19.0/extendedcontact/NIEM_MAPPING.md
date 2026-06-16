# NIEM Mapping for ExtendedContact Module

This document maps the ExtendedContact module fields to NIEM (National Information Exchange Model) Core schema elements, ensuring compliance with government data exchange standards.

## Overview

The ExtendedContact module provides comprehensive person attributes that align with NIEM Core schema version 5.0, enabling seamless data exchange with government systems, law enforcement agencies, and other NIEM-compliant applications.

## Field Mappings

### Basic Information
| Odoo Field | NIEM Element | Description | Data Type |
|------------|--------------|-------------|-----------|
| `birthdate` | `nc:PersonBirthDate` | Date of birth | Date (ISO 8601) |
| `age` | `nc:PersonAgeMeasure` | Calculated age in years | Integer |
| `gender` | `nc:PersonSexCode` | Gender/sex identification | Selection |
| `marital_status` | `nc:PersonMaritalStatusText` | Marital status | Selection |

### Physical Characteristics
| Odoo Field | NIEM Element | Description | Data Type |
|------------|--------------|-------------|-----------|
| `height` | `nc:PersonHeightMeasure` | Height in centimeters | Float |
| `weight` | `nc:PersonWeightMeasure` | Weight in kilograms | Float |
| `build` | `nc:PersonBuildText` | Physical build/body type | Selection |
| `complexion` | `nc:PersonComplexionText` | Skin complexion | Selection |
| `eye_color` | `nc:PersonEyeColorText` | Eye color | Selection |
| `hair_color` | `nc:PersonHairColorText` | Hair color | Selection |
| `hair_style` | `nc:PersonHairStyleText` | Hair style/length | Selection |
| `blood_type` | `nc:PersonBloodTypeText` | Blood type | Selection |
| `distinguishing_features` | `nc:PersonPhysicalFeatureText` | Other distinguishing features | Text |

### Demographics
| Odoo Field | NIEM Element | Description | Data Type |
|------------|--------------|-------------|-----------|
| `ethnicity` | `nc:PersonEthnicityText` | Ethnicity (Hispanic/Latino) | Selection |
| `race` | `nc:PersonRaceText` | Race identification | Selection |
| `primary_language` | `nc:PersonLanguageText` | Primary language spoken | Char |
| `country_of_birth` | `nc:PersonBirthLocation/nc:LocationCountryName` | Country of birth | Many2one |
| `citizenship_status` | `nc:PersonCitizenshipStatusText` | Citizenship status | Selection |

### Identification
| Odoo Field | NIEM Element | Description | Data Type |
|------------|--------------|-------------|-----------|
| `ssn` | `nc:PersonSSNIdentification` | Social Security Number | Char |
| `driver_license_number` | `nc:PersonDriverLicenseIdentification/nc:IdentificationID` | Driver license number | Char |
| `driver_license_state` | `nc:PersonDriverLicenseIdentification/nc:IdentificationJurisdictionText` | Driver license issuing state | Many2one |
| `passport_number` | `nc:PersonPassportIdentification/nc:IdentificationID` | Passport number | Char |
| `passport_country` | `nc:PersonPassportIdentification/nc:IdentificationJurisdictionText` | Passport issuing country | Many2one |

### Employment & Education
| Odoo Field | NIEM Element | Description | Data Type |
|------------|--------------|-------------|-----------|
| `occupation` | `nc:PersonOccupationText` | Occupation/profession | Char |
| `employer` | `nc:PersonEmployerText` | Current employer | Char |
| `education_level` | `nc:PersonEducationLevelText` | Highest education level | Selection |

### Military Service
| Odoo Field | NIEM Element | Description | Data Type |
|------------|--------------|-------------|-----------|
| `military_service` | `nc:PersonMilitaryServiceIndicator` | Has served in military | Boolean |
| `military_branch` | `nc:PersonMilitaryBranchText` | Military branch served | Selection |

### Medical Information
| Odoo Field | NIEM Element | Description | Data Type |
|------------|--------------|-------------|-----------|
| `medical_conditions` | `nc:PersonMedicalConditionText` | Medical conditions/allergies | Text |

### Emergency Contact
| Odoo Field | NIEM Element | Description | Data Type |
|------------|--------------|-------------|-----------|
| `emergency_contact_name` | `nc:PersonEmergencyContact/nc:PersonName` | Emergency contact name | Char |

| `emergency_contact_relationship` | `nc:PersonEmergencyContact/nc:PersonRelationshipText` | Relationship to emergency contact | Char |

## NIEM XML Export

The module includes a `to_niem_xml()` method that generates NIEM-compliant XML output:

```python
# Example usage
partner = self.env['res.partner'].browse(1)
niem_xml = partner.to_niem_xml()
```

### Sample XML Output
```xml
<?xml version="1.0" encoding="UTF-8"?>
<nc:Person xmlns:nc="http://release.niem.gov/niem/niem-core/5.0/">
    <nc:PersonName>
        <nc:PersonFullName>John Smith</nc:PersonFullName>
    </nc:PersonName>
    <nc:PersonBirthDate>1989-01-15</nc:PersonBirthDate>
    <nc:PersonAgeMeasure>35</nc:PersonAgeMeasure>
    <nc:PersonSexCode>male</nc:PersonSexCode>
    <nc:PersonHeightMeasure>
        <nc:LengthMeasureValue>180.5</nc:LengthMeasureValue>
        <nc:LengthUnitCode>CMT</nc:LengthUnitCode>
    </nc:PersonHeightMeasure>
    <nc:PersonWeightMeasure>
        <nc:WeightMeasureValue>85.2</nc:WeightMeasureValue>
        <nc:WeightUnitCode>KGM</nc:WeightUnitCode>
    </nc:PersonWeightMeasure>
    <nc:PersonEyeColorText>blue</nc:PersonEyeColorText>
    <nc:PersonHairColorText>brown</nc:PersonHairColorText>
    <nc:PersonHairStyleText>short</nc:PersonHairStyleText>
    <nc:PersonBuildText>athletic</nc:PersonBuildText>
    <nc:PersonComplexionText>medium</nc:PersonComplexionText>
    <nc:PersonPhysicalFeatureText>Small scar on left eyebrow</nc:PersonPhysicalFeatureText>
    <nc:PersonEthnicityText>not_hispanic</nc:PersonEthnicityText>
    <nc:PersonRaceText>white</nc:PersonRaceText>
    <nc:PersonBloodTypeText>o_positive</nc:PersonBloodTypeText>
    <nc:PersonMedicalConditionText>Mild seasonal allergies</nc:PersonMedicalConditionText>
    <nc:PersonLanguageText>English</nc:PersonLanguageText>
    <nc:PersonOccupationText>Software Engineer</nc:PersonOccupationText>
    <nc:PersonEmployerText>Tech Solutions Inc.</nc:PersonEmployerText>
    <nc:PersonEducationLevelText>bachelors</nc:PersonEducationLevelText>
    <nc:PersonMaritalStatusText>married</nc:PersonMaritalStatusText>
    <nc:PersonCitizenshipStatusText>citizen</nc:PersonCitizenshipStatusText>
    <nc:PersonSSNIdentification>123-45-6789</nc:PersonSSNIdentification>
    <nc:PersonDriverLicenseIdentification>
        <nc:IdentificationID>DL123456789</nc:IdentificationID>
        <nc:IdentificationJurisdictionText>California</nc:IdentificationJurisdictionText>
    </nc:PersonDriverLicenseIdentification>
    <nc:PersonPassportIdentification>
        <nc:IdentificationID></nc:IdentificationID>
        <nc:IdentificationJurisdictionText></nc:IdentificationJurisdictionText>
    </nc:PersonPassportIdentification>
    <nc:PersonMilitaryServiceIndicator>false</nc:PersonMilitaryServiceIndicator>
    <nc:PersonMilitaryBranchText></nc:PersonMilitaryBranchText>
    <nc:PersonBirthLocation>
        <nc:LocationCountryName>United States</nc:LocationCountryName>
    </nc:PersonBirthLocation>
    <nc:PersonEmergencyContact>
        <nc:PersonName>Jane Smith</nc:PersonName>
        <nc:PersonRelationshipText>Spouse</nc:PersonRelationshipText>
    </nc:PersonEmergencyContact>
</nc:Person>
```

## Validation Rules

The module includes NIEM-compliant validation:

- **Birth Date**: Must not be in the future (ISO 8601 compliance)
- **Height**: Must be between 50-250 cm (CMT unit code)
- **Weight**: Must be between 20-300 kg (KGM unit code)
- **SSN**: Must follow XXX-XX-XXXX format
- **Age**: Automatically calculated from birth date

## Government Integration Benefits

This NIEM-compliant implementation provides:

1. **Standardized Data Exchange**: Compatible with federal, state, and local government systems
2. **Law Enforcement Integration**: Supports criminal justice information systems (CJIS)
3. **Healthcare Interoperability**: Aligns with health information exchange standards
4. **Emergency Response**: Compatible with emergency management systems
5. **Immigration Services**: Supports immigration and border control systems
6. **Social Services**: Compatible with human services and welfare systems

## Compliance Notes

- All field names and data types align with NIEM Core schema 5.0
- XML output follows NIEM namespace conventions
- Validation rules ensure data quality and consistency
- Demo data provides realistic examples for testing
- Search and filter capabilities support efficient data retrieval

## References

- [NIEM Core Schema 5.0](https://release.niem.gov/niem/niem-core/5.0/)
- [NIEM Technical Architecture](https://www.niem.gov/technical-architecture)
- [NIEM Implementation Guide](https://www.niem.gov/implementation-guide) 