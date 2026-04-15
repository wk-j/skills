# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository is a collection of Claude Code skills. Each skill lives in its own top-level directory and is defined by a single `SKILL.md` file.

## Skill format

A skill is a markdown file with YAML frontmatter plus instructions:

```markdown
---
name: <skill-name>
description: <one-line description — determines when Claude invokes this skill>
---

<instructions Claude follows when the skill is invoked>
```

The `description` is the trigger signal — it must clearly state when the skill should fire, because Claude uses it to decide whether to invoke the skill for a given user request. See `grill-me/SKILL.md` for a minimal reference.

## Adding a skill

- Create a new top-level directory named after the skill (kebab-case).
- Add a `SKILL.md` with the frontmatter above.
- No build step, package manager, or test runner — skills are plain markdown consumed directly by Claude Code.

## Importing skills from elsewhere

When asked to pull a skill from an external repo (e.g. `github.com/<user>/skills/tree/main/<skill>`), fetch the directory contents via `gh api repos/<user>/skills/contents/<skill>` and download each file into a matching top-level directory here. Preserve the directory name.

## After downloading any skill

Whenever a skill is downloaded or added to this repo, always update `README.md` to include an entry for it. Each entry must contain:

- The skill name (linked to its directory).
- A **concise** purpose — as short as possible while still conveying what the skill does. Distill the frontmatter `description` into the shortest accurate phrase; do not copy it verbatim.
- The **source** — a link to the original skill (e.g. the GitHub URL it was downloaded from). If the skill was authored in this repo, mark it as such.

Keep `README.md` as the canonical index of every skill, its purpose, and its origin.
