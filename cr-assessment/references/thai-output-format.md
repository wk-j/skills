# Thai Output Format

Guidance for what the assessment must cover, not a sentence-by-sentence template. Compose directly in Thai, drop sections that do not apply, and never leave a placeholder. Choose headings and phrasing a Thai tech lead would actually use when writing to a decision maker.

Read the project's existing Thai-facing documents first and reuse their established terms and level of formality.

## Two audiences, one document

The body is written for someone who decides but does not read code. The evidence section at the end is written for whoever will build it. Keep them apart: file paths, schema names, and commands belong in the evidence section, not scattered through the recommendation. The decision maker must be able to stop reading before that section and still have decided correctly.

## Title

Name the change and the decision at stake, the way a Thai project owner would refer to it in a meeting. Do not translate the CR's English title literally.

## Recommendation first

Open with the answer, not the background. Cover in one short paragraph plus a line or two:

- The recommended option and, in plain Thai, what it does.
- Its tier and both manday figures, with the tier explained by consequence rather than by number — a T4 is "ต้องแก้ฝั่งที่เรียกใช้ด้วย และต้องนัดกับทีมอื่น", not "tier 4".
- The single biggest risk if it proceeds.
- Whether any decision must be made by someone else before work can start.

A reader who reads only this section must be able to approve, reject, or ask the right question.

## What the CR is asking for

State the requested outcome in one or two plain sentences, separated from whatever solution the requester proposed. When those differ, say so — it is often where the cheaper option comes from.

Record any ambiguity that changes the answer, and say which reading you assessed.

List what is out of scope, including what a reader would otherwise assume is included.

## Where it lands in the current system

Explain, without paths, what part of the system this touches and what that part currently does for users. The reader needs to understand what is at stake, not the file layout.

Where the current behavior is genuinely surprising and that surprise drives the cost, explain it here rather than burying it in the evidence section.

## Impact

Describe the blast radius as things people and systems will notice:

- Who sees different behavior, and how.
- What existing data is affected, and whether it must be converted.
- Which other teams, integrations, or external consumers must be told or must change something.
- What stops working if this ships without the accompanying work.

Use a table only when the ideas are genuinely parallel. Do not turn prose into a form.

## Options

Present each option under a Thai heading naming the approach, then cover:

- What it changes and what it deliberately leaves alone.
- Its tier expressed as consequence, and its two manday figures.
- What it makes harder or forecloses later.
- How it is turned off or rolled back, or that it cannot be.

Always include the cheapest option that was considered, even when rejected, and say what breaks under it. A rejected cheap option is evidence the recommendation is grounded; omitting it makes the recommendation look like a preference.

Do not include an option nobody would choose. If only one approach is viable, say so and explain what rules out the others.

## Manday comparison

Compare the options in one table the reader can scan, with a column for a human developer and a column for a developer working with a coding agent. Make clear in a sentence above it that both columns count human คน-วัน — the agent column already includes directing the agent and reviewing its output, so the two columns are comparable.

Below the table, break the recommended option down by work type: งานกลไก, งานตัดสินใจและออกแบบ, งานประกอบและตรวจสอบ, and งานที่ต้องรอคนอื่น. This is where the reader learns *why* the gap between the columns is the size it is, which matters more than the totals. Keep the four names consistent wherever they appear.

Explain the gap in one or two sentences of plain Thai. If the agent column saves little, say why — usually because the work is mostly decisions and coordination, which an agent does not compress. If it saves a lot, say which part is mechanical enough for that to hold.

Report waiting time separately from mandays, phrased as elapsed time, so nobody reads a two-week wait as ten mandays of work.

State the assumptions the numbers rest on: whether the developer already knows this codebase, whether tests cover the affected area, and whether the agent has enough project context to work here. Give a range with a confidence level and a one-line reason for that level.

Close the section by saying plainly that these figures are for comparing options, not a quotation or a commitment.

## When the cheapest option is the expensive one

Include this section whenever the step-5 trap check fires. Say plainly, in Thai:

- Which shortcut the cheap option requires.
- What it makes fragile or inconsistent, in terms of future work rather than code aesthetics.
- When the cost comes due: the next change to this area, a named milestone, or the arrival of a second consumer.

Omit the section when the trap does not apply, but say once in the recommendation that the cheap option was checked and is genuinely safe. Silence reads as if the check was skipped.

## Risks and what must not break

List only risks specific to this change. Skip generic project risks.

For each: what could go wrong, what the reader would observe if it did, and what reduces it. Name the invariants and guarantees this change must preserve — data that must stay correct, permissions that must stay enforced, contracts other systems already depend on.

## Open questions

For each question the project provides no answer to, state who can answer it and which part of the recommendation their answer would change. If nothing material is open, say so plainly.

## Evidence

The section for whoever builds it. Here, and only here, name file paths, schemas, configuration keys, and prior comparable changes that support the tier and size claims. Mark clearly what was read and verified versus what was inferred but not checked.

## Language review

- Draft in Thai from the facts; never translate finished English sentences.
- Keep technical terms in English inside the Thai sentence — identifiers, paths, commands, API names, and established jargon such as deploy, schema, endpoint, migration, rollback, cache. Do not transliterate them into Thai script or invent Thai equivalents.
- When a reader may not know a term, keep the term and explain what it does in a separate clause, rather than substituting a Thai word for it.
- Explain a tier by its consequence for the work, never by its number alone.
- Write plain declarative sentences without ครับ or ค่ะ. This is a document, not a message.
- Avoid noun-heavy constructions built on การ and ความ where a verb reads better, and avoid ถูก where naming who acts is clearer.
- Write manday figures as plain numbers with the Thai unit the team already uses (คน-วัน or manday). Do not convert them into story points or t-shirt sizes.
- Read it back as a Thai manager who must approve or reject this. Rewrite any sentence that sounds translated, and cut any sentence that does not help them decide.
