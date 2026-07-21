---
name: maintain-github-wiki
description: Maintain GitHub repository Wiki pages safely in natural Thai as Open Knowledge Format-compatible markdown by categorizing important repository knowledge, auditing existing wiki content, drafting page changes, and publishing verified updates automatically. Use when asked to create, update, sync, reorganize, or audit a GitHub Wiki for a repository; do not use for README/docs edits in the main repo.
---

# Maintain GitHub Wiki

Maintain GitHub repository Wiki pages so they stay current with repository changes and deliberate user-requested updates.

## Boundary

Use this skill when the user asks to:
- Create, update, audit, reorganize, rename, or delete GitHub Wiki pages.
- Keep wiki content up to date with repository changes, releases, behavior, docs, or user-requested additions.
- Maintain `Home`, `_Sidebar`, `_Footer`, or cross-page wiki navigation.

Do not use this skill for:
- README files, `/docs` content, changelogs, issue comments, PR descriptions, or API docs inside the main repo.
- Publishing to non-GitHub documentation systems.

## Language

Publish wiki page content in natural, native Thai. Do not directly translate English source text sentence-by-sentence. Rewrite for Thai readers while preserving technical accuracy.

Keep technical terms in English — do not translate them into Thai. This covers code identifiers, file paths, API names, commands, package names, and protocol terms, and also established software vocabulary such as deploy, endpoint, cache, middleware, branch, commit, pull request, queue, worker, token, and framework/library names. Thai readers of a technical wiki understand these terms in English; a Thai coinage or transliteration-plus-gloss is harder to recognize and search for. Write the surrounding sentence in Thai and drop the English term in as-is (e.g. "ระบบจะ retry งานที่ fail ผ่าน queue เดิม"), rather than inventing Thai equivalents like "คิวงาน" for queue or "จุดปลายทาง" for endpoint. Translate only genuinely non-technical words.

On a technical term's **first appearance in a page**, gloss it: follow the term with a short plain-Thai explanation in parentheses, e.g. "queue (แถวรอประมวลผลงาน)" or "middleware (โค้ดที่ดักประมวลผล request ก่อนถึง handler หลัก)". After the first use, write the bare term. Gloss per page, not per wiki — readers land on pages directly, so do not assume they read another page first. Skip the gloss for terms so universal they need no explanation to any developer (API, URL, commit) and for code identifiers whose meaning is the surrounding sentence's whole point. If the same specialized terms recur across many pages, create a `Glossary` page collecting them and link the first occurrence to it instead of repeating long glosses.

For OKF metadata fields, write reader-facing fields (`title`, `description`) in natural Thai. Keep machine-facing fields stable and parseable: `type` uses the agreed vocabulary, `resource` keeps the original path or URL, `tags` use short technical slugs, and `timestamp` stays ISO-formatted.

Use stable English or technical slugs for filenames and paths, even when the page title is Thai. Put the natural Thai name in `title` and the H1 heading. Do not rename a file just to improve Thai wording; rename only when the concept identity changes.

## LLM Wiki principle

Follow the LLM Wiki pattern: the wiki is a persistent, compounding knowledge layer between raw repository sources and future questions. Do not mirror every file or commit. Extract only durable, important knowledge that helps someone understand, operate, or change the repository.

Start with these categories for important repository knowledge before writing pages:
- **Overview** — what the repository is for and how the main pieces fit together.
- **Components** — durable modules, services, packages, or subsystems.
- **Workflows** — recurring user, developer, release, deployment, or operational flows.
- **Concepts** — domain terms, invariants, data models, protocols, or integration contracts.
- **Decisions** — meaningful architectural or product choices and their trade-offs.
- **Sources** — important docs, releases, issues, PRs, or code locations that support wiki claims.

Maintain an index or sidebar so future updates can find the right page before creating a new one. Add narrower subcategories only after the repository shows a repeated pattern that does not fit the six starting categories. If a change is too local, temporary, or obvious from one file, leave it out of the wiki.

