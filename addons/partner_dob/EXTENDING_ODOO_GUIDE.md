# Guide: Extending Odoo Modules

This guide explains how to extend Odoo modules, specifically focusing on adding Date of Birth functionality to the contact module. This is based on the [Odoo 18.0 Developer Documentation](https://www.odoo.com/documentation/18.0/developer.html).

## Understanding Odoo Module Structure

### Core Concepts

1. **Models**: Python classes that represent database tables
2. **Views**: XML definitions that control how data is displayed
3. **Inheritance**: Odoo's mechanism for extending existing functionality
4. **Manifest**: Module configuration file

### Key Files in a Module

```
module_name/
├── __manifest__.py      # Module configuration
├── __init__.py          # Python imports
├── models/              # Model definitions
│   ├── __init__.py
│   └── model_name.py
├── views/               # View definitions
│   └── view_name.xml
├── security/            # Access rights
│   └── ir.model.access.csv
├── demo/                # Demo data
│   └── demo_data.xml
└── tests/               # Unit tests
    ├── __init__.py
    └── test_model.py
```

## Step-by-Step Extension Process

### 1. Create Module Structure

First, create the basic module structure:

```bash
mkdir addons/your_module_name
cd addons/your_module_name
mkdir models views security demo tests
touch __manifest__.py __init__.py
touch models/__init__.py
touch views/
touch security/ir.model.access.csv
touch tests/__init__.py
```

### 2. Define Module Manifest

The `__manifest__.py` file is crucial - it tells Odoo about your module:

```python
{
    'name': 'Your Module Name',
    'version': '18.0.1.0.0',
    'category': 'Category',
    'summary': 'Brief description',
    'description': 'Detailed description',
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'depends': ['base', 'other_module'],  # Dependencies
    'data': [
        'views/your_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
```

### 3. Extend Models

To extend an existing model (like `res.partner`), use inheritance:

```python
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'  # Inherit from existing model
    
    # Add new fields
    birthdate = fields.Date(
        string='Date of Birth',
        help='Birth date of the contact',
        tracking=True,
    )
    
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=False,
        help='Age calculated from birth date',
    )
    
    # Add computed methods
    @api.depends('birthdate')
    def _compute_age(self):
        """Compute age based on birthdate"""
        today = date.today()
        for partner in self:
            if partner.birthdate:
                age = today.year - partner.birthdate.year
                # Adjust for birthday not yet occurred this year
                if today.month < partner.birthdate.month or (
                    today.month == partner.birthdate.month and 
                    today.day < partner.birthdate.day
                ):
                    age -= 1
                partner.age = age
            else:
                partner.age = 0
    
    # Add constraints
    @api.constrains('birthdate')
    def _check_birthdate(self):
        """Validate birthdate is not in the future"""
        today = date.today()
        for partner in self:
            if partner.birthdate and partner.birthdate > today:
                raise models.ValidationError(
                    "Birth date cannot be in the future."
                )
```

### 4. Extend Views

Views are extended using XML inheritance with XPath expressions:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Extend existing view -->
        <record id="view_partner_form_inherit" model="ir.ui.view">
            <field name="name">res.partner.form.inherit</field>
            <field name="model">res.partner</field>
            <field name="inherit_id" ref="base.view_partner_form"/>
            <field name="arch" type="xml">
                <!-- Add field after existing field -->
                <xpath expr="//field[@name='function']" position="after">
                    <field name="birthdate" 
                           invisible="is_company" 
                           widget="date"
                           options="{'format': 'dd/mm/yyyy'}"
                           placeholder="e.g. 15/03/1990"/>
                    <field name="age" 
                           invisible="is_company or not birthdate" 
                           readonly="1"/>
                </xpath>
            </field>
        </record>
    </data>
</odoo>
```

### 5. Common View Inheritance Patterns

#### Adding Fields to Forms
```xml
<xpath expr="//field[@name='existing_field']" position="after">
    <field name="new_field"/>
</xpath>
```

#### Adding Fields to Lists
```xml
<xpath expr="//field[@name='email']" position="after">
    <field name="age" optional="hide"/>
</xpath>
```

#### Adding Filters to Search
```xml
<xpath expr="//filter[@name='inactive']" position="after">
    <separator/>
    <filter string="Has Birth Date" 
            name="has_birthdate" 
            domain="[('birthdate', '!=', False)]"/>
</xpath>
```

### 6. Field Types and Options

#### Date Fields
```python
birthdate = fields.Date(
    string='Date of Birth',
    help='Birth date of the contact',
    tracking=True,  # Track changes
)
```

#### Computed Fields
```python
age = fields.Integer(
    string='Age',
    compute='_compute_age',
    store=False,  # Don't store in database
    help='Age calculated from birth date',
)
```

#### Selection Fields
```python
status = fields.Selection([
    ('active', 'Active'),
    ('inactive', 'Inactive'),
], string='Status', default='active')
```

### 7. Computed Methods

#### Simple Computation
```python
@api.depends('field1', 'field2')
def _compute_field3(self):
    for record in self:
        record.field3 = record.field1 + record.field2
```

#### Complex Computation with Conditions
```python
@api.depends('birthdate')
def _compute_age(self):
    today = date.today()
    for partner in self:
        if partner.birthdate:
            age = today.year - partner.birthdate.year
            if today.month < partner.birthdate.month or (
                today.month == partner.birthdate.month and 
                today.day < partner.birthdate.day
            ):
                age -= 1
            partner.age = age
        else:
            partner.age = 0
```

### 8. Constraints and Validation

#### Field Constraints
```python
@api.constrains('field1', 'field2')
def _check_fields(self):
    for record in self:
        if record.field1 and record.field2:
            if record.field1 > record.field2:
                raise ValidationError("Field1 cannot be greater than Field2")
```

#### SQL Constraints
```python
_sql_constraints = [
    ('unique_name', 'UNIQUE(name)', 'Name must be unique!'),
    ('check_age', 'CHECK(age >= 0)', 'Age cannot be negative'),
]
```

### 9. Security and Access Rights

Create `security/ir.model.access.csv`:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_res_partner_user,res.partner.user,model_res_partner,base.group_user,1,1,1,0
access_res_partner_manager,res.partner.manager,model_res_partner,base.group_system,1,1,1,1
```

### 10. Testing Your Module

Create comprehensive tests:

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestYourModel(TransactionCase):
    def setUp(self):
        super().setUp()
        self.model = self.env['your.model']
    
    def test_field_creation(self):
        record = self.model.create({
            'name': 'Test',
            'field1': 'value1',
        })
        self.assertEqual(record.name, 'Test')
    
    def test_validation(self):
        with self.assertRaises(ValidationError):
            self.model.create({
                'name': 'Test',
                'field1': 'invalid_value',
            })
```

### 11. Installation and Testing

1. **Install Module**:
   - Go to Apps → Update Apps List
   - Search for your module
   - Click Install

2. **Test Functionality**:
   - Navigate to the relevant menu
   - Create/Edit records
   - Test all features

3. **Check Logs**:
   - Monitor Odoo logs for errors
   - Use developer tools for debugging

### 12. Best Practices

#### Code Organization
- Keep models in separate files
- Use meaningful field and method names
- Add comprehensive docstrings
- Follow PEP 8 style guidelines

#### Performance
- Use `@api.depends` correctly for computed fields
- Avoid expensive operations in computed methods
- Use `store=True` for frequently accessed computed fields

#### Security
- Always define proper access rights
- Validate user input
- Use appropriate field types and constraints

#### User Experience
- Provide helpful field labels and help text
- Use appropriate widgets for field types
- Make fields invisible when not relevant
- Add proper placeholders and examples

### 13. Common Pitfalls

1. **Forgetting Dependencies**: Always include required modules in `depends`
2. **Incorrect XPath**: Test XPath expressions carefully
3. **Missing Constraints**: Validate data at the model level
4. **Poor Performance**: Avoid expensive computations in loops
5. **Incomplete Testing**: Test all scenarios including edge cases

### 14. Debugging Tips

1. **Enable Developer Mode**: Access advanced features
2. **Use Browser Developer Tools**: Inspect views and JavaScript
3. **Check Odoo Logs**: Monitor for errors and warnings
4. **Use `_logger`**: Add logging to your code
5. **Test Incrementally**: Add features one at a time

## Conclusion

Extending Odoo modules requires understanding the inheritance system, proper model design, and careful view management. This guide covers the essential concepts and provides practical examples for adding Date of Birth functionality to contacts.

For more advanced topics, refer to the [Odoo Developer Documentation](https://www.odoo.com/documentation/18.0/developer.html) and explore existing modules in the Odoo codebase for real-world examples. 