from odoo import http
from odoo.http import request
import os
from pathlib import Path

class DocumentationController(http.Controller):
    
    @http.route('/documentation', type='http', auth='user', website=True)
    def documentation_index(self, **kwargs):
        """Main documentation page"""
        return request.render('odoo_documentation.documentation_index')
    
    @http.route('/documentation/view/<path:doc_path>', type='http', auth='user', website=True)
    def documentation_view(self, doc_path, **kwargs):
        """View a specific documentation page"""
        # Security: ensure path doesn't escape the docs directory
        module_path = Path(request.env['ir.module.module'].search([('name', '=', 'odoo_documentation')]).path)
        docs_path = module_path / 'static' / 'docs'
        
        # Normalize and validate the path
        safe_path = docs_path / doc_path
        try:
            safe_path = safe_path.resolve()
            if not str(safe_path).startswith(str(docs_path)):
                return request.not_found()
        except:
            return request.not_found()
        
        # Read the HTML content
        if safe_path.exists() and safe_path.is_file():
            with open(safe_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return request.render('odoo_documentation.documentation_viewer', {
                'doc_content': content,
                'doc_title': doc_path.split('/')[-1].replace('.html', '').replace('_', ' ').title()
            })
        else:
            return request.not_found()