{
    'name': 'Blue Backend Theme',
    'version': '1.0',
    'category': 'Theme/Backend',
    'summary': 'Custom blue theme for Odoo backend and login',
    'description': """
        This module provides a custom blue theme for the Odoo backend interface and login page.
        Primary color: #29abe2
    """,
    'depends': ['web', 'mail'],
    'data': [],
    'assets': {
        # Override the brand color variable BEFORE core primary_variables.scss.
        'web._assets_primary_variables': [
            ('prepend', 'theme_backend_blue/static/src/scss/variables.scss'),
        ],
        'web.assets_backend': [
            'theme_backend_blue/static/src/scss/style.scss',
            'theme_backend_blue/static/src/scss/branding.scss',
            'theme_backend_blue/static/src/js/branding_patch.js',
        ],
        'web.assets_common': [
            'theme_backend_blue/static/src/scss/style.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
} 