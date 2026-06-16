# Quick Installation Guide

## If You're Getting RPC_ERROR During Installation

Follow these steps to resolve the issue:

### Step 1: Use the Simplified Version

The module now uses a simplified view file that should work without issues.

### Step 2: Clean Installation

1. **Uninstall the module** (if partially installed):
   - Go to Apps → Search for "Partner Date of Birth"
   - Click Uninstall if it appears

2. **Clear browser cache**:
   - Press Ctrl+F5 to hard refresh
   - Or clear browser cache completely

3. **Update module list**:
   - Go to Apps → Update Apps List
   - Click Update

4. **Install the module**:
   - Search for "Partner Date of Birth"
   - Click Install

### Step 3: If Still Having Issues

1. **Check file permissions**:
   ```bash
   # Ensure all files are readable
   chmod -R 755 /path/to/odoo/addons/partner_dob
   ```

2. **Restart Odoo server**:
   ```bash
   # Stop and restart Odoo
   sudo systemctl restart odoo
   # or restart your development server
   ```

3. **Check Odoo logs** for specific error messages

### Step 4: Verify Installation

1. **Go to Contacts** → **Customers**
2. **Create a new contact** or edit an existing one
3. **Look for the Date of Birth field** (only visible for individual contacts)
4. **Enter a birth date** and verify the age calculates automatically

## What the Module Adds

- **Date of Birth field** for individual contacts
- **Age field** (automatically calculated)
- **Age column** in contact list (optional)
- **Validation** to prevent future birth dates

## Troubleshooting

If you still encounter issues:

1. **Check the TROUBLESHOOTING.md file** for detailed solutions
2. **Use the simplified view file** (already configured)
3. **Test on a fresh database** if possible
4. **Check Odoo version compatibility** (designed for Odoo 18.0)

## Support

For additional help, refer to:
- TROUBLESHOOTING.md for detailed solutions
- README.md for feature documentation
- Odoo Community Forum for general Odoo issues 