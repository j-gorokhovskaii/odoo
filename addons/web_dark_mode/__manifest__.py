{
    'name': 'Dark Mode Toggle',
    'version': '1.0.0',
    'category': 'Web',
    'summary': 'Add dark mode toggle to Odoo backend',
    'description': """
        This module adds a dark mode toggle to the Odoo backend interface.
        
        Features:
        - Dark theme with comprehensive styling
        - Toggle button in the top navigation bar
        - User preference stored in local storage
        - Seamless integration with existing Odoo features
        - Responsive design for all screen sizes
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'web_dark_mode/static/src/scss/dark_theme.scss',
            'web_dark_mode/static/src/js/dark_mode_toggle.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
} 