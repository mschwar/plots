# Two-Prompt Buildout Plan

This repo is already in the self-orienting, self-validating state. The remaining work should be done in small, independently mergeable features that fit a two-prompt loop:

Completed in this branch: item 1, the browser smoke harness for homepage + dashboard + one representative plot. The next unfinished item is order 2, offline-safe dashboard loading.

1. Build prompt: create a feature branch, implement one feature, add or update tests, update docs, commit, and push.
2. QA prompt: open the branch in the browser, take screenshots, verify behavior, update docs if needed, commit, push, and merge.

## Loop Contract

- One feature = one branch = one PR.
- Do not combine unrelated surface areas in a single branch.
- Every feature must have an explicit verification path:
  - browser verification for UI changes, or
  - a non-UI command for data, docs, validator, or build changes.
- Every feature branch must leave a handoff note in `CURRENT_STATE.md`.
- The handoff note should state: what changed, how it was verified, and what remains risky.
- Generated files should be regenerated from source instead of edited by hand.
- Keep each PR small enough that a second agent can understand it from the diff plus `AGENTS.md`, `CURRENT_STATE.md`, and this file.

## Missing Feature List

Use the first unfinished item unless a dependency makes it impossible.

| Order | Feature | Merge Surface | Verification | Docs / Handoff |
| --- | --- | --- | --- | --- |
| 1 | Browser smoke harness for homepage + dashboard + one representative plot | `tests/` plus a small helper script if needed | Browser screenshots at desktop and mobile widths, plus a non-UI pass/fail signal | Update `CURRENT_STATE.md` with the smoke command and screenshot result |
| 2 | Offline-safe dashboard loading | `dashboard/index.html`, `dashboard/dashboard.js`, and any local asset wiring | Browser load with network disabled, plus a non-UI check that no required runtime asset is remote-only | Update dashboard notes and `CURRENT_STATE.md` |
| 3 | Provenance coverage for speculative rows | `scripts/validate_all.py`, select `data/meta.json` files, and README data-contract text | `python scripts/validate_repo.py --check` | Update `CURRENT_STATE.md` with the provenance rule |
| 4 | Feature handoff template and PR checklist | `.github/pull_request_template.md`, `AGENTS.md`, or a small docs helper | Non-UI presence check and manual review of the template flow | Update `CURRENT_STATE.md` with the handoff rule |
| 5 | Mobile polish pass for the homepage and dashboard | `shared/site.css`, `dashboard/dashboard.css`, and the generators that own homepage markup | Browser screenshots on a narrow viewport | Update `CURRENT_STATE.md` with the viewport used |
| 6 | Archive cleanup for stale agent docs | `.agent-tasks/`, `docs/plans/`, and stale compatibility notes | Non-UI docs inspection and grep for stale references | Update `CURRENT_STATE.md` with any retained archival files |

## Branch Contract

- Branch name pattern: `feat/<slug>` for product work, `chore/<slug>` for tooling or docs.
- PR title should match the feature slug.
- PR body should include:
  - goal
  - touched files
  - verification command or browser check
  - any unresolved risk
- If a feature touches generated output, commit the source change and regenerate in the same branch.

## Handoff Rule

After each merged feature, update `CURRENT_STATE.md` so the next agent can start cold and still know:

1. what just changed,
2. what command proves it works, and
3. what the next feature is.

That file is the shortest path from one prompt loop to the next.
