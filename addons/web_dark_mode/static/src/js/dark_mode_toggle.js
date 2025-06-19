odoo.define('web_dark_mode.dark_mode_toggle', function (require) {
    'use strict';

    console.log('Dark Mode Toggle Module: Loading...');

    var core = require('web.core');
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    var session = require('web.session');

    var QWeb = core.qweb;
    var _t = core._t;

    /**
     * Dark Mode Toggle Menu Item
     * Extends SystrayMenu to add the toggle to the system tray
     */
    var DarkModeToggleMenuItem = SystrayMenu.extend({
        template: 'DarkModeToggleMenuItem',
        events: {
            'click .dark-mode-toggle': '_onToggleClick',
        },

        /**
         * Initialize the menu item
         */
        init: function () {
            this._super.apply(this, arguments);
            this.isDarkMode = this._getStoredPreference();
            this._applyTheme();
            console.log('Dark Mode Toggle Menu Item: Initialized');
        },

        /**
         * Start the widget
         */
        start: function () {
            this._super.apply(this, arguments);
            this._updateToggleButton();
            console.log('Dark Mode Toggle Menu Item: Started');
            return this._super.apply(this, arguments);
        },

        /**
         * Handle toggle button click
         */
        _onToggleClick: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            
            this.isDarkMode = !this.isDarkMode;
            this._storePreference();
            this._applyTheme();
            this._updateToggleButton();
            console.log('Dark Mode Toggle: Clicked, isDarkMode =', this.isDarkMode);
        },

        /**
         * Apply the current theme to the document
         */
        _applyTheme: function () {
            var body = document.body;
            
            if (this.isDarkMode) {
                body.classList.add('dark-mode');
            } else {
                body.classList.remove('dark-mode');
            }
            console.log('Dark Mode Toggle: Theme applied, isDarkMode =', this.isDarkMode);
        },

        /**
         * Update the toggle button appearance
         */
        _updateToggleButton: function () {
            var toggleBtn = this.$('.dark-mode-toggle');
            var icon = this.$('.toggle-icon');
            
            if (this.isDarkMode) {
                icon.removeClass('fa-moon-o').addClass('fa-sun-o');
                toggleBtn.attr('title', _t('Switch to Light Mode'));
            } else {
                icon.removeClass('fa-sun-o').addClass('fa-moon-o');
                toggleBtn.attr('title', _t('Switch to Dark Mode'));
            }
        },

        /**
         * Get stored preference from localStorage
         */
        _getStoredPreference: function () {
            try {
                var stored = localStorage.getItem('odoo_dark_mode');
                return stored === 'true';
            } catch (e) {
                console.warn('Could not read dark mode preference from localStorage:', e);
                return false;
            }
        },

        /**
         * Store preference in localStorage
         */
        _storePreference: function () {
            try {
                localStorage.setItem('odoo_dark_mode', this.isDarkMode.toString());
            } catch (e) {
                console.warn('Could not save dark mode preference to localStorage:', e);
            }
        },
    });

    // Register the dark mode toggle in the system tray
    SystrayMenu.Items.push(DarkModeToggleMenuItem);
    console.log('Dark Mode Toggle: Registered in SystrayMenu');

    // Alternative approach: Add toggle button directly to navbar
    $(document).ready(function () {
        console.log('Dark Mode Toggle: Document ready, adding direct toggle button');
        
        // Initialize dark mode on page load
        var isDarkMode = false;
        try {
            var stored = localStorage.getItem('odoo_dark_mode');
            isDarkMode = stored === 'true';
        } catch (e) {
            console.warn('Could not read dark mode preference:', e);
        }

        if (isDarkMode) {
            document.body.classList.add('dark-mode');
        }

        // Add toggle button directly to navbar if not already present
        function addToggleButton() {
            var navbar = $('.o_main_navbar .o_menu_systray');
            console.log('Dark Mode Toggle: Looking for navbar, found:', navbar.length);
            
            if (navbar.length && !navbar.find('.dark-mode-toggle').length) {
                console.log('Dark Mode Toggle: Adding toggle button to navbar');
                var toggleHtml = `
                    <li class="o_mail_systray_item">
                        <button class="dark-mode-toggle" type="button" title="Toggle Dark Mode">
                            <i class="toggle-icon fa ${isDarkMode ? 'fa-sun-o' : 'fa-moon-o'}"></i>
                            <span class="sr-only">Toggle Dark Mode</span>
                        </button>
                    </li>
                `;
                navbar.append(toggleHtml);

                // Add click handler
                navbar.find('.dark-mode-toggle').on('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    isDarkMode = !isDarkMode;
                    console.log('Dark Mode Toggle: Direct button clicked, isDarkMode =', isDarkMode);
                    
                    // Update localStorage
                    try {
                        localStorage.setItem('odoo_dark_mode', isDarkMode.toString());
                    } catch (e) {
                        console.warn('Could not save dark mode preference to localStorage:', e);
                    }
                    
                    // Apply theme
                    if (isDarkMode) {
                        document.body.classList.add('dark-mode');
                    } else {
                        document.body.classList.remove('dark-mode');
                    }
                    
                    // Update button
                    var icon = $(this).find('.toggle-icon');
                    var btn = $(this);
                    
                    if (isDarkMode) {
                        icon.removeClass('fa-moon-o').addClass('fa-sun-o');
                        btn.attr('title', 'Switch to Light Mode');
                    } else {
                        icon.removeClass('fa-sun-o').addClass('fa-moon-o');
                        btn.attr('title', 'Switch to Dark Mode');
                    }
                });
            } else {
                console.log('Dark Mode Toggle: Navbar not found or toggle already exists');
            }
        }

        // Try to add button immediately
        addToggleButton();

        // Also try after a short delay to ensure DOM is ready
        setTimeout(addToggleButton, 1000);

        // Watch for navigation changes and re-add button if needed
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    addToggleButton();
                }
            });
        });

        // Start observing
        if ($('.o_main_navbar').length) {
            observer.observe($('.o_main_navbar')[0], {
                childList: true,
                subtree: true
            });
            console.log('Dark Mode Toggle: MutationObserver started');
        }
    });

    console.log('Dark Mode Toggle Module: Loaded successfully');

    return {
        DarkModeToggleMenuItem: DarkModeToggleMenuItem,
    };
}); 