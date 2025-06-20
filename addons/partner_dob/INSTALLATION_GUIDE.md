# Installation and Usage Guide: Partner Date of Birth Module

## Quick Start

This guide will help you install and use the Partner Date of Birth module to add birth date functionality to your Odoo contacts.

## Installation

### Method 1: Manual Installation

1. **Copy the Module**:
   ```bash
   # Copy the partner_dob folder to your Odoo addons directory
   cp -r partner_dob /path/to/odoo/addons/
   ```

2. **Update Module List**:
   - Log into Odoo as an administrator
   - Go to **Apps** → **Update Apps List**
   - Click **Update** to refresh the module list

3. **Install the Module**:
   - Search for "Partner Date of Birth" in the Apps search
   - Click **Install** on the module

### Method 2: Using Odoo.sh or Cloud

1. **Add to Repository**:
   - Add the module files to your Odoo.sh repository
   - Push the changes to trigger automatic deployment

2. **Install via Apps**:
   - Go to **Apps** → **Update Apps List**
   - Search and install "Partner Date of Birth"

## Usage

### Adding Birth Date to Contacts

1. **Navigate to Contacts**:
   - Go to **Contacts** → **Customers**

2. **Create or Edit a Contact**:
   - Click **Create** for a new contact
   - Or select an existing contact and click **Edit**

3. **Enter Birth Date**:
   - For individual contacts (not companies), you'll see:
     - **Date of Birth** field with a date picker
     - **Age** field (automatically calculated)
   - Enter the birth date using the date picker
   - The age will be calculated automatically

4. **Save the Contact**:
   - Click **Save** to store the information

### Viewing Birth Date Information

#### In Contact Form
- The birth date and age are displayed in the main contact information section
- Age is shown as a read-only field next to the birth date

#### In Contact List
- Age can be displayed as an optional column
- Right-click on the list header to add/remove the Age column

#### In Search Results
- Use the search filters to find contacts by age or birth date status

### Search and Filtering

The module adds several new search options:

1. **Has Birth Date**: Shows only contacts with birth dates set
2. **No Birth Date**: Shows only contacts without birth dates
3. **Age 18+**: Shows contacts aged 18 or older
4. **Age 65+**: Shows contacts aged 65 or older

To use these filters:
1. Go to **Contacts** → **Customers**
2. Click the **Search** icon
3. Use the filters in the search panel

### Validation Features

The module includes automatic validation:
- **Future Dates**: Birth dates cannot be set in the future
- **Age Calculation**: Age is automatically calculated and updated
- **Individual Contacts Only**: Birth date fields are only shown for individual contacts, not companies

## Configuration

### Field Visibility

The birth date fields are automatically hidden for:
- Companies (`is_company = True`)
- Contacts without birth dates (age field only)

### Date Format

The date picker uses the format: **DD/MM/YYYY**
- Example: 15/03/1990 for March 15, 1990

### Age Calculation

Age is calculated as of the current date:
- If the birthday hasn't occurred this year, the age is reduced by 1
- If no birth date is set, age shows as 0

## Troubleshooting

### Module Not Appearing

1. **Check Installation**:
   - Verify the module is in the correct addons directory
   - Ensure the `__manifest__.py` file is properly formatted

2. **Update Module List**:
   - Go to **Apps** → **Update Apps List**
   - Click **Update**

3. **Check Dependencies**:
   - Ensure the `base` and `contacts` modules are installed

### Fields Not Visible

1. **Check Contact Type**:
   - Birth date fields only appear for individual contacts
   - Companies will not show these fields

2. **Check User Permissions**:
   - Ensure you have proper access rights to view/edit contacts

3. **Clear Browser Cache**:
   - Refresh the page or clear browser cache

### Age Not Calculating

1. **Check Birth Date**:
   - Ensure a valid birth date is entered
   - Check that the date is not in the future

2. **Refresh the Page**:
   - Age is calculated on-the-fly, try refreshing the page

3. **Check for Errors**:
   - Look for any error messages in the browser console

## Advanced Usage

### API Access

You can access birth date information programmatically:

```python
# Get contacts with birth dates
partners_with_birthdate = env['res.partner'].search([
    ('birthdate', '!=', False)
])

# Get contacts by age
adult_contacts = env['res.partner'].search([
    ('age', '>=', 18)
])

# Calculate age manually
for partner in partners:
    if partner.birthdate:
        age = (date.today() - partner.birthdate).days // 365
        print(f"{partner.name}: {age} years old")
```

### Custom Views

You can create custom views that include birth date information:

```xml
<record id="custom_partner_view" model="ir.ui.view">
    <field name="name">custom.partner.view</field>
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="birthdate"/>
                    <field name="age"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

### Reporting

You can create reports that include age demographics:

```python
# Example: Age distribution report
age_groups = {
    '18-25': 0,
    '26-35': 0,
    '36-50': 0,
    '50+': 0
}

for partner in env['res.partner'].search([('birthdate', '!=', False)]):
    if 18 <= partner.age <= 25:
        age_groups['18-25'] += 1
    elif 26 <= partner.age <= 35:
        age_groups['26-35'] += 1
    elif 36 <= partner.age <= 50:
        age_groups['36-50'] += 1
    else:
        age_groups['50+'] += 1
```

## Support

If you encounter issues:

1. **Check the Logs**: Look for error messages in Odoo logs
2. **Verify Installation**: Ensure all files are in the correct locations
3. **Test in Clean Environment**: Try installing in a fresh Odoo instance
4. **Contact Support**: Reach out to your Odoo partner or create an issue

## Updates

To update the module:

1. **Backup Data**: Always backup your database before updates
2. **Update Files**: Replace the module files with new versions
3. **Update Module**: Go to **Apps** → **Update Apps List** → **Update**
4. **Test Functionality**: Verify all features work correctly

## License

This module is licensed under LGPL-3. You are free to modify and distribute it according to the license terms. 