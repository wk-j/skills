---
name: cr-assessment
description: Assess a change request (CR) against an existing system, recommend the smallest change that genuinely satisfies it, and estimate mandays twice — built by a human developer versus built with a coding agent — so the two can be compared. Classifies the CR on a change tier ladder from config-only to architectural, maps blast radius from real code evidence, and flags when the minimal option is the expensive one. Use before the build decision, when asked whether a CR is worth doing, what it will break, how many mandays it costs, whether an agent would be faster, or which approach to take. Do not use after the decision is made and the user wants a task list, or for greenfield work with no existing system to change.
---

# Assess a Change Request

Judge a proposed change against the system that already exists, then recommend the smallest change that genuinely satisfies it. Write the user-facing result in Thai.

## Boundary

Use this skill when the user asks:
- Whether a CR is worth doing, what it will cost, or what it will break.
- Which of several approaches to take for a requested change.
- Whether a CR forces an architectural change.
- For an impact analysis or options paper before work starts.

Do not use this skill when:
- The decision is already made and the user wants tasks and status — use `development-checklist`.
- The input is a GitHub issue needing a structured analysis document — use `analyze-github-issue`, then assess its output with this skill if a decision is still open.
- The user wants the change implemented, not assessed.
- There is no existing system to change. This skill reasons about impact on what exists; greenfield work has no blast radius to map.

## Core principle

**Propose the lowest tier that genuinely satisfies the CR. To propose a higher tier, name what fails at the lower one.**

"Minimal change" is not a preference for doing less. It is a requirement to justify every increment of change against the system you already have. An unjustified tier jump is over-engineering; an unjustified tier stop is a workaround that someone pays for later. Both are failures of this skill.

## Change tier ladder

Classify every option on this ladder. The tier, not the line count, is what makes a change expensive.

| Tier | What changes | Test |
| --- | --- | --- |
| T1 | Configuration or data only | No code changes at all |
| T2 | New code, additively | Existing callers behave exactly as before |
| T3 | Existing behavior modified | Existing callers get different results |
| T4 | A contract changes | API shape, DB schema, event payload, or file format changes; needs migration and coordination with consumers |
| T5 | Architecture changes | New component, new external dependency, new boundary between parts, or an existing invariant no longer holds |

Cost rises sharply at T4 and again at T5, because those tiers pull in people and systems outside the change itself. A T3 change touching twenty files is usually cheaper than a T4 change touching two.

Report the tier of every option. Never report a tier you have not grounded in step 2.

## Workflow

### 1. Pin down what the CR actually asks for

- Separate the requested **outcome** from the requested **solution**. Users often write a CR as an implementation ("add a field to the export"), when the outcome ("finance needs to reconcile by cost centre") admits a cheaper change. Assess the outcome.
- Restate the CR in one sentence. If two readings lead to different tiers, that ambiguity is a finding — record it rather than picking one silently.
- List what the CR explicitly excludes, and what a reader would reasonably assume is included.
- Accept a CR in any form: a ticket, a document, an email, or a sentence in chat. Do not require a template.

### 2. Locate the CR in the existing system

Grounding rule: **no tier, no impact, and no size without a file path.** An assessment that names no code is a guess with formatting.

- Read project instructions such as `AGENTS.md`, `CLAUDE.md`, `README`, and architecture documents before reading code.
- Find the code, configuration, schema, and tests the CR actually touches. Name them.
- Find how the current behavior is produced, not just where it lives.
- Look for a comparable change already made in the repository. A precedent is the strongest evidence of what a change of this shape really costs here.
- Keep discovery read-only. Do not change code while assessing.
- Mark anything you could not verify as unverified. Never present an unread assumption in the same voice as a read fact.

### 3. Map the blast radius

For each anchor found in step 2, find what depends on it:
- Callers, and callers of callers where behavior propagates.
- Stored data already written in the old shape, and whether it must be migrated or can be read leniently.
- Published contracts: API consumers, event subscribers, exports, reports, integrations.
- Background jobs, scheduled tasks, and caches holding the old shape.
- Tests that encode the current behavior as intended.
- Permissions and audit paths, when the CR touches who may do what.

A CR that reaches a published contract or stored data is at least T4, whatever its code size suggests.

### 4. Build options, lowest tier first

Produce two or three real options. Start by asking what the T1 or T2 answer would be, even when you expect to reject it — stating why the cheap option fails is what makes the recommended option credible.

For each option record: the tier, what it changes, what it leaves alone, what it forecloses later, and how it is rolled back or turned off.

Reject fake options. An option nobody would choose is padding. If only one approach is viable, say so and explain what rules the others out.

### 5. Check the minimal-change trap

