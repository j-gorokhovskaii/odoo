/** @odoo-module **/

// Dark mode toggle: injects a navbar systray button, toggles `body.dark-mode`,
// and persists the choice in localStorage.
//
// 19.0 port: rewritten from the legacy `odoo.define(name, [], function (require) {…})`
// AMD form (removed in 19) to a standard ES module. The logic is plain DOM/localStorage
// (no Odoo deps), so it runs on bundle load. A future cleanup could express this as a
// proper OWL systray registry component.

function ready(fn) {
    if (document.readyState !== "loading") {
        fn();
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

ready(function () {
    let isDarkMode = false;
    try {
        isDarkMode = localStorage.getItem("odoo_dark_mode") === "true";
    } catch (e) {
        // localStorage unavailable — default to light
    }

    if (isDarkMode) {
        document.body.classList.add("dark-mode");
    }

    function addToggleButton() {
        const navbar = document.querySelector(".o_main_navbar .o_menu_systray");
        if (!navbar || navbar.querySelector(".dark-mode-toggle")) {
            return;
        }
        const toggleHtml = `
            <li class="o_mail_systray_item">
                <button class="dark-mode-toggle" type="button" title="Toggle Dark Mode">
                    <i class="toggle-icon fa ${isDarkMode ? "fa-sun-o" : "fa-moon-o"}"></i>
                    <span class="sr-only">Toggle Dark Mode</span>
                </button>
            </li>`;
        navbar.insertAdjacentHTML("beforeend", toggleHtml);

        const toggleBtn = navbar.querySelector(".dark-mode-toggle");
        toggleBtn.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            isDarkMode = !isDarkMode;
            try {
                localStorage.setItem("odoo_dark_mode", isDarkMode.toString());
            } catch (err) {
                // ignore persistence failure
            }
            document.body.classList.toggle("dark-mode", isDarkMode);
            const icon = this.querySelector(".toggle-icon");
            if (isDarkMode) {
                icon.classList.remove("fa-moon-o");
                icon.classList.add("fa-sun-o");
                this.setAttribute("title", "Switch to Light Mode");
            } else {
                icon.classList.remove("fa-sun-o");
                icon.classList.add("fa-moon-o");
                this.setAttribute("title", "Switch to Dark Mode");
            }
        });
    }

    // The webclient navbar renders asynchronously; try now, after delays, and on DOM changes.
    addToggleButton();
    setTimeout(addToggleButton, 1000);
    setTimeout(addToggleButton, 3000);

    if (window.MutationObserver) {
        const navbar = document.querySelector(".o_main_navbar");
        if (navbar) {
            new MutationObserver(addToggleButton).observe(navbar, {
                childList: true,
                subtree: true,
            });
        }
    }

    const checkInterval = setInterval(function () {
        const navbar = document.querySelector(".o_main_navbar .o_menu_systray");
        if (navbar && !document.querySelector(".dark-mode-toggle")) {
            addToggleButton();
        }
    }, 2000);
    setTimeout(function () {
        clearInterval(checkInterval);
    }, 30000);
});
