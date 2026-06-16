# Custom modules — ported to Odoo 19.0

These are the 8 custom modules from this project, ported to run on **Odoo 19.0**
(the versions in `addons/` on the 18.0 branches target 18.0).

Modules: `opensource_knowledge`, `odoo_documentation`, `partner_dob`, `partner_height`,
`company_details`, `extendedcontact`, `web_dark_mode`, `theme_backend_blue`.

- All 8 install and run on a fresh Odoo 19.0 database.
- The generated docs mirror (`odoo_documentation/static/docs/`) is **not** committed —
  regenerate it with `odoo_documentation/scripts/import_docs.py`.
- Every 18.0 → 19.0 change and fix is catalogued in the local `ODOO_UPGRADE_PLAYBOOK.md`.

To run on 19.0, point an Odoo 19.0 `addons_path` at this folder (see the parallel
environment described in `RUNNING_ODOO.md` §12).
