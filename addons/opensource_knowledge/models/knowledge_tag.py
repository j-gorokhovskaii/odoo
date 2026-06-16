from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KnowledgeTag(models.Model):
    _name = 'knowledge.tag'
    _description = 'Knowledge Tag'
    _order = 'name'

    name = fields.Char(
        string='Tag Name',
        required=True,
        help='Name of the tag'
    )
    
    color = fields.Integer(
        string='Color',
        default=0,
        help='Color index for the tag'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of what this tag represents'
    )
    
    active = fields.Boolean(default=True)
    
    # Reverse relationship
    article_ids = fields.Many2many(
        'knowledge.article',
        string='Articles',
        help='Articles tagged with this tag'
    )
    
    # Statistics
    article_count = fields.Integer(
        string='Article Count',
        compute='_compute_article_count',
        store=True,
        help='Number of articles with this tag'
    )

    @api.depends('article_ids')
    def _compute_article_count(self):
        for tag in self:
            tag.article_count = len(tag.article_ids)

    template_ids = fields.Many2many(
        'knowledge.template',
        'knowledge_template_tag_rel',
        'tag_id',
        'template_id',
        string='Templates',
        help='Templates that use this tag by default'
    )

    @api.constrains('name')
    def _check_name_uniqueness(self):
        """Ensure tag names are unique"""
        for tag in self:
            if self.search_count([('name', '=ilike', tag.name), ('id', '!=', tag.id)]) > 0:
                raise ValidationError(_('Tag name must be unique.'))

    def name_get(self):
        result = []
        for tag in self:
            name = f"{tag.name} ({tag.article_count})" if tag.article_count else tag.name
            result.append((tag.id, name))
        return result

    def action_view_articles(self):
        """View all articles with this tag"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Articles tagged with %s') % self.name,
            'view_mode': 'tree,form',
            'res_model': 'knowledge.article',
            'domain': [('tag_ids', 'in', [self.id])],
            'context': {
                'default_tag_ids': [(6, 0, [self.id])],
            },
        }

    @api.model
    def get_popular_tags(self, limit=10):
        """Get most popular tags by article count"""
        return self.search([], order='article_count desc', limit=limit)

    @api.model
    def search_tags(self, search_term, limit=10):
        """Search tags by name"""
        return self.search([
            ('name', 'ilike', search_term)
        ], limit=limit)

    def merge_tags(self, target_tag):
        """Merge this tag into target tag"""
        if self == target_tag:
            raise ValidationError(_('Cannot merge tag with itself.'))
        
        # Move all articles to target tag
        for article in self.article_ids:
            article.tag_ids = [(3, self.id), (4, target_tag.id)]
        
        # Move all templates to target tag
        for template in self.template_ids:
            template.tag_ids = [(3, self.id), (4, target_tag.id)]
        
        # Delete this tag
        self.unlink()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Tags Merged'),
                'message': _('Tag has been merged into %s') % target_tag.name,
                'type': 'success',
            }
        }