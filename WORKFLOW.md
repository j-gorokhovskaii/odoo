# Development Workflow

How work flows through this repo: branches, issues, PRs, commits, CI, and releases.
Designed for a **solo developer scaling to a small team**, on a **public fork of
`odoo/odoo`** where the real work is **custom Odoo modules**. Windows (Git Bash + PowerShell).

> Companion docs (local only, gitignored): `RUNNING_ODOO.md`, `ODOO_UPGRADE_PLAYBOOK.md`.

---

## TL;DR — the daily loop

```bash
# 1. Start fresh from the trunk
git checkout main && git pull origin main

# 2. One branch per issue
git checkout -b feat/42-knowledge-pdf-export        # or fix/57-age-rounding

# 3. Small, conventional commits
git add -p
git commit -m "feat(opensource_knowledge): export article to PDF"

# 4. Stay current with trunk (rebase, not merge)
git fetch origin && git rebase origin/main

# 5. Push and open a PR (Draft while WIP)
git push -u origin feat/42-knowledge-pdf-export
#    PR body includes:  Closes #42

# 6. CI green + checklist done -> "Squash and merge" on GitHub

# 7. Clean up
git checkout main && git pull origin main
git branch -d feat/42-knowledge-pdf-export
git push origin --delete feat/42-knowledge-pdf-export
```

---

## 1. Branching strategy (Workflow Architect)

**Model: GitHub Flow** (not full trunk-based). One protected long-lived branch + short
feature branches. It's the simplest model that stays correct when a second dev joins;
trunk-based (commit straight to main behind flags) adds ceremony a solo dev doesn't need yet.

| Branch | Purpose | Base | Merges into |
|--------|---------|------|-------------|
| `main` | **Trunk** — your integrated custom work; always releasable | — | — |
| `feat/<issue>-<slug>` | New feature | `main` | `main` |
| `fix/<issue>-<slug>` | Bug fix | `main` | `main` |
| `hotfix/<slug>` | Urgent fix that can't wait | `main` | `main` |
| `chore/<slug>` | Tooling / deps / config | `main` | `main` |
| `docs/<slug>` | Docs only | `main` | `main` |
| `refactor/<slug>` | Restructure, no behaviour change | `main` | `main` |
| `18.0`, `19.0` | **Upstream mirrors** of `odoo/odoo` — keep clean, sync only | upstream | never into `main` |

Rules: lowercase, hyphenated slug, lead with the issue number (`feat/42-...`). Keep
branches short-lived (hours/days). Delete after merge.

---

## 2. Bug & work tracking (Issue Triager)

> ⚠️ Issues are enabled on the repo. Bug/feature **templates live in `.github/ISSUE_TEMPLATE/`**.

**Lifecycle:** `status:triage` → `status:todo` → `status:in-progress` → `status:review` → closed.

**Labels** (starter set, created on the repo):
- Type: `type:bug`, `type:feature`, `type:chore`, `type:docs`, `type:refactor`
- Priority: `priority:high`, `priority:medium`, `priority:low`
- Status: `status:triage`, `status:todo`, `status:in-progress`, `status:blocked`, `status:review`
- Misc: `good-first-issue`, `wontfix`, `duplicate`

**Milestones:** one per release (e.g. `2026.07`). Assign issues you intend to ship.

**Projects board** (set up once, in the UI): a Project with columns
**Triage → Todo → In Progress → In Review → Done**; enable the *Auto-add* and
*Item closed → Done* built-in workflows.

**Linking (auto-close):** put a closing keyword in the **PR body** (or a commit on the PR):
`Closes #42`, `Fixes #57`, `Resolves #12`. When the PR merges to the default branch, the
issue closes automatically. Use plain `#42` (no keyword) to reference without closing.

---

## 3. PR process (QA Lead + DevOps)

- **Size:** aim < ~400 changed lines. Bigger → split into stacked PRs.
- **Draft vs Ready:** open as **Draft** while WIP; flip to **Ready for review** when CI is green and the checklist passes.
- **Required check:** the **CI (custom modules)** workflow must pass (see §5).
- **Merge method:** **Squash and merge** — one tidy Conventional Commit per PR on `main`.
  The squash *commit title* should be a Conventional Commit (e.g. `fix(extendedcontact): correct age rounding (#57)`).
- **Self-review:** before flipping to Ready, read your own diff top to bottom; run the app on the relevant Odoo version.
- **Definition of done:**
  - *Feature:* works on the stated version, CI green, CHANGELOG updated, docs touched if user-facing.
  - *Bugfix:* root cause fixed (not symptom), the failing case now passes, a note on how it's prevented from regressing.

The PR checklist is enforced by `.github/PULL_REQUEST_TEMPLATE.md`.

---

## 4. Git command reference (DevOps)

```bash
# START
git checkout main && git pull origin main
git checkout -b fix/57-age-rounding

# COMMIT (stage hunks, conventional message)
git add -p
git commit -m "fix(extendedcontact): correct age rounding at month boundaries"

# REBASE onto latest trunk (keep history linear)
git fetch origin
git rebase origin/main
#   conflict? edit files, then:
git add <files> && git rebase --continue
#   abort if needed:  git rebase --abort

# PUSH (first time)
git push -u origin fix/57-age-rounding
#   after a rebase you'll need:
git push --force-with-lease

# MERGE: done on GitHub via "Squash and merge"

# CLEANUP
git checkout main && git pull origin main
git branch -d fix/57-age-rounding
git push origin --delete fix/57-age-rounding

# RELEASE TAG (after merging release-worthy work)
git tag -a v2026.07 -m "Release 2026.07: knowledge PDF export, age fix"
git push origin v2026.07
```

