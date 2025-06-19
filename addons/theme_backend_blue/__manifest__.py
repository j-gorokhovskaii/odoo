{
    'name': 'Blue Backend Theme',
    'version': '1.0',
    'category': 'Theme/Backend',
    'summary': 'Custom blue theme for Odoo backend',
    'description': """
        This module provides a custom blue theme for the Odoo backend interface.
        Primary color: #29abe2
    """,
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'theme_backend_blue/static/src/scss/style.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
} 