Use a `Wiki Update Log` page only when maintenance is ongoing, multiple pages change together, or a major repository change drives the update. Each entry should record the date, action, affected pages, and source evidence. For small one-page edits, rely on the wiki repository's git history instead of adding log noise.

## Open Knowledge Format compatibility

Write wiki concept pages as markdown with an OKF metadata block first. GitHub Wiki does not hide YAML frontmatter — a bare `---` block renders as a horizontal rule plus stray metadata text at the top of the page — so wrap the YAML in an HTML comment instead. GitHub hides the comment while the YAML stays machine-parseable:

```markdown
<!-- okf
type: components
title: ระบบ queue งาน
description: จัดการงานเบื้องหลังผ่าน queue และ worker
resource: src/queue/
tags: [queue, worker]
timestamp: 2026-07-03T00:00:00Z
-->
```

Each page must include `type`; include `title`, `description`, `resource`, `tags`, and `timestamp` when known. Use the six categories above as `type` values unless the repository has a better established vocabulary. When auditing existing pages, convert any bare `---` frontmatter to this comment-wrapped form.

Set `resource` to the primary source the page describes or verifies, such as a repo-relative code path, docs path, release, issue, or PR. Do not set `resource` to the wiki page's own URL unless the page is documenting the wiki itself. Put additional evidence under a `## Sources` section in the markdown body.

Use a light body template for new concept pages: `# <Title>`, `## Summary`, `## Key relationships`, and `## Sources`. Add type-specific sections after these common sections; omit a common section only when it truly does not apply. Do not force one large template across every `type`.

Link cross-page relationships with **extensionless** page names: `[Orders](Orders)`, not `[Orders](Orders.md)`. GitHub Wiki serves rendered pages at extensionless URLs (`/wiki/Orders`); a `.md` suffix makes GitHub treat the link as a raw-file request and redirect to `raw.githubusercontent.com/.../Orders.md`, showing plain text instead of the rendered page. This overrides OKF's usual `.md`-link convention: on a published GitHub Wiki, links that work in the browser take priority over cross-tool path portability. Keep the file path (still `Orders.md` on disk) as the concept identity; rename pages only when the concept identity changes. `[[Page Title]]` links also work on GitHub, but prefer explicit `[text](Page-Name)` links so link text and target stay clear.

Link to source files in the **main repo** with full URLs (`https://github.com/OWNER/REPO/blob/main/src/queue/worker.ts`), never relative `.md` paths — the wiki is a separate git repository, so relative paths cannot reach main-repo files.

Link issues, PRs, and commits with full-URL markdown links: `[#325](https://github.com/OWNER/REPO/issues/325)`, not a bare `#325`. GitHub autolinks `#325` shorthand in issue/PR/commit text in the main repo, but **not** on wiki pages — there a bare `#325` renders as plain text. This applies inside tables too (e.g. an `Issue` column): write `[#325](…/issues/325)` in each cell so the number is clickable.

Point each issue/PR URL at the repository that actually hosts it, which is often **not** the wiki's own repo — issues are frequently tracked in a separate project or tracker repo. Confirm the owning repo before writing the link (ask, or infer from context) rather than defaulting to the wiki's repo; a link to the wrong repo lands on an unrelated issue or a 404. Cross-repo shorthand like `owner/repo#325` also does not autolink on wiki pages, so always use the explicit full URL to the correct repo.

Use `index.md` pages for category navigation when the wiki has enough pages to need hierarchy. Update `index.md` whenever creating a page, deleting or renaming a page, or changing a page's `title`, `description`, `type`, or `tags`; skip index edits for body-only changes that do not affect navigation. Use `log.md` for chronological history when the update-log rule applies.
Keep `_Sidebar.md` minimal and GitHub-specific: link to `Home.md`, major categories, or `index.md`, but do not list every concept page there. Create or update `_Sidebar.md` only when navigation is missing or the top-level category structure changes; `index.md` remains the portable navigation source of truth.

