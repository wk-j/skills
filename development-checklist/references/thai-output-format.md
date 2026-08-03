# Thai Output Format

Use this as guidance for information coverage, not as a sentence-by-sentence translation template. Compose the result directly in Thai, remove irrelevant sections, and never leave placeholders. Choose headings, labels, sentence order, and transitions that a native Thai project owner would naturally use.

Read the project's existing Thai-facing documents before writing. Reuse their established terms and level of formality unless they are unclear or inconsistent.

## Title

Choose a concise title that a Thai project owner would naturally use to name both the document purpose and the desired outcome. Do not translate an English title literally.

## Executive summary

Cover the following ideas, combining or reordering them when that reads more naturally in Thai:

- Goal: the user or organizational outcome in one or two sentences.
- Affected people: the user groups, teams, or systems involved.
- In scope: what this work includes.
- Out of scope: related work intentionally excluded.
- Key risk: the practical harm that could occur.

## Glossary

Include this section only when technical terms, abbreviations, or proper system names are unavoidable. Use a two-column table:

1. Original term or system name.
2. Its meaning for people or work, explained in plain Thai.

Never define one technical term with another. Explain the concrete effect, such as describing a required status check as an automated result that must pass before work can be merged.

## Project snapshot

Summarize only the verified facts needed to understand the checklist. Use a two-column table when a table improves clarity:

1. Verified current state.
2. Why it matters to the remaining work.

Keep source paths, commands, URLs, and issue-tracker references in the analysis, not in the user-facing checklist. The reader must not need to open another resource to understand the current state or decide what to do next.

## Requirements and checklists

Organize the checkpoint by requirement, not by a flat list of development activities. Use product behavior, data, integrations, correctness, testing, performance, maintainability, and technical documentation to discover the requirements and the work needed to fulfill them.

For each requirement:

1. Use a concise Thai heading that names the result people expect from the system.
2. Explain the requirement in one to three plain-Thai sentences, including its scope, observable behavior, and an important exclusion when necessary.
3. Place the complete task checklist for that requirement directly below the explanation.

Do not publish a checkbox whose requirement is unclear. Do not state only a feature name or technical component; explain what result it must produce for people, data, or another system.

A requirement is complete only when every material implementation, verification, and documentation task below it is `[x]`. If any material task is `[ ]`, leave the requirement visibly incomplete through its checklist without adding a separate status badge.

For an overall project development checklist, exclude deployment, infrastructure provisioning, production access, release packaging, Cutover, backup operations, training, and operational handoff unless the user explicitly includes them. Do not turn a development checklist into a production-readiness checklist.

For an overall checkpoint, include every material development task whether completed or open. Reconstruct the scope from product behavior, code, tests, migrations, and technical documentation rather than listing only current tickets or remaining work.

For each checklist item, convey:

- A task box and one action. Use `[x]` only for work verified complete and `[ ]` for incomplete, partial, blocked, or unverified work. Do not add an inline priority tag.
- The practical consequence of doing or skipping it, when this is not already obvious.
- The responsible role.
- An observable completion condition.
- The artifact or result that proves completion, when separate evidence is useful.

Name the evidence that should exist, such as a test report or signed acceptance record, but do not link to it or require the reader to open an issue or external page.

Write each checkbox as one natural sentence, or at most two short sentences when the consequence needs explanation. Weave the responsible role and observable result into the sentence. Do not repeat label-value fields for ownership, rationale, completion, or evidence under every item.

Order an overall checkpoint by logical product and development flow. Within each section, place unresolved blockers before lower-impact open work without hiding completed items:

- Keep completed and open tasks together in the development area where they belong so the reader sees the whole scope.
- Put non-blocking improvements in one optional section at the end, only when they add real value.
- Never emit inline priority tags, including translated equivalents.

When an item is partially implemented, keep it unchecked and state naturally in the same sentence what already exists and what still needs work. Do not invent a third checkbox state or add a status label.

For a scoped feature checklist, aim for 6–12 main items needed for a decision. For an overall project checkpoint, do not impose an item cap; include all material tasks and group them into readable development areas.

Default to a compact sentence that naturally includes the action, responsible role, and observable result. Add a second sentence only when the consequence or proof is not already obvious.

The completion condition must be observable. Avoid vague claims such as “works correctly,” “good quality,” or “fully tested” without saying what evidence demonstrates them.

## Decision conditions

Include only conditions relevant to development. Express applicable conditions in Thai for:

- When work may start.
- When the implementation is complete enough for acceptance testing.
- When development is blocked by an unresolved product or technical decision.

## Unanswered questions

List questions for which the project provides no evidence. For each question, state in Thai:

- Who can answer it.
- Which checklist item, scope boundary, or risk the answer would change.

If no material question remains, say so plainly in Thai.

## Language review

- Draft in Thai from the underlying facts; never translate completed English sentences.
- Prefer idiomatic Thai sentence order and familiar workplace phrasing over literal equivalents of English headings or management jargon.
- Avoid repeated subject labels, noun-heavy constructions, and passive wording that sounds translated.
- Avoid form-like micro-labels repeated under every checkbox. Rewrite the information as ordinary Thai sentences.
- Preserve established project terms that Thai stakeholders already use naturally, even when they are loanwords or product names.
- Do not force Thai replacements for familiar workplace terms such as version, build, release, deploy, or checklist. Explain an unfamiliar term once instead of inventing a new Thai word.
- Reject coined phrases that a Thai colleague would not normally say in a project meeting, even when they are technically accurate translations.
- Describe effects on people or work instead of relying on technical error names.
- Put the plain-Thai meaning before an unavoidable technical identifier.
- Spell out abbreviations and explain them on first use.
- Keep unavoidable product names and technical identifiers unchanged, then explain their practical significance. Keep source paths and commands in the analysis unless the user explicitly asks for them.
- Do not emit hyperlinks, issue numbers, or references to external pages. Restate the relevant fact in plain language inside the checklist.
- Read the result aloud from the perspective of a Thai manager or work owner who does not write software. Rewrite any sentence that feels like translated English, and explain any remaining English term, abbreviation, or tool detail that does not help that reader decide.
