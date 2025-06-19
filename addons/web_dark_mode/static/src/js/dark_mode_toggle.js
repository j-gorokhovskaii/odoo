odoo.define('web_dark_mode.dark_mode_toggle', function (require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    var session = require('web.session');

    var QWeb = core.qweb;
    var _t = core._t;

    /**
     * Dark Mode Toggle Widget
     * Handles the dark mode toggle functionality
     */
    var DarkModeToggle = Widget.extend({
        template: 'DarkModeToggle',
        events: {
            'click .dark-mode-toggle': '_onToggleClick',
        },

        /**
         * Initialize the dark mode toggle
         */
        init: function () {
            this._super.apply(this, arguments);
            this.isDarkMode = this._getStoredPreference();
            this._applyTheme();
        },

        /**
         * Start the widget
         */
        start: function () {
            this._super.apply(this, arguments);
            this._updateToggleButton();
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
        },

        /**
         * Start the widget
         */
        start: function () {
            this._super.apply(this, arguments);
            this._updateToggleButton();
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

    // Initialize dark mode on page load
    $(document).ready(function () {
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
    });

    return {
        DarkModeToggle: DarkModeToggle,
        DarkModeToggleMenuItem: DarkModeToggleMenuItem,
    };
}); 