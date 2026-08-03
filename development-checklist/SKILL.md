---
name: development-checklist
description: Inspect an existing software project and produce a practical, project-specific development checklist or overall development checkpoint in clear Thai for non-developers. Define each verified requirement clearly, map every development task needed to fulfill it, and show both completed and open work. Use for an existing project, feature, change, bug fix, migration, or integration when the user explicitly asks for a complete task list, status checklist, or requirement-by-requirement checkpoint. Ground every requirement and status in current code, documentation, tests, and configuration. Do not trigger for deployment, release, production-readiness, operational handoff, generic planning, English-only output, generic checklists, or greenfield work without an existing project.
---

# Define Project Development Checklist

Create a checklist that non-developers can use to track and accept software work in an existing project. Base it on project evidence rather than a generic template. Write the user-facing result in Thai.

## Workflow

### 1. Understand the intended outcome

- Distinguish development work from deployment, release, production operations, and project rollout before drafting.
- For an overall project development checkpoint, reconstruct the complete material scope across product behavior, code, data handling, integrations, tests, performance, maintainability, and technical documentation.
- Include verified completed work as well as partial, blocked, unverified, and not-started work. Do not reduce an overall checkpoint to a backlog of remaining tasks.
- Extract the material requirements before listing tasks. Distinguish what the system must achieve from the work needed to build or prove it.
- Exclude environment provisioning, production access, release packaging, Cutover, backup operations, user rollout, and handoff unless the user explicitly asks for them or they directly block development or testing.
- Identify the requested work, the affected users or organization, and the observable result expected at completion.
- Separate explicit user requirements from assumptions.
- Inspect the project before asking for missing information.
- Ask only questions whose answers materially change scope or outcome. When work can continue safely, state the assumption and proceed.

### 2. Inspect the project as it exists

- Read project instructions such as `AGENTS.md`, `README`, architecture documents, and release or deployment guides.
- Inspect relevant structure, dependency manifests, configuration, entry points, and modules.
- Find comparable implementations, call sites, tests, CI/CD, and operational practices.
- Inspect implementation, tests, migrations, documentation, and relevant history before marking any task complete.
- Keep discovery read-only. Do not change code or configuration unless the user requests that as a separate task.
- Use verified paths, commands, endpoints, database tables, and configuration values during analysis, but do not make the reader open them to understand the checklist.

Inspect only the areas relevant to the requested work. Stop broad exploration when the available evidence is sufficient.

### 3. Map requirements to completion work

Build a traceable chain for every requirement:

`requirement -> expected observable behavior -> implementation and verification tasks -> completion evidence -> status`

- State each requirement in plain language before its checklist.
- Include every material task needed to implement, verify, and document that requirement; do not list orphan tasks with no requirement.
- Keep each task under the requirement it fulfills. Create a separate cross-cutting requirement only when performance, maintainability, or shared infrastructure affects multiple behaviors.
- Do not invent a requirement when project sources conflict or remain silent. State the unresolved decision plainly and keep its decision and follow-up tasks unchecked.

Consider these lenses only when relevant:

- User journeys and business rules
- User interfaces, APIs, background jobs, and external systems
- Existing data, migrations, and backward compatibility
- Access control, secrets, privacy, and security
- Failures, logs, alerts, recovery, and rollback
- Testing, acceptance of developed behavior, maintainability, and technical documentation

Do not add a category merely to make the checklist look complete.

### 4. Write the checklist in Thai

Read [Thai output format](references/thai-output-format.md) and use it as the default structure. Remove sections that do not apply.

- Compose directly in natural Thai; never draft an English structure sentence by sentence and translate it.
- Match the terminology and tone used by native Thai writers in the project's existing business documents.
- Keep familiar software workplace loanwords when Thai teams naturally use them. Do not invent formal Thai substitutes that sound translated or are unlikely to be said in a project meeting.
- Make the result fully self-contained. Include the facts and decisions the reader needs directly in the checklist instead of sending them to another document.
- Do not include hyperlinks, issue numbers, issue-tracker references, or instructions such as "see" or "read" an external resource. Convert relevant issue or document content into a standalone action, risk, or completion condition.
- Reorder, merge, or reframe ideas when that makes the Thai flow more naturally; do not preserve English syntax or label order.
- Assume the reader cannot inspect code and has no software-development background.
- Write each item as a natural sentence centered on a concrete action. Let Thai sentence flow determine whether the action or responsible role comes first.
- Explain a technical term in plain Thai before showing its original identifier in parentheses.
- Add a glossary when technical terms, abbreviations, or system names cannot be avoided. Define their effect on people or work, not with more jargon.
- Give each item one verifiable outcome; split items that contain multiple actions.
- State why the item matters and what observable evidence proves completion.
- Separate verified facts, inferences, and unanswered questions.
- Use technical identifiers as supporting evidence, never as a substitute for explaining impact.
- Weave ownership and the observable result into the sentence when they are useful. Do not render them as repeated label-value fields.
- Use `[x]` only when project evidence proves the material task is complete. Use `[ ]` when work is partial, blocked, not started, or lacks enough evidence; state what exists and what remains inside the sentence.
- Present each requirement as a heading plus a short plain-Thai statement of the expected behavior, followed immediately by the checklist that fulfills it.

### 5. Run the quality gate

Confirm that the checklist:

- Matches the requested work and verified project state.
- Covers the full material development scope, including both verified completed work and work still open.
- Defines every material requirement clearly enough that a non-developer can understand the intended result before reading its tasks.
- Maps every checklist item to a requirement and includes the implementation, verification, and documentation work needed to satisfy that requirement.
- Treats a requirement as complete only when every material task beneath it is verified complete.
- Never marks an item complete merely because a file, class, page, or test exists; verify that the intended behavior and its relevant checks are present.
- Does not drift into deployment, release, infrastructure operations, Cutover, backup procedures, or user handoff unless explicitly requested.
- Gives every item an action, a clear responsible role, and an observable result without exposing those parts as a rigid form.
- Orders blocking work first and places optional improvements in a separate final section, without repeating priority tags on every item.
- Does not present unverified claims as facts.
- Remains understandable without opening a link, issue, source file, or supporting document.
- Contains no hyperlinks or issue references unless the user explicitly requests them.
- Lets a non-developer understand importance and ask useful progress questions.
- Sounds like it was written by a Thai project owner, not translated from an English template.
- Explains English terms, abbreviations, and system names on first use in reader-facing prose. Unavoidable product names and technical identifiers may remain unchanged when their practical meaning is explained.

If the user asks only for a checklist, return the checklist without changing code. If the user asks to save it, follow that project's documentation location and format.
