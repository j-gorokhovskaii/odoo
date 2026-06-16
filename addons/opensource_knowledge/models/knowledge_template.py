from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KnowledgeTemplate(models.Model):
    _name = 'knowledge.template'
    _description = 'Knowledge Article Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    # Basic Information
    name = fields.Char(
        string='Template Name',
        required=True,
        tracking=True,
        help='Name of the template'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of what this template is used for'
    )
    
    body = fields.Html(
        string='Template Content',
        sanitize_style=True,
        sanitize_form=False,
        help='Default content for articles created from this template'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Used to order templates'
    )
    
    # Template Settings
    category_id = fields.Many2one(
        'knowledge.category',
        string='Default Category',
        help='Default category for articles created from this template'
    )
    
    tag_ids = fields.Many2many(
        'knowledge.tag',
        'knowledge_template_tag_rel',
        'template_id',
        'tag_id',
        string='Default Tags',
        help='Default tags for articles created from this template'
    )
    
    article_type = fields.Selection([
        ('article', 'Article'),
        ('procedure', 'Procedure'),
        ('faq', 'FAQ'),
        ('policy', 'Policy'),
        ('manual', 'Manual'),
        ('tutorial', 'Tutorial'),
        ('reference', 'Reference'),
    ], string='Article Type', default='article', help='Default article type')
    
    visibility = fields.Selection([
        ('private', 'Private'),
        ('internal', 'Internal Users'),
        ('portal', 'Portal Users'),
        ('public', 'Public'),
    ], string='Default Visibility', default='internal', help='Default visibility for articles')
    
    # Template Type
    template_type = fields.Selection([
        ('standard', 'Standard Template'),
        ('form', 'Form Template'),
        ('checklist', 'Checklist Template'),
        ('workflow', 'Workflow Template'),
    ], string='Template Type', default='standard', required=True)
    
    # Access Control
    is_public = fields.Boolean(
        string='Public Template',
        default=True,
        help='If checked, all users can use this template'
    )
    
    user_ids = fields.Many2many(
        'res.users',
        'knowledge_template_user_rel',
        'template_id',
        'user_id',
        string='Authorized Users',
        help='Users who can use this template (if not public)'
    )
    
    group_ids = fields.Many2many(
        'res.groups',
        'knowledge_template_group_rel',
        'template_id',
        'group_id',
        string='Authorized Groups',
        help='Groups who can use this template (if not public)'
    )
    
    # Authoring
    author_id = fields.Many2one(
        'res.users',
        string='Template Author',
        default=lambda self: self.env.user,
        required=True,
        tracking=True
    )
    
    # Status
    active = fields.Boolean(default=True, tracking=True)
    
    # Statistics
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help='Number of times this template has been used'
    )
    
    # Form Fields Configuration (for form templates)
    field_ids = fields.One2many(
        'knowledge.template.field',
        'template_id',
        string='Template Fields',
        help='Fields for form-based templates'
    )
    
    # Statistics fields temporarily removed for debugging
    # article_count = fields.Integer(
    #     string='Articles Created',
    #     default=0,
    #     help='Number of articles created from this template'
    # )
    
    # last_used_date = fields.Datetime(
    #     string='Last Used',
    #     help='Date when this template was last used'
    # )


    def action_create_article(self):
        """Create a new article from this template"""
        self.usage_count += 1
        
        # Prepare article values
        article_vals = {
            'name': _('New Article from %s') % self.name,
            'body': self.body,
            'template_id': self.id,
            'category_id': self.category_id.id,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'article_type': self.article_type,
            'visibility': self.visibility,
            'stage': 'draft',
        }
        
        # Create the article
        article = self.env['knowledge.article'].create(article_vals)
        
        # Return action to open the new article
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Article'),
            'view_mode': 'form',
            'res_model': 'knowledge.article',
            'res_id': article.id,
            'target': 'current',
        }

    def action_preview(self):
        """Preview the template"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Template Preview: %s') % self.name,
            'view_mode': 'form',
            'res_model': 'knowledge.template',
            'res_id': self.id,
            'target': 'new',
            'context': {'preview_mode': True},
        }

    def action_duplicate(self):
        """Duplicate the template"""
        copy_vals = {
            'name': _('%s (Copy)') % self.name,
            'usage_count': 0,
        }
        return self.copy(default=copy_vals)

    def action_view_articles(self):
        """View articles created from this template"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Articles from %s') % self.name,
            'view_mode': 'tree,form',
            'res_model': 'knowledge.article',
            'domain': [('template_id', '=', self.id)],
            'context': {
                'default_template_id': self.id,
            },
        }

    @api.constrains('is_public', 'user_ids', 'group_ids')
    def _check_access_configuration(self):
        """Ensure proper access configuration"""
        for template in self:
            if not template.is_public and not template.user_ids and not template.group_ids:
                raise ValidationError(_('Private templates must have at least one authorized user or group.'))

    @api.model
    def get_available_templates(self, user_id=None):
        """Get templates available to a specific user"""
        if not user_id:
            user_id = self.env.user.id
        
        user = self.env['res.users'].browse(user_id)
        domain = [
            ('active', '=', True),
            '|',
            ('is_public', '=', True),
            '|',
            ('user_ids', 'in', [user_id]),
            ('group_ids', 'in', user.groups_id.ids)
        ]
        
        return self.search(domain)

    @api.model
    def create_from_article(self, article_id, template_name, template_description=None):
        """Create a template from an existing article"""
        article = self.env['knowledge.article'].browse(article_id)
        
        template_vals = {
            'name': template_name,
            'description': template_description or _('Template created from article: %s') % article.name,
            'body': article.body,
            'category_id': article.category_id.id,
            'tag_ids': [(6, 0, article.tag_ids.ids)],
            'article_type': article.article_type,
            'visibility': article.visibility,
            'template_type': 'standard',
        }
        
        return self.create(template_vals)


