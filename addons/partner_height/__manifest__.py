{
    'name': 'Partner Height',
    'version': '18.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Add Height field to contacts',
    'description': """
        This module extends the contact (res.partner) model to include a Height field.
        
        Features:
        - Adds a Height field to contacts in metric format (cm)
        - Only visible for individual contacts (not companies)
        - Proper validation for reasonable height values
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