{
    'name': 'Company Details Extension',
    'version': '18.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Add comprehensive company information fields to business contacts',
    'description': """
        This module extends the contact (res.partner) model to include comprehensive company information.
        
        Features:
        - Company Registration Information (Registration Number, Date, Authority)
        - Tax Information (Tax ID, VAT Number, Tax Registration Date)
        - Business Classification (Industry, Business Type, Company Size)
        - Financial Information (Annual Revenue, Employee Count, Credit Rating)
        - Compliance Information (ISO Certifications, Industry Certifications)
        - Legal Information (Legal Structure, Incorporation Date, Legal Representative)
        - Government Integration (NIEM-compliant data structure)
        - Only visible for company contacts (not individuals)
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