class KnowledgeTemplateField(models.Model):
    _name = 'knowledge.template.field'
    _description = 'Knowledge Template Field'
    _order = 'sequence, name'

    template_id = fields.Many2one(
        'knowledge.template',
        string='Template',
        required=True,
        ondelete='cascade'
    )
    
    name = fields.Char(
        string='Field Name',
        required=True,
        help='Name of the field'
    )
    
    label = fields.Char(
        string='Field Label',
        required=True,
        help='Label displayed to users'
    )
    
    field_type = fields.Selection([
        ('text', 'Text'),
        ('textarea', 'Text Area'),
        ('html', 'HTML'),
        ('date', 'Date'),
        ('datetime', 'Date & Time'),
        ('selection', 'Selection'),
        ('boolean', 'Checkbox'),
        ('integer', 'Integer'),
        ('float', 'Float'),
    ], string='Field Type', required=True, default='text')
    
    required = fields.Boolean(
        string='Required',
        default=False,
        help='Whether this field is required'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order of fields in the form'
    )
    
    default_value = fields.Text(
        string='Default Value',
        help='Default value for this field'
    )
    
    help_text = fields.Text(
        string='Help Text',
        help='Help text displayed to users'
    )
    
    selection_options = fields.Text(
        string='Selection Options',
        help='Options for selection fields (one per line)'
    )
    
    placeholder = fields.Char(
        string='Placeholder',
        help='Placeholder text for input fields'
    )

    @api.constrains('field_type', 'selection_options')
    def _check_selection_options(self):
        """Ensure selection fields have options"""
        for field in self:
            if field.field_type == 'selection' and not field.selection_options:
                raise ValidationError(_('Selection fields must have options defined.'))

    def get_selection_options_list(self):
        """Get selection options as a list"""
        if self.selection_options:
            return [option.strip() for option in self.selection_options.split('\n') if option.strip()]
        return []