# Troubleshooting Guide: Partner Date of Birth Module

## Common Installation Issues and Solutions

### 1. RPC_ERROR: Odoo Server Error - ParseError

**Error Message:**
```
odoo.tools.convert.ParseError: while parsing file:/path/to/partner_dob/views/res_partner_views.xml:79
Error while parsing or validating view:
Element '<xpath expr="//field[@name='phone']">' cannot be located in parent view
```

**Cause:** The XPath expression is trying to find a field that doesn't exist in the parent view.

**Solution:**
1. **Use the simplified view file**: Replace `res_partner_views.xml` with `res_partner_views_simple.xml`
2. **Update manifest**: Change the data file reference in `__manifest__.py`:

```python
'data': [
    'views/res_partner_views_simple.xml',  # Use simplified version
],
```

### 2. Module Not Appearing in Apps List

**Cause:** Module not properly detected by Odoo.

**Solution:**
1. **Check file permissions**: Ensure all files are readable
2. **Verify manifest syntax**: Check `__manifest__.py` for syntax errors
3. **Update module list**: Go to Apps → Update Apps List
4. **Check addons path**: Ensure module is in the correct addons directory

### 3. Fields Not Visible After Installation

**Cause:** View inheritance issues or cache problems.

**Solution:**
1. **Clear browser cache**: Hard refresh (Ctrl+F5)
2. **Restart Odoo server**: Stop and restart the Odoo service
3. **Update module**: Go to Apps → Update Apps List → Update
4. **Check user permissions**: Ensure you have proper access rights

### 4. Age Not Calculating

**Cause:** Computed field not working properly.

**Solution:**
1. **Check birth date format**: Ensure valid date is entered
2. **Refresh page**: Age is calculated on-the-fly
3. **Check for errors**: Look in browser console for JavaScript errors
4. **Verify model**: Check if the model extension is working

### 5. Database Migration Issues

**Cause:** Database schema conflicts or missing dependencies.

**Solution:**
1. **Backup database**: Always backup before updates
2. **Check dependencies**: Ensure `base` and `contacts` modules are installed
3. **Manual migration**: If needed, run database updates manually
4. **Fresh installation**: Consider testing on a fresh database

## Step-by-Step Recovery Process

### If Module Installation Fails:

1. **Uninstall the module** (if partially installed):
   ```bash
   # Go to Apps → Search for "Partner Date of Birth" → Uninstall
   ```

2. **Use simplified version**:
   - Replace `views/res_partner_views.xml` with `views/res_partner_views_simple.xml`
   - Update `__manifest__.py` to reference the simplified file

3. **Clear Odoo cache**:
   ```bash
   # Stop Odoo server
   # Delete cache files (if any)
   # Restart Odoo server
   ```

4. **Reinstall module**:
   - Go to Apps → Update Apps List
   - Search for "Partner Date of Birth"
   - Install the module

### If Views Don't Work:

1. **Check view inheritance**:
   - Verify the parent view exists
   - Check XPath expressions
   - Use simpler XPath expressions

2. **Test with minimal view**:
   ```xml
   <record id="test_view" model="ir.ui.view">
       <field name="name">test.view</field>
       <field name="model">res.partner</field>
       <field name="inherit_id" ref="base.view_partner_form"/>
       <field name="arch" type="xml">
           <xpath expr="//field[@name='name']" position="after">
               <field name="birthdate"/>
           </xpath>
       </field>
   </record>
   ```

3. **Check Odoo logs**:
   - Look for specific error messages
   - Check for view validation errors

## Alternative Installation Methods

### Method 1: Manual Installation (Recommended)

1. **Copy files manually**:
   ```bash
   cp -r partner_dob /path/to/odoo/addons/
   ```

2. **Set proper permissions**:
   ```bash
   chmod -R 755 /path/to/odoo/addons/partner_dob
   ```

3. **Restart Odoo server**:
   ```bash
   sudo systemctl restart odoo
   # or
   ./odoo-bin -c odoo.conf
   ```

### Method 2: Development Installation

1. **Install in development mode**:
   ```bash
   ./odoo-bin -d your_database -i partner_dob --dev=all
   ```

2. **Check for errors in console output**

3. **Fix any issues and restart**

## Debugging Tips

### 1. Enable Developer Mode

1. Go to Settings → Activate Developer Mode
2. This gives access to advanced debugging features

### 2. Check Odoo Logs

1. **Enable debug logging**:
   ```bash
   ./odoo-bin -d your_database --log-level=debug
   ```

2. **Look for specific errors**:
   - View parsing errors
   - Model loading errors
   - Database migration errors

### 3. Test Individual Components

1. **Test model separately**:
   ```python
   # In Odoo shell
   env['res.partner'].create({
       'name': 'Test Contact',
       'birthdate': '1990-01-01',
   })
   ```

2. **Test view inheritance**:
   - Create minimal test views
   - Verify XPath expressions work

### 4. Browser Developer Tools

1. **Check console for JavaScript errors**
2. **Inspect network requests**
3. **Check for RPC errors**

## Common XPath Issues

### 1. Field Not Found

**Problem**: `Element cannot be located in parent view`

**Solution**: Use more specific XPath expressions:
```xml
<!-- Instead of -->
<xpath expr="//field[@name='phone']" position="after">

<!-- Use -->
<xpath expr="//field[@name='category_id']" position="after">
```

### 2. Multiple Elements Found

**Problem**: XPath matches multiple elements

**Solution**: Make XPath more specific:
```xml
<!-- Instead of -->
<xpath expr="//field[@name='email']" position="after">

<!-- Use -->
<xpath expr="//group//field[@name='email']" position="after">
```

### 3. View Inheritance Order

**Problem**: Views not inheriting in correct order

**Solution**: Set proper priority:
```xml
<record id="view_partner_form_inherit_dob" model="ir.ui.view">
    <field name="priority" eval="100"/>
    <!-- ... rest of view definition -->
</record>
```

## Getting Help

If you continue to experience issues:

1. **Check Odoo Community Forum**: [https://www.odoo.com/forum/help-1](https://www.odoo.com/forum/help-1)
2. **Review Odoo Documentation**: [https://www.odoo.com/documentation/18.0/developer.html](https://www.odoo.com/documentation/18.0/developer.html)
3. **Check Module Logs**: Look for specific error messages
4. **Test on Fresh Installation**: Try on a clean Odoo instance

## Prevention Tips

1. **Always backup before installing modules**
2. **Test on development environment first**
3. **Use version control for custom modules**
4. **Keep Odoo and modules updated**
5. **Monitor logs regularly** 