# Company Details Extension Module

## Overview

The Company Details Extension module extends Odoo's contact management system to include comprehensive company information fields. This module is designed to be NIEM-compliant and suitable for government integration and enterprise-level contact management.

## Features

### Company Registration Information
- **Company Registration Number**: Official registration number issued by regulatory authority
- **Registration Date**: Date when company was officially registered
- **Registration Authority**: Government authority that issued the registration
- **Incorporation Date**: Date when company was incorporated

### Tax Information
- **Tax ID**: Company tax identification number
- **VAT Number**: Value Added Tax registration number
- **Tax Registration Date**: Date when company was registered for tax purposes

### Business Classification
- **Industry**: Primary industry sector (Technology, Healthcare, Finance, etc.)
- **Business Type**: Legal structure (Corporation, LLC, Partnership, etc.)
- **Company Size**: Employee count categories (Micro to Enterprise)
- **Legal Structure**: Detailed legal structure description

### Financial Information
- **Annual Revenue**: Revenue range categories
- **Employee Count**: Total number of employees
- **Credit Rating**: Company credit rating (AAA to D)

### Compliance Information
- **ISO Certifications**: Multiple ISO certifications (9001, 14001, 27001, 45001)
- **Industry Certifications**: Industry-specific certifications and licenses
- **Compliance Status**: Overall compliance status

### Legal Information
- **Legal Representative**: Name of legal representative
- **Legal Representative Title**: Title or position of legal representative

### Social Media Information
- **Company Website**: Official company website
- **LinkedIn Profile**: Company LinkedIn profile
- **Facebook Page**: Company Facebook page
- **Twitter Handle**: Company Twitter handle
- **Instagram Profile**: Company Instagram profile

### Company Age Information
- **Company Age (Years/Months/Days/Hours)**: Detailed age calculation
- **Days to Next Anniversary**: Countdown to next company anniversary

## User Interface

### Company Extended Information Tab
The module adds a new "Company Extended Information" tab next to the "Internal Notes" tab in the contact form. This tab is only visible for company contacts and contains all comprehensive company information organized into logical sections:

- **Registration Information**: Company registration details
- **Tax Information**: Tax-related information
- **Business Classification**: Industry and business type details
- **Financial Information**: Revenue and employee information
- **Legal Information**: Legal representative details
- **Compliance Information**: Certifications and compliance status
- **Social Media**: Company social media profiles
- **Company Age**: Detailed age calculations and anniversary countdown

## NIEM Compliance

This module is designed to be NIEM (National Information Exchange Model) compliant, making it suitable for government integration:

### NIEM Mapping
- **Company Registration**: `nc:Organization/nc:OrganizationIdentification`
- **Tax Information**: `nc:Organization/nc:OrganizationTaxIdentification`
- **Business Classification**: `nc:Organization/nc:OrganizationCategory`
- **Financial Information**: `nc:Organization/nc:OrganizationFinancialInformation`
- **Compliance Information**: `nc:Organization/nc:OrganizationComplianceInformation`

### XML Export
The module includes a method to export company data in NIEM-compliant XML format:
```python
partner.export_as_niem_xml()
```

## Installation

1. Place the module in your Odoo addons directory
2. Update the addons list in Odoo
3. Install the "Company Details Extension" module
4. Restart Odoo server

## Usage

### For Companies Only
All company detail fields are only visible for company contacts (`is_company = True`). Individual contacts will not see these fields.

### Accessing Company Details
1. Go to Contacts
2. Select a company contact
3. Click on the "Company Extended Information" tab
4. Fill in the relevant company information

### Search and Filter
The module adds comprehensive search filters:
- Companies with registration information
- Companies with tax information
- Large/Small companies
- Compliant companies
- Companies by industry

### List View
The list view includes additional columns:
- Industry
- Company Size
- Employee Count
- Registration Number
- Compliance Status

## Validation

The module includes comprehensive validation:
- Registration and incorporation dates cannot be in the future
- Employee count must be positive
- Registration number format validation
- Required field validation

## Demo Data

The module includes demo data for:
- ISO Certifications (9001, 14001, 27001, 45001)
- Sample companies in different industries
- Various business types and sizes

## Government Integration Benefits

### Data Standardization
- NIEM-compliant data structure
- Standardized field formats
- Consistent data validation

### Regulatory Compliance
- Comprehensive compliance tracking
- ISO certification management
- Audit trail capabilities

### Reporting Capabilities
- Industry classification reporting
- Compliance status reporting
- Financial information aggregation

### Interoperability
- XML export functionality
- Standard data exchange formats
- Government system compatibility

## Technical Details

### Dependencies
- `base`: Core Odoo functionality
- `contacts`: Contact management

### Models
- `res.partner`: Extended with company fields
- `company.iso.certification`: ISO certification management

### Views
- Form view with Company Extended Information tab
- Search view with company-specific filters
- Tree view with additional columns

### Computed Fields
- Company age calculations
- Anniversary countdown
- Real-time updates

## Contributing

When contributing to this module:
1. Follow Odoo development guidelines
2. Maintain NIEM compliance
3. Add appropriate validation
4. Update documentation
5. Include demo data for new features

## License

This module is licensed under LGPL-3.

## Support

For support and questions:
- Check the module documentation
- Review the demo data for examples
- Contact the development team

## Version History

- **18.0.1.0.0**: Initial release with comprehensive company information fields and Company Extended Information tab 