Before recommending the lowest tier, test it against these. If any holds, the minimal option is the expensive one and you must say so plainly:

- It adds a special case to a path that other features rely on staying general.
- It makes an invariant hold sometimes rather than always. Partial invariants are what turn later changes into archaeology.
- It duplicates logic that already exists, leaving two copies to keep in step.
- It stores data in a shape that contradicts what the schema claims.
- The same CR, or a near neighbour, has already been absorbed this way before. A second workaround at the same spot is evidence the design, not the request, is wrong.

When you flag the trap, estimate when the debt comes due: the next CR that touches this area, a specific upcoming milestone, or the point where a second consumer appears. A debt with no due date gets ignored.

### 6. Estimate mandays two ways

Estimate every option twice: built by a human developer, and built by a developer working with a coding agent. Report both so they can be compared.

Both columns measure the same thing: **human mandays consumed.** The agent column is not how long the agent runs. It is how much of a person's day the work still costs when an agent does the typing, including the time spent directing it and reviewing what it produced. An agent estimate that omits review is not an estimate, it is a sales pitch.

#### Estimate by work type, not as one number

Agent leverage is not uniform. Split each option's work into these four types, estimate each, then total them. The split is what makes the comparison honest — and it is usually more informative than the totals.

| Work type | Examples | Agent leverage |
| --- | --- | --- |
| Mechanical | Boilerplate, scaffolding, mechanical refactor, test cases against a settled spec, doc updates | High |
| Design and decision | Choosing the approach, resolving ambiguity in the CR, deciding the data shape | Low |
| Integration and verification | Making it work end to end, debugging, edge cases, checking the blast radius held | Medium |
| Coordination and human gates | Agreeing a contract with another team, product sign-off, migration window, code review, UAT | None |

Two consequences follow, and the assessment should state them when they apply:

- **Agent advantage shrinks as tier rises.** A T1 or T2 change is mostly mechanical, so the agent column drops sharply. A T4 or T5 change is dominated by coordination and design, which do not compress — the two columns converge. Reporting a large agent saving on a T5 is almost always an error in the split.
- **Coordination is calendar, not effort.** Waiting two weeks for another team's sign-off is not two weeks of mandays. Keep waiting time out of the manday figures and note it separately as elapsed time, or the comparison silently double-counts.

#### Review cost scales with risk, not with volume

Charge review to the agent column explicitly. Reviewing generated code for a T3 behavior change costs more per line than for T2 additive code, because the reviewer must confirm what did *not* change. On a high-risk change, review can erase most of the mechanical saving. Say so when it does.

#### State the assumptions the numbers rest on

An estimate without its assumptions cannot be checked or reused. Record:

- The assumed developer: familiar with this codebase, or new to it.
- Whether usable tests already cover the affected area.
- Whether the agent has the context it needs here — project instructions, readable structure, existing similar code to follow.
- Anything that would change the numbers materially if it turned out false.

#### Report a range and a confidence

Give a range, not a point value, and label the confidence as high, medium, or low with a reason. Where the CR contains unresolved ambiguity, the range must widen to cover both readings — never quietly estimate only the cheaper one.

State plainly that these are estimates for comparing options, not a commitment or a quotation.

### 7. Write the assessment in Thai

Read [Thai output format](references/thai-output-format.md) and follow it. Compose directly in Thai; never write English sentences and translate them.

### 8. Run the quality gate

Confirm the assessment:

- Names a recommended option in the first paragraph, with its tier and both manday figures.
- Grounds every tier, impact, and manday claim in a named file, schema, or configuration.
- Explains why the lowest tier considered was accepted or rejected.
- Separates verified facts, inferences, and open questions, and never presents one as another.
- States the blast radius in terms of what people and systems notice, not only which files change.
- Applies the step-5 trap check explicitly, and says so when the trap does not apply.
- Gives every option a rollback or disable path, or says plainly that there is none.
- Gives every option both manday estimates, broken down by the four work types, with the assumptions and confidence stated.
- Charges directing and reviewing the agent to the agent column, and never reports an agent saving on a coordination-heavy option without explaining it.
- Keeps waiting time out of the manday figures and reports it separately as elapsed time.
- Labels the estimates as a basis for comparison, not as a commitment.
- Names who must answer each open question, and which part of the recommendation would change.
- Reads as though a Thai tech lead wrote it for a decision maker, not as a translated template.

If the assessment cannot reach a recommendation because a product decision is missing, say that plainly and name the decision. An honest blocked assessment is more useful than a confident one built on a guessed requirement.

## Output destination

Return the assessment in the reply by default. Write it to a file only when the user asks, and then follow the project's existing documentation location and naming.
