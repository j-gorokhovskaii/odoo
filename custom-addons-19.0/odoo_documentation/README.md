# Odoo Documentation Module

This module integrates the official Odoo documentation directly into your Odoo instance, allowing users to access documentation without leaving the application.

## Features

- Access complete Odoo 18.0 documentation within your instance
- Organized navigation by category (Applications, Administration, Developer, Contributing)
- Fast local access without internet dependency
- Responsive design that works on all devices
- Integrated with Odoo's menu system

## Installation Steps

1. **Ensure the documentation is cloned** (you've already done this):
   ```bash
   cd /path/to/odoo
   git clone https://github.com/odoo/documentation.git
   ```

2. **Run the import script** to process and copy documentation:
   ```bash
   cd addons/odoo_documentation
   python scripts/import_docs.py
   ```

3. **Update the module list** in Odoo:
   - Go to Apps menu
   - Click "Update Apps List"
   - Search for "Odoo Documentation"

4. **Install the module**:
   - Click Install on the Odoo Documentation module

## Usage

After installation:
1. A new "Documentation" menu item will appear in the main menu
2. Click on it to access the documentation viewer
3. Use the navigation panel to browse different sections
4. Documentation is displayed in an embedded viewer

## Module Structure

```
odoo_documentation/
├── controllers/          # Web controllers for serving documentation
├── scripts/             # Import script for processing docs
├── security/            # Access rights
├── static/
│   ├── docs/           # Processed documentation (generated)
│   └── src/
│       └── css/        # Styling for documentation viewer
└── views/              # Menu items and templates
```

## Troubleshooting

- If the import script fails, ensure you have the required Python packages:
  ```bash
  pip install sphinx docutils pygments
  ```

- If documentation doesn't display, check that the import script completed successfully
- For permission issues, ensure the user has access to the Documentation menu

## Notes

- The documentation is stored statically, so updates require re-running the import script
- Large documentation sets may take time to process initially
- Images and assets from the documentation are preserved