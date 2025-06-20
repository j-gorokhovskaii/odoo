# Partner Height Module

This module extends the Odoo contact (res.partner) model to include Height functionality.

## Features

- **Height Field**: Adds a height field to contacts in metric format (centimeters)
- **Individual Contacts Only**: Height field is only visible for individual contacts (not companies)
- **Validation**: Ensures height values are within reasonable bounds (50-250 cm)
- **Search & Filtering**: Enhanced search capabilities with height-based filters
- **Multiple Views**: Works across all partner views (form, tree, search)

## Installation

1. Place this module in your Odoo addons directory
2. Update the modules list in Odoo
3. Install the "Partner Height" module

## Usage

### Adding Height to Contacts

1. Go to **Contacts** → **Customers**
2. Create a new contact or edit an existing one
3. For individual contacts, you'll see the "Height (cm)" field
4. Enter the height in centimeters (e.g., 175.5 for 175.5 cm)
5. The field will validate that the height is between 50 and 250 cm

### Searching and Filtering

The module adds several new search options:
- **Has Height**: Shows contacts with height values
- **No Height**: Shows contacts without height values
- **Height 150cm+**: Shows contacts 150cm or taller
- **Height 180cm+**: Shows contacts 180cm or taller

### List View

In the contacts list view, you can optionally display the height column for individual contacts.

## Technical Details

### Model Extensions

The module extends the `res.partner` model with:

- `height`: Float field for storing height in centimeters
- `_check_height()`: Constraint to validate height values

### View Extensions

The module extends several views:
- Main partner form view
- Simplified partner form view
- Partner tree/list view
- Partner search view

## Validation Rules

- Height must be between 50 and 250 centimeters
- Only individual contacts (not companies) can have height values
- Height field is optional

## Dependencies

- `base`: Core Odoo functionality
- `contacts`: Contact management module

## License

This module is licensed under LGPL-3.

## Contributing

Feel free to contribute to this module by submitting issues or pull requests.

## Support

For support, please contact your Odoo partner or create an issue in the module repository. 