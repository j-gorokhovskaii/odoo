{
    'name': 'Odoo Documentation',
    'version': '18.0.2.0.0',
    'category': 'Documentation',
    'summary': 'Adds a Documentation menu linking to the live official Odoo docs',
    'description': """
Odoo Documentation Link
=======================

Adds a **Documentation** menu to Odoo that opens the official online Odoo
documentation (https://www.odoo.com/documentation/) in a new browser tab.

Always current, no local copy, no maintenance. (Previous versions of this module
served a local static snapshot built from a clone of the docs repo; that approach
was removed in favour of linking the live docs.)
    """,
    'author': 'j-gorokhovskaii',
    'website': 'https://github.com/j-gorokhovskaii/odoo',
    'depends': ['base', 'web'],
    'data': [
        'views/documentation_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
