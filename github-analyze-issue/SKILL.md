---
name: github-analyze-issue
description: Analyze GitHub issues and produce a structured markdown analysis document before any code changes — routes bug/improvement issues and question issues into separate document folders
---

## GitHub Issue Analyzer

Produce a structured analysis doc for a GitHub issue. Always write the doc **before** any code change.

### Rules

1. Write the analysis doc to disk **first**, automatically, before any implementation.
2. Confirm with the user before implementing a fix, posting a GitHub comment, or creating any external resource (ticket, PR, etc.). Never run `gh issue comment` without explicit approval.

### Classification

| Type | Signals | Output folder |
|------|---------|---------------|
| Bug / Improvement | labels `type: Bug`, `type: Enhancement`; words like fix/bug/error/add/implement | `docs/cr/{repo}/{issue-id}/` |
| Question | labels `type: Question`, `type: Help Wanted`; words like how/why/what/explain | `docs/question/{repo}/{issue-id}/` |

Ask the user if ambiguous. Follow project conventions in `CLAUDE.md` if they differ.

### Workflow

1. **Fetch**: `gh issue view <n> --repo <owner>/<repo> --comments`. Extract image URLs (`user-attachments/assets/…`), download with `curl -sL -H "Authorization: token $(gh auth token)" <url> -o /tmp/...`, and `Read` them — screenshots often contain critical context.
2. **Classify** using the table above.
3. **Investigate**: read the relevant code, query DB/external systems as needed, identify root cause, and capture file paths and snippets.
4. **Write the doc** to `docs/{cr|question}/{repo}/{issue-id}/{kebab-name}.md` (3–5 word descriptive name). Create folders as needed.
5. **Suggest next steps** (fix, GitHub comment, tracking task) — do not act on them without approval.

### Audience

Docs may be read by non-developers. Include a **Glossary** defining every technical term, column, enum, or internal identifier in plain language — explain business meaning, not just technical definition. Pair identifiers with a short human description on first use. If the project's primary language isn't English, match it (use existing docs in the target folder as a style guide).

### Templates

Adapt headings to the project's language/conventions; this is the baseline.

#### Bug / Improvement

```markdown
# Issue #{n}: {title}

> GitHub: https://github.com/{owner}/{repo}/issues/{n}

## Summary
{1–2 sentences}

## Glossary
| Term | Meaning |
|------|---------|
| `{term}` | {plain-language business meaning} |

## Analysis

### Affected Components
| Component | File |
|-----------|------|
| {layer} | `{path}` |

### Root Cause
{why it happens / what must change}

### Current Implementation
{snippet + path}

## Proposed Fix
{what to change}

### Files to Change
- `{path}` — {change}

## Impact
- Surfaces affected: {list}
- Scope: {users/modules}
- Risk: {Low/Medium/High}

---
🤖 Analyzed by AI (Claude <MODEL_NAME>)
```

#### Question

```markdown
# Issue #{n}: {title}

> GitHub: https://github.com/{owner}/{repo}/issues/{n}

## Question
{restated}

## Glossary
| Term | Meaning |
|------|---------|

## Answer
{direct answer}

### Details
{evidence: code refs, queries}

### Related Code
| File | Relevance |
|------|-----------|

### Database Evidence (if applicable)
```sql
{query}
```
{results / interpretation}

## Conclusion
{summary and recommendations}

---
🤖 Analyzed by AI (Claude <MODEL_NAME>)
```

### Command reference

```bash
gh issue view <n> --repo <owner>/<repo>
gh issue view <n> --repo <owner>/<repo> --comments
gh issue list --repo <owner>/<repo> --limit 10
gh issue view <n> --repo <owner>/<repo> --json labels
```
