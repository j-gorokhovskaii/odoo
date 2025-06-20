{
    'name': 'Extended Contact Information',
    'version': '18.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Add comprehensive personal information fields to contacts',
    'description': """
        This module extends the contact (res.partner) model to include comprehensive personal information.
        
        Features:
        - Adds a Date of Birth field to contacts
        - Computed age field based on birth date
        - Adds Height field in metric format (cm)
        - Adds Weight field in metric format (kg)
        - Adds Eye Color selection field
        - Adds Hair Color selection field
        - Adds Other Distinguishing Features text field
        - Only visible for individual contacts (not companies)
        - Proper validation and formatting
        - Enhanced search capabilities with comprehensive filters
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
} 