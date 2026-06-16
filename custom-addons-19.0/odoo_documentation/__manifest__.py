{
    'name': 'Odoo Documentation',
    'version': '19.0.1.0.0',
    'category': 'Documentation',
    'summary': 'Integrated Odoo official documentation viewer',
    'description': """
Odoo Documentation Module
=========================

This module integrates the official Odoo documentation directly into your Odoo instance.

Features:
---------
* Access Odoo documentation without leaving your instance
* Organized by categories (Applications, Administration, Developer, Contributing)
* Fast local access
* Search functionality
* Responsive design

Setup:
------
1. Clone the Odoo documentation: git clone https://github.com/odoo/documentation.git
2. Run the import script: python addons/odoo_documentation/scripts/import_docs.py
3. Install this module in Odoo
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'web'],
    'data': [
        'views/documentation_menu.xml',
        'views/documentation_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_documentation/static/src/css/documentation.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}