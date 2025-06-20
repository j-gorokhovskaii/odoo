{
    'name': 'Partner Date of Birth',
    'version': '18.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Add Date of Birth field to contacts',
    'description': """
        This module extends the contact (res.partner) model to include a Date of Birth field.
        
        Features:
        - Adds a Date of Birth field to contacts
        - Computed age field based on birth date
        - Only visible for individual contacts (not companies)
        - Proper validation and formatting
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_views_simple.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
} 