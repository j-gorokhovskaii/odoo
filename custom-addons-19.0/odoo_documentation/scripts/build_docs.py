#!/usr/bin/env python3
"""
Build Odoo documentation using Sphinx and integrate into the module.
This properly handles all Sphinx directives and cross-references.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

def build_documentation():
    """Build documentation using Sphinx"""
    script_dir = Path(__file__).parent
    module_dir = script_dir.parent
    docs_source = module_dir.parent.parent / 'documentation'
    docs_dest = module_dir / 'static' / 'docs'
    
    if not docs_source.exists():
        print(f"Documentation source not found at {docs_source}")
        print("Please clone https://github.com/odoo/documentation.git to the odoo root directory")
        return False
    
    print(f"Building documentation from {docs_source}")
    
    # Create destination directory
    docs_dest.mkdir(parents=True, exist_ok=True)
    
    # Change to documentation directory
    os.chdir(docs_source)
    
    # Install dependencies if needed
    print("Installing documentation dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Build HTML documentation
    print("Building HTML documentation...")
    build_dir = docs_source / '_build' / 'html'
    
    # Clean previous build
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Run Sphinx build
    result = subprocess.run([
        sys.executable, "-m", "sphinx.cmd.build",
        "-b", "html",
        "-d", "_build/doctrees",
        ".", "_build/html"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Build errors:")
        print(result.stderr)
        return False
    
    print("Build completed successfully!")
    
    # Copy built documentation to module
    print(f"Copying documentation to {docs_dest}")
    if build_dir.exists():
        # Copy all HTML files
        for item in build_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, docs_dest)
            elif item.is_dir() and item.name not in ['_sources', '_static', '.doctrees']:
                dest_subdir = docs_dest / item.name
                if dest_subdir.exists():
                    shutil.rmtree(dest_subdir)
                shutil.copytree(item, dest_subdir)
        
        # Copy static files
        static_src = build_dir / '_static'
        static_dest = docs_dest / '_static'
        if static_src.exists():
            if static_dest.exists():
                shutil.rmtree(static_dest)
            shutil.copytree(static_src, static_dest)
    
    # Create a simple wrapper for iframe display
    create_wrapper_page(docs_dest)
    
    return True

def create_wrapper_page(docs_dest):
    """Create a wrapper page for the documentation"""
    wrapper_content = """<!DOCTYPE html>
<html>
<head>
    <title>Odoo Documentation</title>
    <meta charset="utf-8">
    <style>
        body { margin: 0; padding: 0; }
        .doc-wrapper { 
            display: flex; 
            height: 100vh;
        }
        .doc-frame {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>
    <div class="doc-wrapper">
        <iframe class="doc-frame" src="index.html"></iframe>
    </div>
</body>
</html>"""
    
    wrapper_file = docs_dest / 'wrapper.html'
    with open(wrapper_file, 'w', encoding='utf-8') as f:
        f.write(wrapper_content)

if __name__ == '__main__':
    os.chdir(Path(__file__).parent.parent.parent)  # Go to odoo root
    if build_documentation():
        print("\nDocumentation built and integrated successfully!")
        print("You can now install the odoo_documentation module in Odoo")
    else:
        print("\nDocumentation build failed!")
        sys.exit(1)