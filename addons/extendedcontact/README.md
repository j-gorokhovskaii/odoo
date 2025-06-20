# Extended Contact Information Module

This module extends the Odoo contact (res.partner) model to include comprehensive personal information: Date of Birth, Age, Height, Weight, Eye Color, Hair Color, and Other Distinguishing Features.

## Features

- **Date of Birth Field**: Adds a birthdate field to contacts
- **Computed Age**: Automatically calculates and displays age based on birth date
- **Height Field**: Adds a height field to contacts in metric format (centimeters)
- **Weight Field**: Adds a weight field to contacts in metric format (kilograms)
- **Eye Color Field**: Selection field with common eye colors
- **Hair Color Field**: Selection field with common hair colors
- **Distinguishing Features**: Text field for other physical characteristics
- **Individual Contacts Only**: All fields are only visible for individual contacts (not companies)
- **Validation**: Ensures birth date cannot be in the future and physical measurements are within reasonable bounds
- **Search & Filtering**: Enhanced search capabilities with comprehensive filters
- **Multiple Views**: Works across all partner views (form, tree, search)

## Installation

1. Place this module in your Odoo addons directory
2. Update the modules list in Odoo
3. Install the "Extended Contact Information" module

## Usage

### Adding Personal Information to Contacts

1. Go to **Contacts** → **Customers**
2. Create a new contact or edit an existing one
3. For individual contacts, you'll see the following fields:
   - **Date of Birth**: Enter birth date (e.g., 15/03/1990)
   - **Age**: Automatically calculated and displayed
   - **Height (cm)**: Enter height in centimeters (e.g., 175.5)
   - **Weight (kg)**: Enter weight in kilograms (e.g., 70.5)
   - **Eye Color**: Select from dropdown (Brown, Blue, Green, Hazel, Gray, Amber, Other)
   - **Hair Color**: Select from dropdown (Black, Brown, Blonde, Red, Gray, White, Other)
   - **Other Distinguishing Features**: Free text for additional characteristics

### Validation Rules

- Birth date cannot be in the future
- Height must be between 50 and 250 centimeters
- Weight must be between 20 and 300 kilograms
- Only individual contacts (not companies) can have these values
- All fields are optional

### Searching and Filtering

The module adds comprehensive search options:

**Birth Date Filters:**
- Has Birth Date / No Birth Date

**Height Filters:**
- Has Height / No Height
- Height 150cm+ / Height 180cm+

**Weight Filters:**
- Has Weight / No Weight
- Weight 50kg+ / Weight 80kg+

**Eye Color Filters:**
- Brown Eyes / Blue Eyes / Green Eyes

**Hair Color Filters:**
- Brown Hair / Black Hair / Blonde Hair / Red Hair

**Search Fields:**
- All fields are searchable by typing in the search bar

Note: Age-based filtering is not available since age is a computed field, but you can filter by birth date and see the computed age in the list view.

### List View

In the contacts list view, you can optionally display the following columns for individual contacts:
- Age (computed)
- Height
- Weight
- Eye Color
- Hair Color

## Technical Details

### Model Extensions

The module extends the `res.partner` model with:

- `birthdate`: Date field for storing birth date
- `age`: Computed integer field showing current age (not stored in database)
- `height`: Float field for storing height in centimeters
- `weight`: Float field for storing weight in kilograms
- `eye_color`: Selection field for eye color
- `hair_color`: Selection field for hair color
- `distinguishing_features`: Text field for additional characteristics
- `_compute_age()`: Method to calculate age from birth date
- `_check_birthdate()`: Constraint to validate birth date
- `_check_height()`: Constraint to validate height values
- `_check_weight()`: Constraint to validate weight values

### View Extensions

The module extends several views:
- Main partner form view
- Simplified partner form view
- Partner tree/list view
- Partner search view

### Field Options

**Eye Colors Available:**
- Brown, Blue, Green, Hazel, Gray, Amber, Other

**Hair Colors Available:**
- Black, Brown, Blonde, Red, Gray, White, Other

## Dependencies

- `base`: Core Odoo functionality
- `contacts`: Contact management module

## License

This module is licensed under LGPL-3.

## Contributing

Feel free to contribute to this module by submitting issues or pull requests.

## Support

For support, please contact your Odoo partner or create an issue in the module repository. 