/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { xml } from "@odoo/owl";

class DarkModeToggle extends Component {
    setup() {
        this.isDarkMode = false;
        this.loadDarkModePreference();
        this.applyDarkMode();
    }

    loadDarkModePreference() {
        try {
            const stored = localStorage.getItem('odoo_dark_mode');
            this.isDarkMode = stored === 'true';
        } catch (e) {
            console.warn('Could not read dark mode preference:', e);
        }
    }

    applyDarkMode() {
        if (this.isDarkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }

    toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
        
        // Update localStorage
        try {
            localStorage.setItem('odoo_dark_mode', this.isDarkMode.toString());
        } catch (e) {
            console.warn('Could not save dark mode preference to localStorage:', e);
        }
        
        // Apply theme
        this.applyDarkMode();
    }
}

DarkModeToggle.template = xml`
    <li class="o_menu_systray_item">
        <button 
            class="dark-mode-toggle" 
            type="button" 
            t-att-title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
            t-on-click="() => this.toggleDarkMode()">
            <i t-att-class="isDarkMode ? 'fa fa-sun-o' : 'fa fa-moon-o'"></i>
        </button>
    </li>
`;

// Register as a systray item with high sequence to appear near the end
registry.category("systray").add("web_dark_mode.toggle", {
    Component: DarkModeToggle,
}, { sequence: 50 }); 