from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Knowledge Statistics
    knowledge_article_count = fields.Integer(
        string='Articles Authored',
        compute='_compute_knowledge_stats',
        help='Number of articles authored by this user'
    )
    
    knowledge_article_views = fields.Integer(
        string='Total Article Views',
        compute='_compute_knowledge_stats',
        help='Total views of articles authored by this user'
    )
    
    knowledge_contribution_score = fields.Float(
        string='Contribution Score',
        compute='_compute_knowledge_stats',
        help='Knowledge contribution score based on articles and engagement'
    )
    
    # Preferences
    knowledge_default_category_id = fields.Many2one(
        'knowledge.category',
        string='Default Category',
        help='Default category for new articles'
    )
    
    knowledge_default_visibility = fields.Selection([
        ('private', 'Private'),
        ('internal', 'Internal Users'),
        ('portal', 'Portal Users'),
        ('public', 'Public'),
    ], string='Default Visibility', default='internal', 
    help='Default visibility for new articles')
    
    knowledge_email_notifications = fields.Boolean(
        string='Email Notifications',
        default=True,
        help='Receive email notifications for knowledge activities'
    )
    
    knowledge_digest_frequency = fields.Selection([
        ('never', 'Never'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], string='Digest Frequency', default='weekly',
    help='Frequency of knowledge digest emails')

    # Reverse relationships
    authored_articles = fields.One2many(
        'knowledge.article',
        'author_id',
        string='Authored Articles'
    )
    
    review_articles = fields.Many2many(
        'knowledge.article',
        'knowledge_article_reviewer_rel',
        'user_id',
        'article_id',
        string='Articles to Review'
    )
    
    favorite_articles = fields.Many2many(
        'knowledge.article',
        'knowledge_user_favorite_rel',
        'user_id',
        'article_id',
        string='Favorite Articles'
    )

    @api.depends('authored_articles', 'authored_articles.view_count')
    def _compute_knowledge_stats(self):
        for user in self:
            articles = user.authored_articles.filtered(lambda a: a.stage == 'published')
            user.knowledge_article_count = len(articles)
            user.knowledge_article_views = sum(articles.mapped('view_count'))
            
            # Calculate contribution score
            # Base score: 10 points per published article
            # Bonus: 1 point per 10 views
            # Bonus: 5 points per article with likes > 5
            base_score = len(articles) * 10
            view_bonus = user.knowledge_article_views // 10
            popular_bonus = len(articles.filtered(lambda a: a.like_count > 5)) * 5
            
            user.knowledge_contribution_score = base_score + view_bonus + popular_bonus

    def action_view_authored_articles(self):
        """View articles authored by this user"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('My Articles'),
            'view_mode': 'tree,form',
            'res_model': 'knowledge.article',
            'domain': [('author_id', '=', self.id)],
            'context': {
                'default_author_id': self.id,
            },
        }

    def action_view_articles_to_review(self):
        """View articles assigned for review"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Articles to Review'),
            'view_mode': 'tree,form',
            'res_model': 'knowledge.article',
            'domain': [
                ('reviewer_ids', 'in', [self.id]),
                ('stage', '=', 'review')
            ],
        }

    def action_view_favorite_articles(self):
        """View favorite articles"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Favorite Articles'),
            'view_mode': 'tree,form',
            'res_model': 'knowledge.article',
            'domain': [('id', 'in', self.favorite_articles.ids)],
        }

    def get_knowledge_dashboard_data(self):
        """Get data for knowledge dashboard"""
        return {
            'authored_count': self.knowledge_article_count,
            'total_views': self.knowledge_article_views,
            'contribution_score': self.knowledge_contribution_score,
            'articles_to_review': len(self.review_articles.filtered(lambda a: a.stage == 'review')),
            'favorite_count': len(self.favorite_articles),
            'recent_articles': self.authored_articles.filtered(
                lambda a: a.stage == 'published'
            ).sorted('publish_date', reverse=True)[:5],
        }

    def toggle_article_favorite(self, article_id):
        """Toggle favorite status for an article"""
        article = self.env['knowledge.article'].browse(article_id)
        if article in self.favorite_articles:
            self.favorite_articles = [(3, article_id)]
            return {'favorited': False}
        else:
            self.favorite_articles = [(4, article_id)]
            return {'favorited': True}

    @api.model
    def get_knowledge_leaders(self, limit=10):
        """Get top knowledge contributors"""
        return self.search([
            ('knowledge_contribution_score', '>', 0)
        ], order='knowledge_contribution_score desc', limit=limit)

    def send_knowledge_digest(self):
        """Send knowledge digest email to user"""
        if not self.knowledge_email_notifications or self.knowledge_digest_frequency == 'never':
            return
        
        # Get recent articles and activities
        from datetime import timedelta
        days_mapping = {'daily': 1, 'weekly': 7, 'monthly': 30}
        days_back = days_mapping.get(self.knowledge_digest_frequency, 7)
        
        recent_articles = self.env['knowledge.article'].search([
            ('stage', '=', 'published'),
            ('publish_date', '>=', fields.Datetime.now() - timedelta(days=days_back))
        ], order='publish_date desc', limit=10)
        
        # Send digest email
        template = self.env.ref('opensource_knowledge.knowledge_digest_email_template', raise_if_not_found=False)
        if template:
            template.with_context(
                user=self,
                recent_articles=recent_articles
            ).send_mail(self.id, force_send=True)

    @api.model
    def send_all_knowledge_digests(self):
        """Send digest emails to all users (called by cron)"""
        today = fields.Date.today()
        
        # Daily digests
        daily_users = self.search([
            ('knowledge_digest_frequency', '=', 'daily'),
            ('knowledge_email_notifications', '=', True)
        ])
        for user in daily_users:
            user.send_knowledge_digest()
        
        # Weekly digests (on Monday)
        if today.weekday() == 0:  # Monday
            weekly_users = self.search([
                ('knowledge_digest_frequency', '=', 'weekly'),
                ('knowledge_email_notifications', '=', True)
            ])
            for user in weekly_users:
                user.send_knowledge_digest()
        
        # Monthly digests (on 1st of month)
        if today.day == 1:
            monthly_users = self.search([
                ('knowledge_digest_frequency', '=', 'monthly'),
                ('knowledge_email_notifications', '=', True)
            ])
            for user in monthly_users:
                user.send_knowledge_digest()