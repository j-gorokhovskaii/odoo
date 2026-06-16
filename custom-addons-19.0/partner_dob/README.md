# Partner Date of Birth Module

This module extends the Odoo contact (res.partner) model to include Date of Birth functionality.

## Features

- **Date of Birth Field**: Adds a birthdate field to contacts
- **Computed Age**: Automatically calculates and displays age based on birth date
- **Individual Contacts Only**: Birth date fields are only visible for individual contacts (not companies)
- **Validation**: Ensures birth date cannot be in the future
- **Search & Filtering**: Enhanced search capabilities with age-based filters
- **Multiple Views**: Works across all partner views (form, tree, search)

## Installation

1. Place this module in your Odoo addons directory
2. Update the modules list in Odoo
3. Install the "Partner Date of Birth" module

## Usage

### Adding Birth Date to Contacts

1. Go to **Contacts** → **Customers**
2. Create a new contact or edit an existing one
3. For individual contacts, you'll see the "Date of Birth" field
4. Enter the birth date using the date picker
5. The age will be automatically calculated and displayed

### Searching and Filtering

The module adds several new search options:
- **Has Birth Date**: Shows contacts with birth dates
- **No Birth Date**: Shows contacts without birth dates
- **Age 18+**: Shows contacts aged 18 or older
- **Age 65+**: Shows contacts aged 65 or older

### List View

In the contacts list view, you can optionally display the age column for individual contacts.

## Technical Details

### Model Extensions

The module extends the `res.partner` model with:

- `birthdate`: Date field for storing birth date
- `age`: Computed integer field showing current age
- `_compute_age()`: Method to calculate age from birth date
- `_check_birthdate()`: Constraint to validate birth date

### View Extensions

The module extends several views:
- Main partner form view
- Simplified partner form view
- Private address form view
- Partner tree/list view
- Partner search view

## Dependencies

- `base`: Core Odoo functionality
- `contacts`: Contact management module

## License

This module is licensed under LGPL-3.

## Contributing

Feel free to contribute to this module by submitting issues or pull requests.

## Support

For support, please contact your Odoo partner or create an issue in the module repository. 