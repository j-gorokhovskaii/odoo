odoo.define('web_dark_mode.dark_mode_toggle', [], function (require) {
    'use strict';

    console.log('Dark Mode Toggle Module: Loading...');

    // Wait for DOM to be ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    // Simple approach using vanilla JavaScript
    ready(function () {
        console.log('Dark Mode Toggle: Document ready, initializing...');
        
        // Initialize dark mode on page load
        var isDarkMode = false;
        try {
            var stored = localStorage.getItem('odoo_dark_mode');
            isDarkMode = stored === 'true';
            console.log('Dark Mode Toggle: Stored preference =', isDarkMode);
        } catch (e) {
            console.warn('Could not read dark mode preference:', e);
        }

        if (isDarkMode) {
            document.body.classList.add('dark-mode');
            console.log('Dark Mode Toggle: Applied dark mode on load');
        }

        // Function to add toggle button
        function addToggleButton() {
            var navbar = document.querySelector('.o_main_navbar .o_menu_systray');
            console.log('Dark Mode Toggle: Looking for navbar, found:', navbar ? 1 : 0);
            
            if (navbar && !navbar.querySelector('.dark-mode-toggle')) {
                console.log('Dark Mode Toggle: Adding toggle button to navbar');
                var toggleHtml = `
                    <li class="o_mail_systray_item">
                        <button class="dark-mode-toggle" type="button" title="Toggle Dark Mode">
                            <i class="toggle-icon fa ${isDarkMode ? 'fa-sun-o' : 'fa-moon-o'}"></i>
                            <span class="sr-only">Toggle Dark Mode</span>
                        </button>
                    </li>
                `;
                navbar.insertAdjacentHTML('beforeend', toggleHtml);

                // Add click handler
                var toggleBtn = navbar.querySelector('.dark-mode-toggle');
                toggleBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    isDarkMode = !isDarkMode;
                    console.log('Dark Mode Toggle: Button clicked, isDarkMode =', isDarkMode);
                    
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
                    var icon = this.querySelector('.toggle-icon');
                    var btn = this;
                    
                    if (isDarkMode) {
                        icon.classList.remove('fa-moon-o');
                        icon.classList.add('fa-sun-o');
                        btn.setAttribute('title', 'Switch to Light Mode');
                    } else {
                        icon.classList.remove('fa-sun-o');
                        icon.classList.add('fa-moon-o');
                        btn.setAttribute('title', 'Switch to Dark Mode');
                    }
                });
                
                console.log('Dark Mode Toggle: Button added successfully');
            } else {
                console.log('Dark Mode Toggle: Navbar not found or toggle already exists');
            }
        }

        // Try to add button immediately
        addToggleButton();

        // Also try after a short delay to ensure DOM is ready
        setTimeout(addToggleButton, 1000);
        
        // Try again after a longer delay
        setTimeout(addToggleButton, 3000);

        // Watch for navigation changes and re-add button if needed
        if (window.MutationObserver) {
            var observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'childList') {
                        addToggleButton();
                    }
                });
            });

            // Start observing
            var navbar = document.querySelector('.o_main_navbar');
            if (navbar) {
                observer.observe(navbar, {
                    childList: true,
                    subtree: true
                });
                console.log('Dark Mode Toggle: MutationObserver started');
            }
        }

        // Alternative: Check periodically for navbar
        var checkInterval = setInterval(function() {
            var navbar = document.querySelector('.o_main_navbar .o_menu_systray');
            var toggle = document.querySelector('.dark-mode-toggle');
            if (navbar && !toggle) {
                addToggleButton();
            }
        }, 2000);

        // Stop checking after 30 seconds
        setTimeout(function() {
            clearInterval(checkInterval);
        }, 30000);
    });

    console.log('Dark Mode Toggle Module: Loaded successfully');

    return {};
}); 