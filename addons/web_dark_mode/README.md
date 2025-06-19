# Dark Mode Toggle for Odoo 18

A comprehensive dark mode module for Odoo 18 that provides a seamless dark theme experience with user preference persistence.

## 🌟 Features

### Dark Theme
- **Comprehensive Styling**: Complete dark theme that covers all Odoo interface elements
- **Smooth Transitions**: Elegant transitions between light and dark modes
- **Responsive Design**: Works perfectly on all screen sizes and devices
- **Accessibility**: Maintains proper contrast ratios for readability

### Toggle Functionality
- **System Tray Integration**: Toggle button appears in the top navigation bar
- **Icon Changes**: Moon icon for light mode, sun icon for dark mode
- **Tooltips**: Helpful tooltips explaining the current mode and action
- **Keyboard Accessible**: Full keyboard navigation support

### User Preference
- **Local Storage**: User preference is stored in browser's local storage
- **Session Persistence**: Theme preference persists across browser sessions
- **Per-User**: Each user can have their own theme preference
- **Fallback Handling**: Graceful fallback if local storage is unavailable

## 🚀 Installation

### Method 1: Manual Installation
1. Copy the `web_dark_mode` folder to your Odoo addons directory
2. Restart your Odoo server
3. Go to Apps menu and search for "Dark Mode Toggle"
4. Install the module

### Method 2: Git Installation
```bash
cd /path/to/odoo/addons
git clone <repository-url> web_dark_mode
```

## 📖 Usage

### Enabling Dark Mode
1. After installation, you'll see a moon icon (🌙) in the top navigation bar
2. Click the moon icon to switch to dark mode
3. The icon will change to a sun (☀️) indicating dark mode is active
4. Click the sun icon to switch back to light mode

### User Experience
- **Instant Switching**: Theme changes are applied immediately
- **Smooth Animations**: All transitions are smooth and professional
- **No Page Reload**: Theme switching doesn't require page refresh
- **Consistent Experience**: Works across all Odoo modules and views

## 🎨 Theme Coverage

The dark theme comprehensively covers:

### Core Interface
- Navigation bar and menus
- Content areas and forms
- List views and kanban boards
- Calendar views and dashboards
- Modal dialogs and popups

### Form Elements
- Input fields and text areas
- Dropdown menus and selectors
- Buttons and action items
- Checkboxes and radio buttons
- Progress bars and indicators

### Data Views
- Table headers and rows
- Search panels and filters
- Breadcrumbs and navigation
- Status bars and controls
- Sidebars and panels

### Special Elements
- Alerts and notifications
- Cards and containers
- Tabs and navigation
- Badges and labels
- Scrollbars (Webkit browsers)

## 🔧 Technical Details

### Architecture
- **Frontend**: JavaScript with Odoo's widget system
- **Styling**: SCSS with CSS custom properties
- **Storage**: Browser localStorage API
- **Integration**: Odoo's system tray menu

### Files Structure
```
web_dark_mode/
├── __init__.py
├── __manifest__.py
├── README.md
├── views/
│   └── assets.xml
└── static/
    └── src/
        ├── scss/
        │   └── dark_theme.scss
        └── js/
            └── dark_mode_toggle.js
```

### Key Components

#### JavaScript (dark_mode_toggle.js)
- `DarkModeToggle`: Main widget for toggle functionality
- `DarkModeToggleMenuItem`: System tray menu integration
- Local storage management
- Theme application logic

#### SCSS (dark_theme.scss)
- Comprehensive dark theme variables
- Complete interface styling
- Smooth transitions
- Responsive design

#### QWeb Templates (assets.xml)
- Toggle button templates
- Asset inclusion
- System tray integration

## 🛠️ Customization

### Modifying Colors
Edit the variables in `dark_theme.scss`:
```scss
$dark-bg-primary: #1a1a1a;      // Main background
$dark-bg-secondary: #2d2d2d;    // Secondary background
$dark-text-primary: #ffffff;    // Primary text
$dark-accent: #007bff;          // Accent color
```

### Adding Custom Elements
To style custom elements, add CSS rules within the `body.dark-mode` selector:
```scss
body.dark-mode {
    .your-custom-element {
        background-color: $dark-bg-secondary;
        color: $dark-text-primary;
    }
}
```

## 🔍 Troubleshooting

### Theme Not Applying
1. Clear browser cache and cookies
2. Restart Odoo server
3. Check browser console for JavaScript errors
4. Verify module is properly installed

### Toggle Button Not Visible
1. Ensure module is installed and active
2. Check if user has proper permissions
3. Clear browser cache
4. Restart Odoo server

### Local Storage Issues
- Module gracefully handles localStorage unavailability
- Falls back to light mode if storage fails
- Check browser console for warnings

## 📝 Development

### Adding New Features
1. Extend the JavaScript widget
2. Add corresponding SCSS styles
3. Update QWeb templates if needed
4. Test across different browsers

### Testing
- Test on different browsers (Chrome, Firefox, Safari, Edge)
- Verify responsive design on mobile devices
- Check accessibility compliance
- Test with different Odoo modules

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This module is licensed under LGPL-3. See the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

### v1.0.0
- Initial release
- Complete dark theme implementation
- System tray toggle integration
- Local storage preference persistence
- Comprehensive interface coverage

---

**Enjoy your dark mode experience! 🌙** 