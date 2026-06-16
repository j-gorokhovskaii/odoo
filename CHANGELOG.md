# Changelog

All notable changes to the **custom modules** in this repo are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/); module versions follow
SemVer in each `__manifest__.py`. Older detail lives in `git log`.

## [Unreleased]

### Added
- `opensource_knowledge` — knowledge base (articles, categories, tags, templates, sharing)
- `odoo_documentation` — in-app documentation viewer
- Contact extensions: `partner_dob`, `partner_height`, `company_details`, `extendedcontact`
- `theme_backend_blue` (#29abe2 branding) and `web_dark_mode`
- Odoo 19.0 ports of all custom modules (branch `19.0-custom-modules`, `custom-addons-19.0/`)

### Changed
- Decoupled the `#29abe2` branding from Odoo core into `theme_backend_blue`
  (via `web._assets_primary_variables`), so core stays pristine across upgrades.
