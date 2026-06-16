from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from datetime import datetime
import re

try:
    import html2text
except ImportError:
    html2text = None


class KnowledgeArticle(models.Model):
    _name = 'knowledge.article'
    _description = 'Knowledge Article'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'sequence, name'
    _rec_names_search = ['name']

    # Basic Information
    name = fields.Char(
        string='Title',
        required=True,
        tracking=True,
        help='The title of the knowledge article'
    )
    
    body = fields.Html(
        string='Content',
        sanitize_style=True,
        sanitize_form=False,
        help='Main content of the article'
    )
    
    summary = fields.Text(
        string='Summary',
        help='Brief summary of the article content'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Used to order articles'
    )
    
    # Organization
    category_id = fields.Many2one(
        'knowledge.category',
        string='Category',
        tracking=True,
        help='Category for organizing articles'
    )
    
    parent_id = fields.Many2one(
        'knowledge.article',
        string='Parent Article',
        help='Parent article for hierarchical organization'
    )
    
    child_ids = fields.One2many(
        'knowledge.article',
        'parent_id',
        string='Child Articles'
    )
    
    tag_ids = fields.Many2many(
        'knowledge.tag',
        string='Tags',
        help='Tags for categorizing and searching articles'
    )
    
    # Template and Type
    template_id = fields.Many2one(
        'knowledge.template',
        string='Template',
        help='Template used to create this article'
    )
    
    is_template = fields.Boolean(
        string='Is Template',
        default=False,
        help='Check if this article should be used as a template'
    )
    
    article_type = fields.Selection([
        ('article', 'Article'),
        ('procedure', 'Procedure'),
        ('faq', 'FAQ'),
        ('policy', 'Policy'),
        ('manual', 'Manual'),
        ('tutorial', 'Tutorial'),
        ('reference', 'Reference'),
    ], string='Type', default='article', tracking=True)
    
    # Access Control
    visibility = fields.Selection([
        ('private', 'Private'),
        ('internal', 'Internal Users'),
        ('portal', 'Portal Users'),
        ('public', 'Public'),
    ], string='Visibility', default='internal', required=True, tracking=True)
    
    permission_ids = fields.One2many(
        'knowledge.permission',
        'article_id',
        string='Permissions'
    )
    
    # Sharing
    public_url = fields.Char(
        string='Public URL',
        compute='_compute_public_url',
        help='Public URL for sharing this article'
    )
    
    share_token = fields.Char(
        string='Share Token',
        help='Unique token for sharing',
        copy=False
    )
    
    # Status and Workflow
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ], string='Stage', default='draft', tracking=True)
    
    active = fields.Boolean(default=True)
    
    # Authoring
    author_id = fields.Many2one(
        'res.users',
        string='Author',
        default=lambda self: self.env.user,
        required=True,
        tracking=True
    )
    
    reviewer_ids = fields.Many2many(
        'res.users',
        'knowledge_article_reviewer_rel',
        'article_id',
        'user_id',
        string='Reviewers'
    )
    
    # Dates
    publish_date = fields.Datetime(
        string='Published Date',
        tracking=True
    )
    
    last_review_date = fields.Datetime(
        string='Last Review Date'
    )
    
    next_review_date = fields.Datetime(
        string='Next Review Date',
        help='Date when this article should be reviewed next'
    )
    
    # Statistics
    view_count = fields.Integer(
        string='View Count',
        default=0,
        help='Number of times this article has been viewed'
    )
    
    like_count = fields.Integer(
        string='Likes',
        compute='_compute_like_count',
        store=True
    )
    
    # Computed Fields
    word_count = fields.Integer(
        string='Word Count',
        compute='_compute_word_count',
        store=True,
        help='Approximate word count of the article content'
    )
    
    reading_time = fields.Integer(
        string='Reading Time (minutes)',
        compute='_compute_reading_time',
        store=True,
        help='Estimated reading time in minutes'
    )
    
    has_children = fields.Boolean(
        string='Has Child Articles',
        compute='_compute_has_children'
    )
    
    # Version Control
    version = fields.Float(
        string='Version',
        default=1.0,
        help='Version number of the article'
    )
    
    version_history_ids = fields.One2many(
        'knowledge.article.version',
        'article_id',
        string='Version History'
    )

    @api.depends('body')
    def _compute_word_count(self):
        for article in self:
            if article.body:
                if html2text:
                    # Convert HTML to plain text and count words
                    plain_text = html2text.html2text(article.body)
                    words = len(re.findall(r'\b\w+\b', plain_text))
                    article.word_count = words
                else:
                    # Fallback: strip HTML tags roughly and count words
                    import re as regex
                    plain_text = regex.sub(r'<[^>]+>', '', article.body)
                    words = len(regex.findall(r'\b\w+\b', plain_text))
                    article.word_count = words
            else:
                article.word_count = 0

    @api.depends('word_count')
    def _compute_reading_time(self):
        # Average reading speed: 200 words per minute
        for article in self:
            if article.word_count:
                article.reading_time = max(1, round(article.word_count / 200))
            else:
                article.reading_time = 0

    @api.depends('child_ids')
    def _compute_has_children(self):
        for article in self:
            article.has_children = bool(article.child_ids)

    def _compute_like_count(self):
        # This would be implemented with a likes/ratings system
        for article in self:
            article.like_count = 0  # Placeholder

    def _compute_public_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for article in self:
            if article.visibility == 'public' and article.share_token:
                article.public_url = f"{base_url}/knowledge/article/{article.share_token}"
            else:
                article.public_url = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('share_token'):
                vals['share_token'] = self._generate_share_token()
        articles = super().create(vals_list)
        for article in articles:
            article._create_version_history()
        return articles

    def write(self, vals):
        # Track content changes for version history
        content_changed = 'body' in vals or 'name' in vals
        if content_changed:
            for article in self:
                article._create_version_history()
                # Auto-increment version for major content changes
                if 'body' in vals:
                    vals['version'] = article.version + 0.1
        return super().write(vals)

    def _generate_share_token(self):
        import secrets
        return secrets.token_urlsafe(32)

    def _create_version_history(self):
        """Create a version history entry"""
        if self.body:  # Only create history if there's content
            self.env['knowledge.article.version'].create({
                'article_id': self.id,
                'name': self.name,
                'body': self.body,
                'version': self.version,
                'author_id': self.env.user.id,
                'create_date': fields.Datetime.now(),
            })

    def action_publish(self):
        """Publish the article"""
        self.write({
            'stage': 'published',
            'publish_date': fields.Datetime.now()
        })
        self.message_post(body=_("Article has been published."))

    def action_archive(self):
        """Archive the article"""
        self.write({'stage': 'archived'})
        self.message_post(body=_("Article has been archived."))

    def action_submit_review(self):
        """Submit article for review"""
        if not self.reviewer_ids:
            raise ValidationError(_("Please assign reviewers before submitting for review."))
        self.write({'stage': 'review'})
        self.message_post(body=_("Article submitted for review."))

    def action_duplicate(self):
        """Duplicate article with incremented name"""
        copy_vals = {
            'name': _("%s (Copy)") % self.name,
            'stage': 'draft',
            'publish_date': False,
            'view_count': 0,
            'version': 1.0,
        }
        return self.copy(default=copy_vals)

    def action_create_template(self):
        """Convert article to template"""
        template_vals = {
            'name': f"Template: {self.name}",
            'description': f"Template based on {self.name}",
            'body': self.body,
            'category_id': self.category_id.id,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
        }
        template = self.env['knowledge.template'].create(template_vals)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Template Created'),
            'view_mode': 'form',
            'res_model': 'knowledge.template',
            'res_id': template.id,
            'target': 'current',
        }

    def increment_view_count(self):
        """Increment view count (called when article is viewed)"""
        self.sudo().write({'view_count': self.view_count + 1})

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        """Prevent circular references in parent-child relationships"""
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive article hierarchies.'))

    @api.constrains('visibility', 'permission_ids')
    def _check_visibility_permissions(self):
        """Ensure proper permissions based on visibility"""
        for article in self:
            if article.visibility == 'private' and not article.permission_ids:
                # Private articles should have explicit permissions
                pass  # Could auto-create permission for author

    def _get_portal_access_url(self):
        """Get portal URL for this article"""
        return f'/knowledge/article/{self.share_token}'

    @api.model
    def search_articles(self, search_term, category_id=None, tag_ids=None, limit=20):
        """Advanced search functionality"""
        domain = [
            ('stage', '=', 'published'),
            ('active', '=', True),
            '|', '|',
            ('name', 'ilike', search_term),
            ('body', 'ilike', search_term),
            ('summary', 'ilike', search_term)
        ]
        
        if category_id:
            domain.append(('category_id', '=', category_id))
            
        if tag_ids:
            domain.append(('tag_ids', 'in', tag_ids))
            
        return self.search(domain, limit=limit, order='view_count desc')


class KnowledgeArticleVersion(models.Model):
    _name = 'knowledge.article.version'
    _description = 'Knowledge Article Version History'
    _order = 'create_date desc'

    article_id = fields.Many2one(
        'knowledge.article',
        string='Article',
        required=True,
        ondelete='cascade'
    )
    
    name = fields.Char(
        string='Title',
        required=True
    )
    
    body = fields.Html(
        string='Content'
    )
    
    version = fields.Float(
        string='Version',
        required=True
    )
    
    author_id = fields.Many2one(
        'res.users',
        string='Author',
        required=True
    )
    
    create_date = fields.Datetime(
        string='Created On',
        required=True
    )
    
    change_summary = fields.Text(
        string='Change Summary',
        help='Summary of changes made in this version'
    )