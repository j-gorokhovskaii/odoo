/** @odoo-module **/

// Re-apply our brand-aligned link colors for Discuss/chatter messages, instead of
// editing addons/mail core. The Message component reads these static constants via
// `this.constructor.SHADOW_LINK_COLOR`, so reassigning the statics is enough.
import { Message } from "@mail/core/common/message";

Message.SHADOW_LINK_COLOR = "#1f6feb"; // darkened #29abe2
Message.SHADOW_LINK_HOVER_COLOR = "#0056b3";

// Recolor the PWA/mobile browser chrome "theme-color" meta tag (done in JS to avoid
// adding an ir.ui.view data record to this theme_-named module).
const themeColorMeta = document.querySelector('meta[name="theme-color"]');
if (themeColorMeta) {
    themeColorMeta.setAttribute("content", "#29abe2");
}
