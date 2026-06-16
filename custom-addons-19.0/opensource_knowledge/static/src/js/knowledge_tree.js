/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class KnowledgeTree extends Component {
    static template = "opensource_knowledge.KnowledgeTree";
    
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        
        this.state = useState({
            categories: [],
            articles: [],
            expandedCategories: new Set(),
            searchTerm: '',
            loading: true
        });
        
        onWillStart(this.onWillStart);
    }
    
    async onWillStart() {
        await this.loadCategories();
        await this.loadArticles();
        this.state.loading = false;
    }
    
    async loadCategories() {
        try {
            const categories = await this.orm.searchRead(
                "knowledge.category",
                [['active', '=', true]],
                ['id', 'name', 'parent_id', 'article_count', 'color', 'sequence'],
                { order: 'sequence, name' }
            );
            this.state.categories = this.buildCategoryTree(categories);
        } catch (error) {
            console.error('Failed to load categories:', error);
            this.notification.add('Failed to load categories', { type: 'danger' });
        }
    }
    
    async loadArticles() {
        try {
            const articles = await this.orm.searchRead(
                "knowledge.article",
                [['stage', '=', 'published'], ['active', '=', true]],
                ['id', 'name', 'category_id', 'parent_id', 'view_count', 'author_id', 'sequence'],
                { order: 'sequence, name' }
            );
            this.state.articles = this.buildArticleTree(articles);
        } catch (error) {
            console.error('Failed to load articles:', error);
            this.notification.add('Failed to load articles', { type: 'danger' });
        }
    }
    
    buildCategoryTree(categories) {
        const categoryMap = new Map();
        const rootCategories = [];
        
        // Create category objects
        categories.forEach(cat => {
            categoryMap.set(cat.id, {
                ...cat,
                children: []
            });
        });
        
        // Build hierarchy
        categories.forEach(cat => {
            const category = categoryMap.get(cat.id);
            if (cat.parent_id) {
                const parent = categoryMap.get(cat.parent_id[0]);
                if (parent) {
                    parent.children.push(category);
                }
            } else {
                rootCategories.push(category);
            }
        });
        
        return rootCategories;
    }
    
    buildArticleTree(articles) {
        const articleMap = new Map();
        const rootArticles = [];
        
        // Create article objects
        articles.forEach(art => {
            articleMap.set(art.id, {
                ...art,
                children: []
            });
        });
        
        // Build hierarchy
        articles.forEach(art => {
            const article = articleMap.get(art.id);
            if (art.parent_id) {
                const parent = articleMap.get(art.parent_id[0]);
                if (parent) {
                    parent.children.push(article);
                }
            } else {
                rootArticles.push(article);
            }
        });
        
        return rootArticles;
    }
    
    toggleCategory(categoryId) {
        if (this.state.expandedCategories.has(categoryId)) {
            this.state.expandedCategories.delete(categoryId);
        } else {
            this.state.expandedCategories.add(categoryId);
        }
    }
    
    isCategoryExpanded(categoryId) {
        return this.state.expandedCategories.has(categoryId);
    }
    
    async openArticle(articleId) {
        try {
            // Increment view count
            await this.orm.call("knowledge.article", "increment_view_count", [articleId]);
            
            // Open article form
            await this.action.doAction({
                type: 'ir.actions.act_window',
                name: 'Knowledge Article',
                res_model: 'knowledge.article',
                res_id: articleId,
                view_mode: 'form',
                target: 'current'
            });
        } catch (error) {
            console.error('Failed to open article:', error);
            this.notification.add('Failed to open article', { type: 'danger' });
        }
    }
    
    async createArticle(categoryId = null) {
        try {
            const context = {
                default_stage: 'draft',
                default_author_id: this.env.services.user.userId,
                form_view_initial_mode: 'edit'
            };
            
            if (categoryId) {
                context.default_category_id = categoryId;
            }
            
            await this.action.doAction({
                type: 'ir.actions.act_window',
                name: 'New Article',
                res_model: 'knowledge.article',
                view_mode: 'form',
                target: 'current',
                context: context
            });
        } catch (error) {
            console.error('Failed to create article:', error);
            this.notification.add('Failed to create article', { type: 'danger' });
        }
    }
    
    async searchArticles() {
        if (!this.state.searchTerm.trim()) {
            await this.loadArticles();
            return;
        }
        
        try {
            const articles = await this.orm.call(
                "knowledge.article",
                "search_articles",
                [this.state.searchTerm, null, null, 20]
            );
            
            this.state.articles = articles.map(art => ({
                ...art,
                children: []
            }));
        } catch (error) {
            console.error('Search failed:', error);
            this.notification.add('Search failed', { type: 'danger' });
        }
    }
    
    onSearchInput(event) {
        this.state.searchTerm = event.target.value;
        // Debounce search
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }
        this.searchTimeout = setTimeout(() => {
            this.searchArticles();
        }, 500);
    }
    
    clearSearch() {
        this.state.searchTerm = '';
        this.loadArticles();
    }
    
    getArticlesByCategory(categoryId) {
        return this.state.articles.filter(article => 
            article.category_id && article.category_id[0] === categoryId
        );
    }
    
    getCategoryColor(color) {
        const colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#F4A460', '#87CEEB', '#FFB6C1', '#98FB98'
        ];
        return colors[color % colors.length] || '#6c757d';
    }
    
    async refresh() {
        this.state.loading = true;
        await this.loadCategories();
        await this.loadArticles();
        this.state.loading = false;
        this.notification.add('Knowledge tree refreshed', { type: 'success' });
    }
}

// Register the component
registry.category("actions").add("knowledge_tree", KnowledgeTree);