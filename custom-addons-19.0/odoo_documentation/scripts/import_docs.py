#!/usr/bin/env python3
"""
Script to import Odoo documentation into the module.
Converts RST files to HTML and copies them to the static directory.
"""
import os
import shutil
import sys
from pathlib import Path
import subprocess

def setup_sphinx():
    """Install required dependencies"""
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sphinx>=4.3.2", "docutils>=0.17", "pygments", "rst2html5"])

def convert_rst_to_html(rst_file, output_dir):
    """Convert RST file to HTML using sphinx.cmd.build"""
    output_file = output_dir / rst_file.stem / 'index.html'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # For now, just copy the RST content wrapped in HTML
        # A full Sphinx build would be more complex
        with open(rst_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic HTML wrapper
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{rst_file.stem}</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="/odoo_documentation/static/src/css/documentation.css">
</head>
<body>
    <div class="rst-content">
        <h1>{rst_file.stem.replace('_', ' ').title()}</h1>
        <pre>{content}</pre>
    </div>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
    except Exception as e:
        print(f"Warning: Could not fully process {rst_file}: {e}")
        return False

def import_documentation():
    """Import documentation from the cloned repository"""
    # Get paths
    script_dir = Path(__file__).parent
    module_dir = script_dir.parent
    docs_source = module_dir.parent.parent / 'documentation'
    docs_dest = module_dir / 'static' / 'docs'
    
    if not docs_source.exists():
        print(f"Documentation source not found at {docs_source}")
        print("Please clone https://github.com/odoo/documentation.git to the odoo root directory")
        return False
    
    print(f"Importing documentation from {docs_source}")
    
    # Create destination directory
    docs_dest.mkdir(parents=True, exist_ok=True)
    
    # Copy static assets
    static_source = docs_source / 'static'
    static_dest = docs_dest / 'static'
    if static_source.exists():
        print("Copying static assets...")
        shutil.copytree(static_source, static_dest, dirs_exist_ok=True)
    
    # Process RST files
    content_dir = docs_source / 'content'
    if not content_dir.exists():
        print(f"Content directory not found at {content_dir}")
        return False
    
    # Create documentation structure
    doc_structure = {
        'applications': [],
        'administration': [],
        'developer': [],
        'contributing': []
    }
    
    # Convert RST files to HTML
    print("Converting RST files to HTML...")
    total_files = 0
    converted_files = 0
    
    for category in doc_structure.keys():
        category_dir = content_dir / category
        if category_dir.exists():
            category_dest = docs_dest / category
            category_dest.mkdir(parents=True, exist_ok=True)
            
            # Copy and convert all RST files
            for rst_file in category_dir.rglob('*.rst'):
                total_files += 1
                rel_path = rst_file.relative_to(category_dir)
                
                # Create subdirectory structure
                dest_subdir = category_dest / rel_path.parent
                dest_subdir.mkdir(parents=True, exist_ok=True)
                
                # Convert RST to HTML
                if convert_rst_to_html(rst_file, dest_subdir):
                    converted_files += 1
                    doc_structure[category].append({
                        'path': str(rel_path),
                        'title': rst_file.stem.replace('_', ' ').title()
                    })
                
                # Copy associated images
                img_dir = rst_file.parent
                for img_ext in ['*.png', '*.jpg', '*.svg', '*.gif']:
                    for img_file in img_dir.glob(img_ext):
                        shutil.copy2(img_file, dest_subdir)
    
    print(f"\nConverted {converted_files}/{total_files} documentation files")
    
    # Generate index file
    generate_index(docs_dest, doc_structure)
    
    return True

def generate_index(docs_dest, doc_structure):
    """Generate an index HTML file for navigation"""
    index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Odoo Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #714b9d; }
        h2 { color: #875a7b; margin-top: 30px; }
        ul { list-style-type: none; padding-left: 20px; }
        li { margin: 5px 0; }
        a { color: #714b9d; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Odoo 18.0 Documentation</h1>
"""
    
    for category, docs in doc_structure.items():
        if docs:
            index_content += f"    <h2>{category.title()}</h2>\n    <ul>\n"
            for doc in docs:
                doc_path = f"{category}/{doc['path'].replace('.rst', '')}/index.html"
                index_content += f'        <li><a href="{doc_path}">{doc["title"]}</a></li>\n'
            index_content += "    </ul>\n"
    
    index_content += """</body>
</html>"""
    
    index_file = docs_dest / 'index.html'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"Generated index file at {index_file}")

if __name__ == '__main__':
    setup_sphinx()
    if import_documentation():
        print("\nDocumentation imported successfully!")
        print("You can now install the odoo_documentation module in Odoo")
    else:
        print("\nDocumentation import failed!")
        sys.exit(1)