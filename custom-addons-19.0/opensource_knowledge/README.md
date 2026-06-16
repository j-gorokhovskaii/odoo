# Open Source Knowledge Management

A comprehensive knowledge management system for Odoo 18.0 that provides enterprise-grade features for creating, organizing, and sharing knowledge within your organization.

## Features

### Core Features
- **Rich Text Editor**: Create beautiful, formatted articles with comprehensive editing tools
- **Hierarchical Organization**: Organize content with categories and subcategories
- **Tagging System**: Add tags for better content discovery and organization
- **Template System**: Create consistent content using predefined templates
- **Version Control**: Track changes and maintain article history
- **Advanced Search**: Powerful search capabilities across all content

### Collaboration Features
- **Granular Permissions**: Control who can read, write, comment, or manage articles
- **Article Sharing**: Share articles via public/private links with expiration dates
- **User Collaboration**: Multi-user editing and commenting system
- **Review Workflow**: Submit articles for review before publication
- **Team Workspaces**: Organize knowledge by teams or departments

### Integration Features
- **Portal Integration**: Share knowledge with portal users
- **Website Integration**: Public knowledge base for customers
- **Email Integration**: Send knowledge digests and notifications
- **API Access**: REST API for external integrations
- **Cross-App Linking**: Link articles to CRM, Projects, and other Odoo apps

### Advanced Features
- **Article Analytics**: Track views, likes, and engagement
- **Contribution Scoring**: Gamify knowledge sharing
- **Auto-Save**: Never lose your work with automatic saving
- **Mobile Responsive**: Access knowledge on any device
- **Multi-Language**: Support for multiple languages
- **Export Capabilities**: Export articles to PDF, HTML, and other formats

## Installation

1. Copy the `opensource_knowledge` folder to your Odoo addons directory
2. Update your apps list in Odoo
3. Install the "Open Source Knowledge Management" module
4. Configure user permissions and create your first categories

## Configuration

### User Groups
- **Knowledge User**: Can read and create articles
- **Knowledge Manager**: Can manage categories, templates, and review articles
- **Knowledge Administrator**: Full access to all features

### Initial Setup
1. Create categories for organizing your knowledge
2. Set up templates for common article types
3. Configure user permissions and access levels
4. Import demo data for testing (optional)

## Usage

### Creating Articles
1. Navigate to Knowledge > Articles
2. Click "Create" to start a new article
3. Choose a template or start with a blank article
4. Write your content using the rich text editor
5. Add tags and set permissions
6. Save as draft or publish immediately

### Organizing Content
- Use categories to create a logical structure
- Add tags for cross-cutting topics
- Create parent-child relationships between articles
- Use templates to maintain consistency

### Sharing Knowledge
- Set article visibility (private, internal, portal, public)
- Create share links for external access
- Set up permissions for specific users or groups
- Enable commenting and collaboration

## Technical Details

### Models
- `knowledge.article`: Main article model with rich content
- `knowledge.category`: Hierarchical categorization
- `knowledge.template`: Template system for consistency
- `knowledge.permission`: Granular access control
- `knowledge.tag`: Tagging system
- `knowledge.share`: External sharing capabilities

### Security
- Role-based access control
- Record-level security rules
- Field-level permissions
- Audit trail for all changes

### Performance
- Optimized database queries
- Caching for frequently accessed content
- Lazy loading for large knowledge bases
- Full-text search capabilities

## Customization

The module is designed to be easily customizable:

### Adding Custom Fields
Extend the article model to add custom fields specific to your organization.

### Custom Templates
Create custom templates for specific document types or processes.

### Integration Hooks
Use the provided hooks to integrate with other systems or add custom functionality.

### Styling
Customize the appearance by modifying the CSS files or adding custom themes.

## Support

For support, issues, or feature requests, please contact the development team or check the project documentation.

## License

This module is licensed under LGPL-3. See the LICENSE file for details.

## Credits

Developed by Elena Rodriguez - Senior Odoo Developer
Built with enterprise-grade security and scalability in mind.

## Version History

- **1.0.0**: Initial release with core functionality
- Features: Article creation, categorization, templates, permissions
- Security: Role-based access control, sharing capabilities
- Integration: Portal and website integration ready