{
    'name': 'Extended Contact Information',
    'version': '18.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Extended contact information module (restored to original)',
    'description': """
        This module extends the contact (res.partner) model.
        
        Currently restored to original form with no custom fields.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
} 