## Workflow

1. **Identify the target repository.** Prefer an explicit `OWNER/REPO`. If missing, infer from the current git remote; ask only if multiple remotes or repos are plausible.
2. **Inspect the existing wiki first.** GitHub Wikis are separate git repositories at `https://github.com/OWNER/REPO.wiki.git`. Keep the local wiki working copy as a sibling directory of the main repo: if the repo directory is `skills`, the wiki directory should be `skills.wiki` in the same parent directory. Clone or fetch that wiki repo before drafting changes. If the wiki does not exist or is disabled, report that before creating pages.
3. **Inventory pages and navigation.** Read existing `*.md` pages, especially `Home.md`, `_Sidebar.md`, and `_Footer.md`. Preserve page names, links, and manually curated sections unless the user explicitly asks to change them.
4. **Ground wiki facts in the source of truth.** Read the main repo as evidence, but do not edit or commit it during wiki maintenance unless the original request explicitly asks for main-repo changes. When syncing from the main repo, verify claims against code, existing docs, issues, releases, or the specific user request. The wiki should not invent behavior or copy stale docs without checking.
5. **Plan the edit.** Before changing files, produce a compact internal plan: page, action (`create`, `edit`, `rename`, `delete`), reason, and source evidence. Do not interrupt the user for routine updates.
6. **Edit locally.** Make the smallest page changes that satisfy the request. Keep pages Open Knowledge Format-compatible: comment-wrapped OKF metadata block first, extensionless cross-page links (`[Orders](Orders)`), full URLs for main-repo source files, stable filenames for concept identity, and natural Thai prose for reader-facing content. Maintain `_Sidebar.md` only as GitHub Wiki navigation, not as the source of truth.
7. **Verify before publishing.** Inspect the diff, run markdown/metadata checks when available, confirm no page starts with a bare `---` frontmatter block, confirm no cross-page wiki link carries a `.md` suffix (those break to raw file views on GitHub), confirm issue/PR/commit references are full-URL markdown links rather than bare `#NNN` (which do not autolink on wiki pages), and scan for secrets or private data. If a requested update would require deleting pages, renaming pages, publishing secrets, or overwriting broad human-authored content without explicit instruction in the original request, stop and report the blocker instead of guessing.
8. **Publish automatically after verification.** Commit and push only the wiki repository with a clear message, then verify the public wiki URL or GitHub page view if accessible. Report what changed after publishing.

## Safety rules

- Never force-push a wiki repository.
- Never overwrite a whole page when a section edit is enough.
- Never remove human-authored content unless the original user request explicitly asked for removal and the diff shows exactly what will disappear.
- Never publish secrets, internal URLs, credentials, private customer data, or unreleased plans. If detected, remove them or stop with a blocker.
- If source docs and code disagree, record the conflict in the page or `log.md`, update to match verified source evidence, and include the conflict in the final report. Treat code/runtime behavior as stronger evidence than prose docs unless the user says otherwise.
- Keep attribution and generated-by footers out of wiki pages unless the project already uses them or the user asks for them.

## Command reference

Use commands appropriate to the local environment; these are common options:

```bash
# Check whether the repository has wiki support enabled
gh api repos/OWNER/REPO --jq '.has_wiki'

# Clone the wiki repository beside the main repo directory
# Example: ../skills and ../skills.wiki share the same parent directory
git clone https://github.com/OWNER/REPO.wiki.git ../REPO.wiki

# Inspect pending wiki changes before automatic publish
git -C ../REPO.wiki diff --stat
git -C ../REPO.wiki diff --check
git -C ../REPO.wiki diff

# Publish after verification
git -C ../REPO.wiki add .
git -C ../REPO.wiki commit -m "Update wiki: <summary>"
git -C ../REPO.wiki push
```
