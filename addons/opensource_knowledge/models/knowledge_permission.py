from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from dateutil.relativedelta import relativedelta


class KnowledgePermission(models.Model):
    _name = 'knowledge.permission'
    _description = 'Knowledge Article Permission'
    _rec_name = 'article_id'

    article_id = fields.Many2one(
        'knowledge.article',
        string='Article',
        required=True,
        ondelete='cascade'
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='User',
        help='Specific user (leave empty for group permission)'
    )
    
    group_id = fields.Many2one(
        'res.groups',
        string='Group',
        help='User group (leave empty for user permission)'
    )
    
    permission = fields.Selection([
        ('read', 'Read'),
        ('write', 'Write'),
        ('comment', 'Comment'),
        ('manage', 'Manage'),
    ], string='Permission', required=True, default='read')
    
    inherit_to_children = fields.Boolean(
        string='Inherit to Child Articles',
        default=True,
        help='Apply this permission to all child articles'
    )
    
    # Sharing settings
    share_token = fields.Char(
        string='Share Token',
        help='Token for sharing access'
    )
    
    expiry_date = fields.Datetime(
        string='Expiry Date',
        help='Date when this permission expires'
    )
    
    # Metadata
    create_uid = fields.Many2one(
        'res.users',
        string='Created by',
        default=lambda self: self.env.user
    )
    
    create_date = fields.Datetime(
        string='Created on',
        default=fields.Datetime.now
    )

    @api.constrains('user_id', 'group_id')
    def _check_user_or_group(self):
        """Ensure either user or group is specified, but not both"""
        for permission in self:
            if not permission.user_id and not permission.group_id:
                raise ValidationError(_('Either user or group must be specified.'))
            if permission.user_id and permission.group_id:
                raise ValidationError(_('Cannot specify both user and group.'))

    @api.constrains('expiry_date')
    def _check_expiry_date(self):
        """Ensure expiry date is in the future"""
        for permission in self:
            if permission.expiry_date and permission.expiry_date <= fields.Datetime.now():
                raise ValidationError(_('Expiry date must be in the future.'))

    def name_get(self):
        result = []
        for permission in self:
            target = permission.user_id.name if permission.user_id else permission.group_id.name
            name = f"{permission.article_id.name} - {target} ({permission.permission})"
            result.append((permission.id, name))
        return result

    @api.model_create_multi
    def create(self, vals_list):
        """Generate share token if needed"""
        for vals in vals_list:
            if not vals.get('share_token'):
                vals['share_token'] = self._generate_share_token()
        return super().create(vals_list)

    def _generate_share_token(self):
        """Generate a unique share token"""
        import secrets
        return secrets.token_urlsafe(32)

    def is_expired(self):
        """Check if permission has expired"""
        return self.expiry_date and self.expiry_date <= fields.Datetime.now()

    @api.model
    def check_article_access(self, article_id, user_id=None, permission='read'):
        """Check if user has permission to access an article"""
        if not user_id:
            user_id = self.env.user.id
        
        article = self.env['knowledge.article'].browse(article_id)
        user = self.env['res.users'].browse(user_id)
        
        # Check if user is the author
        if article.author_id.id == user_id:
            return True
        
        # Check article visibility
        if article.visibility == 'public':
            return True
        elif article.visibility == 'internal' and not user.share:
            return True
        elif article.visibility == 'portal' and user.share:
            return True
        
        # Check explicit permissions
        domain = [
            ('article_id', '=', article_id),
            ('permission', 'in', self._get_permission_hierarchy(permission)),
            '|',
            ('user_id', '=', user_id),
            ('group_id', 'in', user.groups_id.ids)
        ]
        
        permissions = self.search(domain)
        
        # Check if any permission is valid (not expired)
        for perm in permissions:
            if not perm.is_expired():
                return True
        
        return False

    def _get_permission_hierarchy(self, permission):
        """Get permission hierarchy - higher permissions include lower ones"""
        hierarchy = {
            'read': ['read', 'comment', 'write', 'manage'],
            'comment': ['comment', 'write', 'manage'],
            'write': ['write', 'manage'],
            'manage': ['manage'],
        }
        return hierarchy.get(permission, [permission])

    @api.model
    def get_user_articles(self, user_id=None, permission='read'):
        """Get articles accessible to a user"""
        if not user_id:
            user_id = self.env.user.id
        
        user = self.env['res.users'].browse(user_id)
        
        # Base domain for published articles
        domain = [
            ('stage', '=', 'published'),
            ('active', '=', True)
        ]
        
        # Add visibility conditions
        visibility_domain = []
        
        if user.share:  # Portal user
            visibility_domain.extend([
                ('visibility', 'in', ['public', 'portal']),
                ('author_id', '=', user_id)  # Own articles
            ])
        else:  # Internal user
            visibility_domain.extend([
                ('visibility', 'in', ['public', 'internal']),
                ('author_id', '=', user_id)  # Own articles
            ])
        
        # Add explicit permissions
        permission_articles = self.search([
            ('permission', 'in', self._get_permission_hierarchy(permission)),
            '|',
            ('user_id', '=', user_id),
            ('group_id', 'in', user.groups_id.ids)
        ]).mapped('article_id')
        
        if permission_articles:
            visibility_domain.append(('id', 'in', permission_articles.ids))
        
        # Combine domains
        final_domain = domain + [
            '|' * (len(visibility_domain) - 1)
        ] + visibility_domain if visibility_domain else domain
        
        return self.env['knowledge.article'].search(final_domain)

    def action_revoke(self):
        """Revoke this permission"""
        self.unlink()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_extend_expiry(self):
        """Extend expiry date by 30 days"""
        if self.expiry_date:
            self.expiry_date = fields.Datetime.now() + relativedelta(days=30)
        else:
            self.expiry_date = fields.Datetime.now() + relativedelta(days=30)


