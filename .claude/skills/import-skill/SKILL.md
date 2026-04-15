---
name: import-skill
description: Import a skill from an external source (GitHub repo, URL, or local path) into this repo, rewriting project-specific details (file paths, company/team names, internal tool references, hard-coded URLs, domain examples) as generic patterns that work across any project. Use whenever the user asks to import, pull, copy, fetch, or add a skill from another repo or source.
---

# Import skill

Imports an external skill into this repo and rewrites project-specific content as generic patterns so the skill is reusable across any project.

## Steps

1. **Fetch the source.**
   - GitHub URL (`github.com/<user>/<repo>/tree/<branch>/<path>`): use `gh api repos/<user>/<repo>/contents/<path>?ref=<branch>` to list the directory, then download each file. Decode `content` if base64-encoded, or follow `download_url`.
   - Raw URL or web page: use WebFetch.
   - Local path: read directly.

2. **Identify project-specific content.** Read every file and flag anything tied to the original author's environment:
   - Hard-coded file paths (`/Users/alice/...`, `~/work/acme/...`, `C:\Users\...`)
   - Person, team, or company names (`Acme Corp`, `the platform team`, `@bob`)
   - Internal tools, services, or URLs (`acme-cli`, `https://acme.internal/...`, VPN-only links)
   - Specific repo, branch, project, or product names
   - Stack- or framework-specific examples that could be expressed generically
   - Chat/ticket IDs or channels (Slack `#eng-foo`, Jira `ABC-123`, Linear project codes)
   - Domain jargon, customer names, or business logic that wouldn't translate
   - Hard-coded credentials, tokens, or account IDs (always strip)

   Keep details that are inherent to the skill's purpose — a Python-linting skill can still mention Python.

3. **Rewrite generically.** Replace each project-specific item with one of:
   - A placeholder (`<your-repo>`, `<team>`, `<internal-tool>`)
   - A neutral example (`my-project` instead of `acme-frontend`)
   - A concept ("your team's chat tool" instead of "Slack #eng")
   - Removal, if the detail isn't load-bearing

   Preserve the skill's intent, behavioral guidance, and structure — only strip what's tied to the original context, not what makes the skill useful.

4. **Save into a new top-level directory.** Use the original skill's directory name (kebab-case). If the name itself is project-specific (e.g. `acme-deploy`), rename it and tell the user.

5. **Update `README.md`.** Add a row with: skill name (linked to its `SKILL.md`), a concise purpose distilled from the description, and the source.
   - **GitHub or public URL source:** link to the original (e.g. `[user/repo](https://github.com/...)`).
   - **Local filesystem path source:** do **not** include the original path — use `Authored in this repo` instead. Local paths can leak private project, client, or directory names. This also applies to commit messages, PR descriptions, and user-facing summaries for the import.

   Preserve alphabetical or existing ordering.

6. **Report what was generalized.** Summarize each substitution (original → replacement) so the user can review and revert anything that went too far.

## When unsure

If a substitution would change the skill's meaning or feels lossy, ask the user before applying it. A faithful import with a few project-specific traces is better than an over-eager rewrite that breaks the skill.
