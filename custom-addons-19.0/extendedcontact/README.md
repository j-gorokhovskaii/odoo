# ExtendedContact Module for Odoo

A comprehensive Odoo module that extends the standard contact management system with extensive person attributes compliant with NIEM (National Information Exchange Model) standards. This module is designed for government agencies, law enforcement, healthcare providers, and organizations requiring detailed person identification and demographic information.

## Features

### Comprehensive Person Attributes

#### Basic Information
- **Date of Birth**: ISO 8601 compliant birth date with automatic age calculation
- **Gender**: Standardized gender identification
- **Marital Status**: Current marital status tracking

#### Physical Characteristics
- **Height**: Measured in centimeters (CMT unit code)
- **Weight**: Measured in kilograms (KGM unit code)
- **Build**: Physical body type classification
- **Complexion**: Skin complexion description
- **Eye Color**: Standardized eye color options
- **Hair Color**: Hair color classification
- **Hair Style**: Hair length and style
- **Blood Type**: ABO blood type system
- **Distinguishing Features**: Text field for scars, tattoos, etc.

#### Demographics
- **Ethnicity**: Hispanic/Latino identification
- **Race**: Standardized race categories
- **Primary Language**: Primary spoken language
- **Country of Birth**: Birth location tracking
- **Citizenship Status**: Immigration status

#### Identification
- **Social Security Number**: SSN with format validation (XXX-XX-XXXX)
- **Driver License**: Number and issuing state
- **Passport**: Number and issuing country

#### Employment & Education
- **Occupation**: Current profession
- **Employer**: Current employer
- **Education Level**: Highest education achieved

#### Military Service
- **Military Service**: Boolean indicator
- **Military Branch**: Branch of service (if applicable)

#### Medical Information
- **Medical Conditions**: Allergies, conditions, medications

#### Emergency Contact
- **Emergency Contact Name**: Emergency contact person
- **Emergency Contact Relationship**: Relationship to contact

## NIEM Compliance

This module is fully compliant with NIEM Core schema 5.0, enabling seamless data exchange with:

- **Federal Government Systems**: FBI, DHS, DOJ
- **State and Local Agencies**: Law enforcement, social services
- **Healthcare Systems**: Hospitals, clinics, insurance
- **Emergency Management**: First responders, disaster response
- **Immigration Services**: Border control, visa processing

### NIEM XML Export

Generate NIEM-compliant XML for data exchange:

```python
# Export contact data as NIEM XML
partner = self.env['res.partner'].browse(1)
niem_xml = partner.to_niem_xml()
```

## Installation

1. Copy the `extendedcontact` folder to your Odoo addons directory
2. Update the addons list in Odoo
3. Install the "Extended Contact" module
4. Update the module to create database columns: `-u extendedcontact`

## Usage

### Adding Extended Information

1. Navigate to Contacts → Create/Edit a contact
2. For individual contacts (not companies), you'll see organized sections:
   - Basic Information
   - Physical Characteristics
   - Demographics
   - Identification
   - Employment & Education
   - Military Service
   - Medical Information
   - Emergency Contact

### Search and Filtering

The module provides extensive search capabilities:
- Filter by age ranges
- Search by physical characteristics (height, weight, eye color, hair color)
- Filter by demographics (race, ethnicity, citizenship)
- Search by identification numbers
- Filter by military service
- Advanced filters for all major attributes

### Data Validation

The module includes comprehensive validation:
- Birth dates cannot be in the future
- Height must be between 50-250 cm
- Weight must be between 20-300 kg
- SSN must follow XXX-XX-XXXX format
- Age is automatically calculated from birth date

## Demo Data

The module includes comprehensive demo data with diverse examples:
- **John Smith**: Complete profile with all fields populated
- **Maria Garcia**: Hispanic profile with immigration details
- **David Chen**: Asian profile with military service
- **Lisa Johnson**: African American profile with medical information
- **Robert Wilson**: Elderly profile with retirement status
- **Sarah Thompson**: Young adult profile with education details

## Government Integration Benefits

### Law Enforcement
- **CJIS Compliance**: Compatible with Criminal Justice Information Systems
- **NCIC Integration**: National Crime Information Center compatibility
- **Fingerprint Matching**: Supports biometric identification systems
- **Warrant Tracking**: Enhanced person identification for warrants

### Healthcare
- **HIPAA Compliance**: Secure handling of medical information
- **HIE Integration**: Health Information Exchange compatibility
- **Emergency Response**: Critical medical information for first responders
- **Insurance Verification**: Streamlined insurance processing

### Social Services
- **Benefits Eligibility**: Enhanced eligibility determination
- **Case Management**: Comprehensive person profiles for case workers
- **Fraud Prevention**: Improved identity verification
- **Program Tracking**: Better tracking of service utilization

### Immigration Services
- **Border Control**: Enhanced border security identification
- **Visa Processing**: Streamlined visa application processing
- **Citizenship Verification**: Improved citizenship status tracking
- **Deportation Proceedings**: Enhanced person identification

## Technical Details

### Database Schema
- All fields are added to the `res_partner` table
- Proper indexing for search performance
- Data type validation and constraints
- Audit trail tracking for sensitive fields

### Security Features
- Field-level access control
- Audit logging for sensitive data changes
- Data encryption for sensitive fields
- Role-based access permissions

### Performance Optimization
- Efficient search indexing
- Lazy loading for computed fields
- Optimized database queries
- Minimal impact on existing functionality

## Configuration

### Field Visibility
- Fields are only visible for individual contacts (not companies)
- Configurable field visibility through user groups
- Optional fields can be hidden from views

### Validation Rules
- Configurable validation ranges
- Custom validation rules support
- Error message customization
- Field requirement settings

## Support and Maintenance

### Updates
- Regular updates for NIEM schema changes
- Security patches and bug fixes
- Performance improvements
- New feature additions

### Documentation
- Comprehensive API documentation
- NIEM mapping documentation
- Implementation guides
- Best practices documentation

## Contributing

This module is open for contributions. Please ensure:
- NIEM compliance is maintained
- All changes include proper documentation
- Demo data is updated accordingly
- Tests are added for new features

## License

This module is licensed under LGPL-3.0, allowing for commercial use and modification.

## Contact

For support, questions, or contributions, please contact the development team.

---

**Note**: This module is designed for organizations requiring comprehensive person identification and demographic tracking. Ensure compliance with local privacy laws and regulations when implementing. 