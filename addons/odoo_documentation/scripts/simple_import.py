#!/usr/bin/env python3
"""
Simple documentation import that copies RST files and creates a basic viewer.
This avoids complex Sphinx dependencies.
"""
import os
import shutil
import sys
from pathlib import Path
import re

def clean_rst_content(content):
    """Clean RST content for basic display"""
    # Remove Sphinx-specific directives
    content = re.sub(r'\.\. toctree::\s*\n(?:\s+[^\n]*\n)*', '', content)
    content = re.sub(r':([a-z]+):`([^`]+)`', r'\\2', content)  # Remove roles
    content = re.sub(r'\.\. [a-z-]+::[^\n]*\n(?:\s+[^\n]*\n)*', '', content)  # Remove directives
    
    return content

def convert_rst_to_html(rst_file, output_file):
    """Convert RST to basic HTML"""
    try:
        with open(rst_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean the content
        content = clean_rst_content(content)
        
        # Get title from first line or filename
        lines = content.split('\n')
        title = rst_file.stem.replace('_', ' ').title()
        if lines and not lines[0].startswith('='):
            title = lines[0].strip()
        
        # Create basic HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="utf-8">
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3 {{ color: #714b9d; }}
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        .rst-content {{
            background: white;
            padding: 20px;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="rst-content">
        <h1>{title}</h1>
        <pre>{content}</pre>
    </div>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
    except Exception as e:
        print(f"Error converting {rst_file}: {e}")
        return False

def create_index_page(docs_dest, structure):
    """Create main index page"""
    content = """<!DOCTYPE html>
<html>
<head>
    <title>Odoo 18.0 Documentation</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8f9fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #714b9d;
            text-align: center;
            margin-bottom: 40px;
        }
        .category {
            background: white;
            margin-bottom: 30px;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .category h2 {
            color: #875a7b;
            margin-top: 0;
            border-bottom: 2px solid #714b9d;
            padding-bottom: 10px;
        }
        .doc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .doc-item {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #714b9d;
        }
        .doc-item a {
            color: #714b9d;
            text-decoration: none;
            font-weight: 500;
        }
        .doc-item a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Odoo 18.0 Documentation</h1>
"""
    
    for category, docs in structure.items():
        if docs:
            content += f"""
        <div class="category">
            <h2>{category.title()}</h2>
            <div class="doc-grid">
"""
            for doc in docs:
                content += f"""
                <div class="doc-item">
                    <a href="{doc['file']}" target="_blank">{doc['title']}</a>
                </div>
"""
            content += """
            </div>
        </div>
"""
    
    content += """
    </div>
</body>
</html>"""
    
    index_file = docs_dest / 'index.html'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)

def import_documentation():
    """Import and process documentation"""
    script_dir = Path(__file__).parent
    module_dir = script_dir.parent
    docs_source = module_dir.parent.parent / 'documentation'
    docs_dest = module_dir / 'static' / 'docs'
    
    if not docs_source.exists():
        print(f"Documentation source not found at {docs_source}")
        return False
    
    print(f"Importing documentation from {docs_source}")
    
    # Create destination
    docs_dest.mkdir(parents=True, exist_ok=True)
    
    # Process main categories
    structure = {
        'applications': [],
        'administration': [],
        'developer': [],
        'contributing': []
    }
    
    content_dir = docs_source / 'content'
    
    for category in structure.keys():
        category_dir = content_dir / category
        if not category_dir.exists():
            continue
            
        category_dest = docs_dest / category
        category_dest.mkdir(parents=True, exist_ok=True)
        
        # Process RST files
        for rst_file in category_dir.rglob('*.rst'):
            rel_path = rst_file.relative_to(category_dir)
            
            # Create output path
            html_file = category_dest / rel_path.with_suffix('.html')
            html_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to HTML
            if convert_rst_to_html(rst_file, html_file):
                rel_html_path = html_file.relative_to(docs_dest)
                structure[category].append({
                    'title': rst_file.stem.replace('_', ' ').title(),
                    'file': str(rel_html_path).replace('\\\\', '/')
                })
    
    # Create index
    create_index_page(docs_dest, structure)
    
    # Copy static assets if they exist
    static_source = docs_source / 'static'
    if static_source.exists():
        static_dest = docs_dest / 'static'
        if static_dest.exists():
            shutil.rmtree(static_dest)
        shutil.copytree(static_source, static_dest)
    
    return True

if __name__ == '__main__':
    if import_documentation():
        print("\\nDocumentation imported successfully!")
        print("You can now restart Odoo and access the documentation.")
    else:
        print("\\nDocumentation import failed!")
        sys.exit(1)