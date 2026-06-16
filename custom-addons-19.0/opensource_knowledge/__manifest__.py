{
    'name': 'Open Source Knowledge Management',
    'version': '19.0.1.0.0',
    'category': 'Productivity/Knowledge',
    'summary': 'Comprehensive open source knowledge management and collaboration platform',
    'description': """
        Open Source Knowledge Management System
        
        This module provides a comprehensive knowledge management platform with features including:
        
        Core Features:
        • Rich text article creation and editing
        • Hierarchical organization with categories and tags
        • Template system for consistent documentation
        • Advanced search and filtering capabilities
        • Version control and article history
        
        Collaboration Features:
        • Granular access control and permissions
        • Article sharing via public/private links
        • User collaboration and commenting
        • Team workspaces and knowledge bases
        
        Integration Features:
        • Seamless integration with CRM, Projects, HR
        • Cross-reference linking between articles
        • Email integration for knowledge sharing
        • API endpoints for external integrations
        
        Advanced Features:
        • Article templates and workflows
        • Automated content organization
        • Analytics and usage tracking
        • Multi-language support
        • Export capabilities (PDF, HTML, etc.)
        
        Built with enterprise-grade security and scalability in mind.
    """,
    'author': 'Elena Rodriguez - Senior Odoo Developer',
    'website': 'https://github.com/opensource-knowledge',
    'depends': [
        'base',
        'web',
        'mail',
        'portal',
        'contacts',
        'html_editor',
    ],
    'data': [
        # Security
        'security/knowledge_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/knowledge_data.xml',
        'data/knowledge_post_install.xml',
        
        # Views
        'views/knowledge_article_views.xml',
        'views/knowledge_category_views.xml',
        'views/knowledge_template_views.xml',
        'views/knowledge_permission_views.xml',
        'views/knowledge_menus.xml',
    ],
    'demo': [
        # 'demo/knowledge_demo.xml',  # Temporarily disabled for debugging
    ],
    'assets': {
        'web.assets_backend': [
            'opensource_knowledge/static/src/js/knowledge_editor.js',
            'opensource_knowledge/static/src/js/knowledge_tree.js',
            'opensource_knowledge/static/src/css/knowledge_backend.css',
        ],
    },
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'sequence': 10,
}