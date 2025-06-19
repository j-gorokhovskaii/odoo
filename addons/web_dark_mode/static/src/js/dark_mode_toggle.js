odoo.define('web_dark_mode.dark_mode_toggle', function (require) {
    'use strict';

    console.log('Dark Mode Toggle Module: Loading...');

    // Simple approach without complex dependencies
    $(document).ready(function () {
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
            if ($('.o_main_navbar').length) {
                observer.observe($('.o_main_navbar')[0], {
                    childList: true,
                    subtree: true
                });
                console.log('Dark Mode Toggle: MutationObserver started');
            }
        }

        // Alternative: Check periodically for navbar
        var checkInterval = setInterval(function() {
            if ($('.o_main_navbar .o_menu_systray').length && !$('.dark-mode-toggle').length) {
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