class KnowledgeShare(models.Model):
    _name = 'knowledge.share'
    _description = 'Knowledge Share Link'
    _rec_name = 'article_id'

    article_id = fields.Many2one(
        'knowledge.article',
        string='Article',
        required=True,
        ondelete='cascade'
    )
    
    share_token = fields.Char(
        string='Share Token',
        required=True,
        help='Unique token for this share link'
    )
    
    share_type = fields.Selection([
        ('public', 'Public Link'),
        ('protected', 'Protected Link'),
        ('temporary', 'Temporary Link'),
    ], string='Share Type', required=True, default='public')
    
    password = fields.Char(
        string='Password',
        help='Password for protected links'
    )
    
    expiry_date = fields.Datetime(
        string='Expiry Date',
        help='Date when this share link expires'
    )
    
    max_views = fields.Integer(
        string='Maximum Views',
        help='Maximum number of views allowed'
    )
    
    view_count = fields.Integer(
        string='View Count',
        default=0,
        help='Number of times this link has been used'
    )
    
    allow_download = fields.Boolean(
        string='Allow Download',
        default=True,
        help='Allow downloading the article'
    )
    
    allow_print = fields.Boolean(
        string='Allow Print',
        default=True,
        help='Allow printing the article'
    )
    
    track_views = fields.Boolean(
        string='Track Views',
        default=True,
        help='Track who views this article'
    )
    
    # Metadata
    create_uid = fields.Many2one(
        'res.users',
        string='Created by',
        default=lambda self: self.env.user
    )
    
    create_date = fields.Datetime(
        string='Created on',
        default=fields.Datetime.now
    )
    
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Generate share token if needed"""
        for vals in vals_list:
            if not vals.get('share_token'):
                vals['share_token'] = self._generate_share_token()
        return super().create(vals_list)

    def _generate_share_token(self):
        """Generate a unique share token"""
        import secrets
        return secrets.token_urlsafe(32)

    def is_valid(self):
        """Check if share link is still valid"""
        if not self.active:
            return False
        
        if self.expiry_date and self.expiry_date <= fields.Datetime.now():
            return False
        
        if self.max_views and self.view_count >= self.max_views:
            return False
        
        return True

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        
        # Deactivate if max views reached
        if self.max_views and self.view_count >= self.max_views:
            self.active = False

    def get_share_url(self):
        """Get the full share URL"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/knowledge/share/{self.share_token}"

    def action_copy_link(self):
        """Return share URL for copying"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Share Link'),
                'message': _('Link copied to clipboard: %s') % self.get_share_url(),
                'type': 'success',
            }
        }

    def action_disable(self):
        """Disable this share link"""
        self.active = False