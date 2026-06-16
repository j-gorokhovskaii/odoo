from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KnowledgeCategory(models.Model):
    _name = 'knowledge.category'
    _description = 'Knowledge Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    _parent_name = 'parent_id'
    _parent_store = True

    # Basic Information
    name = fields.Char(
        string='Name',
        required=True,
        tracking=True,
        help='Category name'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of this category'
    )
    
    color = fields.Integer(
        string='Color',
        default=0,
        help='Color index for the category'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Used to order categories'
    )
    
    # Hierarchy
    parent_id = fields.Many2one(
        'knowledge.category',
        string='Parent Category',
        ondelete='cascade',
        tracking=True,
        help='Parent category for hierarchical organization'
    )
    
    child_ids = fields.One2many(
        'knowledge.category',
        'parent_id',
        string='Child Categories'
    )
    
    parent_path = fields.Char(index=True)
    
    # Articles
    article_ids = fields.One2many(
        'knowledge.article',
        'category_id',
        string='Articles',
        help='Articles in this category'
    )
    
    # Access Control
    visibility = fields.Selection([
        ('private', 'Private'),
        ('internal', 'Internal Users'),
        ('portal', 'Portal Users'),
        ('public', 'Public'),
    ], string='Visibility', default='internal', required=True, tracking=True)
    
    permission_ids = fields.One2many(
        'knowledge.category.permission',
        'category_id',
        string='Permissions'
    )
    
    # Manager
    manager_id = fields.Many2one(
        'res.users',
        string='Category Manager',
        tracking=True,
        help='User responsible for managing this category'
    )
    
    # Status
    active = fields.Boolean(default=True, tracking=True)
    
    # Computed Fields
    article_count = fields.Integer(
        string='Article Count',
        compute='_compute_article_count',
        store=True,
        help='Number of articles in this category and subcategories'
    )
    
    direct_article_count = fields.Integer(
        string='Direct Articles',
        compute='_compute_direct_article_count',
        store=True,
        help='Number of articles directly in this category'
    )
    
    has_children = fields.Boolean(
        string='Has Subcategories',
        compute='_compute_has_children'
    )
    
    level = fields.Integer(
        string='Level',
        compute='_compute_level',
        store=True,
        help='Level in the hierarchy (0 for root categories)'
    )
    
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        recursive=True,
        store=True,
        help='Complete category path'
    )

    @api.depends('article_ids', 'child_ids.article_count')
    def _compute_article_count(self):
        for category in self:
            count = len(category.article_ids)
            for child in category.child_ids:
                count += child.article_count
            category.article_count = count

    @api.depends('article_ids')
    def _compute_direct_article_count(self):
        for category in self:
            category.direct_article_count = len(category.article_ids)

    @api.depends('child_ids')
    def _compute_has_children(self):
        for category in self:
            category.has_children = bool(category.child_ids)

    @api.depends('parent_id')
    def _compute_level(self):
        for category in self:
            level = 0
            parent = category.parent_id
            while parent:
                level += 1
                parent = parent.parent_id
            category.level = level

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = f"{category.parent_id.complete_name} / {category.name}"
            else:
                category.complete_name = category.name

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        """Prevent circular references in parent-child relationships"""
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive category hierarchies.'))

    @api.constrains('name', 'parent_id')
    def _check_name_uniqueness(self):
        """Ensure category names are unique within the same parent"""
        for category in self:
            domain = [
                ('name', '=', category.name),
                ('parent_id', '=', category.parent_id.id if category.parent_id else False),
                ('id', '!=', category.id)
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(_('Category name must be unique within the same parent category.'))

    def name_get(self):
        """Return category name with parent hierarchy"""
        result = []
        for category in self:
            result.append((category.id, category.complete_name))
        return result

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=100, order=None):
        """Search in both name and complete_name"""
        domain = domain or []
        if name:
            domain = [
                '|',
                ('name', operator, name),
                ('complete_name', operator, name)
            ] + domain
        return self._search(domain, limit=limit, order=order)

    def action_view_articles(self):
        """View all articles in this category and subcategories"""
        # Get all subcategory IDs
        subcategory_ids = self.search([('parent_path', '=like', self.parent_path + '%')]).ids
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Articles in %s') % self.complete_name,
            'view_mode': 'tree,form',
            'res_model': 'knowledge.article',
            'domain': [('category_id', 'in', subcategory_ids)],
            'context': {
                'default_category_id': self.id,
                'search_default_category_id': self.id,
            },
        }

    def action_create_article(self):
        """Create a new article in this category"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Article'),
            'view_mode': 'form',
            'res_model': 'knowledge.article',
            'target': 'current',
            'context': {
                'default_category_id': self.id,
            },
        }

    def get_category_tree(self):
        """Get category tree structure for frontend"""
        def build_tree(categories, parent_id=False):
            tree = []
            for category in categories.filtered(lambda c: c.parent_id.id == parent_id):
                tree.append({
                    'id': category.id,
                    'name': category.name,
                    'article_count': category.direct_article_count,
                    'children': build_tree(categories, category.id)
                })
            return tree
        
        all_categories = self.search([('active', '=', True)])
        return build_tree(all_categories)


class KnowledgeCategoryPermission(models.Model):
    _name = 'knowledge.category.permission'
    _description = 'Knowledge Category Permission'
    _rec_name = 'category_id'

    category_id = fields.Many2one(
        'knowledge.category',
        string='Category',
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
        ('create', 'Create'),
        ('manage', 'Manage'),
    ], string='Permission', required=True, default='read')
    
    inherit_to_children = fields.Boolean(
        string='Inherit to Subcategories',
        default=True,
        help='Apply this permission to all subcategories'
    )

    @api.constrains('user_id', 'group_id')
    def _check_user_or_group(self):
        """Ensure either user or group is specified, but not both"""
        for permission in self:
            if not permission.user_id and not permission.group_id:
                raise ValidationError(_('Either user or group must be specified.'))
            if permission.user_id and permission.group_id:
                raise ValidationError(_('Cannot specify both user and group.'))

    def name_get(self):
        result = []
        for permission in self:
            target = permission.user_id.name if permission.user_id else permission.group_id.name
            name = f"{permission.category_id.name} - {target} ({permission.permission})"
            result.append((permission.id, name))
        return result