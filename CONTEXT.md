# Skills

This repository contains reusable agent skills. Each skill teaches an agent when and how to perform one recurring task.

## Language

**Skill**:
A reusable instruction bundle that an agent loads for a specific recurring task.
_Avoid_: Prompt, template, script

**Trigger signal**:
The skill description that tells an agent when to load the skill. It names situations and user requests, not a full summary of the workflow.
_Avoid_: Summary, overview

**Repository wiki maintenance**:
Keeping a GitHub repository Wiki accurate, navigable, and consistent with repository changes or deliberate user-requested updates.
_Avoid_: Generic docs generation, README editing

**Important repository knowledge**:
Durable information about the repository that helps people understand, operate, or safely change it over time.
_Avoid_: File-by-file summaries, temporary implementation details

**Wiki working copy**:
The local clone of a GitHub Wiki repository, kept beside the main repository using the `<repo>.wiki` directory name.
_Avoid_: Temporary wiki clone, generated docs folder

**Open Knowledge Format page**:
A markdown knowledge page with YAML frontmatter for structured fields and a markdown body for human-readable context.
_Avoid_: Plain note, unstructured wiki page

**Resource field**:
The YAML frontmatter value that points to the primary source a knowledge page describes or verifies.
_Avoid_: Self-link to the wiki page

**Automatic wiki publishing**:
Updating, committing, and pushing verified GitHub Wiki changes without pausing for user approval during routine maintenance.
_Avoid_: Approval-gated wiki publishing

**Natural Thai wiki prose**:
Thai reader-facing wiki content written idiomatically for native Thai readers while preserving exact technical names where needed.
_Avoid_: Direct translation from English