**Branch hygiene (clear the sprawl):**
```bash
git fetch --prune                      # drop refs deleted on the remote
git branch --merged main               # list local branches safely deletable
# delete a stale remote branch you no longer need:
git push origin --delete darkmode
```

---

## 5. CI (DevOps)

`.github/workflows/ci.yml` runs on PRs into `main` and pushes to `main`, **only when a
custom module changes** (path-filtered). It is intentionally **scoped to your modules**
(the full Odoo suite is impractical) and needs **no database**:

1. **flake8** error-level only (`E9,F63,F7,F82`) — catches syntax / undefined names.
2. **byte-compile** all Python.
3. **XML well-formedness** for every view/data file.
4. **Manifest sanity** — each `__manifest__.py` is a valid dict with a `name`.

Make it a **required status check** in branch protection (see §7) so red CI blocks merge.

---

## 6. Commit & changelog conventions (Documentation Keeper)

**Conventional Commits:** `type(scope): subject`
- types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`, `build`, `ci`
- scope = module, e.g. `feat(company_details): add credit-rating field`
- breaking change: add `!` → `feat(api)!: ...` and explain in the body.

**Versioning:** SemVer **per module** in `__manifest__.py` (`19.0.<major>.<minor>.<patch>`).
Bump on every user-facing change.

**Changelog:** add a line under `## [Unreleased]` in `CHANGELOG.md` in the same PR. At
release, rename `[Unreleased]` to the version/date and start a fresh `[Unreleased]`.

**Onboarding:** a new collaborator reads this file + `CHANGELOG.md`; operational setup is
in `RUNNING_ODOO.md` (local).

---

## 7. Best-practices pack — setup status (Release Manager checklist)

**Done (automated):**
- ✅ Default branch = `main`
- ✅ `main` protected: require PR, required check **`lint`**, 0 approvals (solo), force-push & deletion blocked, admin bypass on
- ✅ Issues enabled + label set created
- ✅ Templates + scoped CI + this doc on `main`; first CI run green
- ✅ Milestone **`2026.07`** created
- ✅ Backlog seeded as issues (#2 board, #3 demo-XML, #4 a11y)

**Optional / your call:**
- **Projects board** (kanban) — *not required.* Issues + labels + milestones already give
  you tracking (use the **Issues** tab's filters/saved views). A board is cosmetic; setting
  it up needs the `project` token scope or a few UI clicks. Tracked in **#2** with steps.

> Tracking = **Issues + labels (type/priority/status) + milestones**. Filter examples:
> `is:open label:type:bug`, `is:open milestone:2026.07`, `is:open label:status:in-progress`.

> Note: because `main` is protected, all changes (including to this file) go through a PR —
> exactly the flow in §1–§4.

---

## 8. Upstream sync (keeping the fork current)

`18.0` / `19.0` mirror `odoo/odoo`. Keep them pristine; never put custom work there.

```bash
git remote add upstream https://github.com/odoo/odoo.git    # once
git fetch upstream 18.0
git checkout 18.0
git merge --ff-only upstream/18.0     # fast-forward only; stays a clean mirror
git push origin 18.0
#   (repeat for 19.0)
```
Do **not** merge `upstream` into `main`. When upstream changes affect your modules,
update them on a `chore/...` branch and PR into `main`.

---

## 9. Collaboration log

Each specialist's recommendation, then the consolidation.

- **Workflow Architect:** GitHub Flow with `main` as the protected trunk; version branches
  kept as upstream mirrors. Trunk-based is overkill for one dev; revisit only if merge
  frequency and team size grow. Short-lived `type/<issue>-<slug>` branches, squash merges.
- **Issue Triager:** Issues had to be enabled first. Three-axis labels (type/priority/status),
  one milestone per release, a 5-column Project, and `Closes #N` in PR bodies for auto-close.
- **DevOps:** Lightweight, DB-less, path-filtered CI scoped to the 8 custom modules; squash
  merges; date-based release tags `vYYYY.MM`; "deploy" = upgrade the module on the local
  18.0/19.0 instance and smoke-test (see `RUNNING_ODOO.md`).
- **QA Lead:** Small PRs, Draft-until-green, a checklist template, and a bugfix rule:
  every fix names its root cause and how regression is prevented. CI is a required check.
- **Documentation Keeper:** Conventional Commits + per-module SemVer + Keep-a-Changelog,
  updated in the same PR; this `WORKFLOW.md` is the onboarding entry point.
- **Release Manager:** Consolidated the above into §§1–8 and the TL;DR loop. Weekly status
  template below.

### Weekly status (Release Manager) — copy/paste
```
## Week of <date>
Shipped (merged to main): <PRs / #issues>
In progress: <open branches -> issues>
Blocked: <issue + reason>
Released: <tag, if any>
Next: <top 1-3 issues>
```

Track "open branches vs issues" anytime:
```bash
git branch -r --no-merged origin/main     # branches with unmerged work
```
