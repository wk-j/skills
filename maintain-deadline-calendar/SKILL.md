---
name: maintain-deadline-calendar
description: Keep the user's Google Calendar in sync with deadlines from GitHub issues and tasks assigned to them, and flag deadline and workload conflicts. Use when the user asks to sync, update, preview, or check their calendar against GitHub issues, due dates, deadlines, or task conflicts. Also run it quietly for a single issue whenever you start, analyze, implement, or close a GitHub issue, create an issue or document that states a due date, or notice that an issue's deadline changed, even if the user never mentions the calendar. Do not use for scheduling meetings with other people, for calendars unrelated to GitHub work, or for reminders that do not come from an issue.
---

# Maintain Deadline Calendar

Make GitHub deadlines visible where the user plans their day. Each issue that states a deadline gets exactly one calendar event, kept current as the issue changes, and every sync checks whether the deadlines collide with each other, with meetings, or with non-working days.

The value comes from trust: the user should be able to look at the calendar and believe it. That is why this skill never invents a deadline, never creates duplicates, and never deletes anything on its own.

## Modes

| Mode | When | Scope |
|---|---|---|
| **Full sync** | The user asks to sync or check their calendar against GitHub | Every open issue assigned to the user in the current repository |
| **Single-issue touch** | Ambient: you start, analyze, implement, or close an issue, or create an issue/document with a due date | That one issue |
| **Preview** | The user says preview, dry run, or "what would change", or you are testing the skill | Same as full sync, but write nothing |

**Scope defaults to the current repository** (`gh repo view --json nameWithOwner`). Widen to other repos or the whole organization only when the user asks. Issues in other repos usually belong to other projects, and mixing them into one sync produces events the user did not want.

## Prerequisites

- **`gh` authenticated.** GitHub Projects date fields need the `read:project` scope. If it is missing, continue with the other deadline sources and tell the user the fix: `gh auth refresh -h github.com -s read:project`. Do not run it yourself, because it opens an interactive browser flow.
- **Google Calendar connector tools** (`list_calendars`, `list_events`, `get_event`, `create_event`, `update_event`). They are often deferred, so load them through tool search before the first call. If no calendar connector exists, stop and tell the user to connect Google Calendar in their connector settings. Do not substitute an `.ics` file unless they ask for one.

## Target calendar

Use the user's primary calendar unless they name another one; resolve a named calendar through `list_calendars`. Write only to calendars where the user is owner or writer. Subscribed calendars (holidays, colleagues, family) are read-only inputs for conflict checks.

Read the calendar's `timeZone` from a `list_events` response. Interpret any deadline that has no explicit zone in that timezone, and leave the `timeZone` parameter unset on writes unless the issue itself states a zone.

## Step 1: Collect deadlines

Run the bundled collector. It reads issues through `gh` and prints JSON:

```bash
python3 -I <skill-dir>/scripts/collect_deadlines.py                  # full sync, current repo, assignee @me
python3 -I <skill-dir>/scripts/collect_deadlines.py --issue 1286     # single-issue touch (any state)
python3 -I <skill-dir>/scripts/collect_deadlines.py --repo OWNER/REPO --issue 12 --issue 15
```

Per issue it returns `deadline` (`value` as `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, `has_time`, `tz`, `source`, `raw`), all `candidates`, `sources_disagree`, `ambiguous` mentions, an `estimate` line when the issue states man-days or points, and the `sync_key`. Top-level `warnings` reports unreadable sources such as a missing `read:project` scope.

Sources in priority order: GitHub Projects date field (due/deadline/target/end) > title tag such as `[Duedate: 17-Oct-2026 06:00]` > the newest comment that states a deadline > issue body > milestone due date. Structured fields and titles are where teams keep the current deadline. A newer comment usually records a moved deadline, so it outranks the original body. A milestone date belongs to a whole batch of issues, so it is the weakest signal for any single issue.

A deadline counts only when a keyword is directly followed by a complete date. Loose keyword matching is the classic failure here: `ETA` matches inside `metadata`, and `due` matches `due to`. If you ever scan issues by hand instead of using the script, keep the same rule.

- **No deadline:** list the issue in the report and do not schedule it. A guessed date on a calendar is worse than no date, because the user will plan around it.
- **Ambiguous** (for example `ภายในวันที่ 24` with no month): report the raw text and leave it unscheduled until the user gives a full date.
- **`sources_disagree`:** use the top-priority candidate, and name the conflicting sources in the report so the user can fix the issue.

## Step 2: Find existing deadline events

Every event this skill manages ends its description with a sync key line:

```
gh-sync-key: OWNER/REPO#NUMBER
```

Look keys up with `list_events` using `fullText: "gh-sync-key"` over a wide window (60 days back to 365 days ahead), then match on the exact key. Do not rely on semantic `search_events` for this. It can miss an event whose title does not contain the issue number.

Also look near each deadline date for an **unkeyed look-alike**, an event whose title contains the issue number or a distinctive phrase from the issue title. The user or another agent may have made one by hand. Adopt it (update it and add the key) instead of creating a duplicate, and show its before → after in the report.

## Step 3: Plan operations

| Issue state | Calendar state | Action |
|---|---|---|
| Open, has deadline | No event | Create |
| Open, has deadline | Event differs in time, title, or reminders | Update |
| Open, has deadline | Event matches | Nothing |
| Open, deadline removed | Keyed event exists | Leave it and ask whether to delete |
| Closed | Keyed event exists | Prefix the title with `✓ Done · ` and keep the event as history |
| No longer assigned to the user | Keyed event exists | Leave it and ask whether to delete |
| No deadline | No event | Nothing; list the issue in the report |

Delete an event only when the user explicitly says to. A deleted event cannot be recovered from the connector, and the user may have added their own notes to it.

In preview mode, stop after this step and report the plan.

## Step 4: Event format

- **Title:** `Deadline HH:MM · #N <short title>` for a timed deadline, or `Deadline · #N <short title>` for a date-only one. Strip bracket tags such as `[Duedate: …]` and keep it under about 80 characters.
- **Time:** a timed deadline becomes a 30-minute block that **ends at the deadline**, so it sits just before the cutoff in day view. A date-only deadline becomes an all-day event on that date.
- **Availability:** free (`AVAILABILITY_FREE`). A deadline is a marker, not a meeting. Marking it busy would block other people's scheduling and make the conflict check count the marker as a commitment.
- **Description** (HTML is fine): the deadline plus where it came from, the issue link, the estimate if one was found, and the `gh-sync-key` line last. Do not copy issue bodies; they can hold customer data, and the calendar is visible on more devices and to more people than the repository.
- **Reminders:** popup 1 day before and 60 minutes before. If the deadline falls outside working hours or on a non-working day, add a popup at the end of the previous working day as well. For work due Saturday 06:00, a 05:00 Saturday reminder is useless.
- Set `notificationLevel: NONE` and add no attendees.

## Step 5: Check conflicts

Read the target calendar from now through the latest deadline (cap the window at about 30 days), plus any subscribed holiday calendars. Assume working hours of 09:00–18:00, Monday to Friday, in the calendar's timezone, and 1 man-day = 8 working hours, unless the user has said otherwise. Then flag:

1. **Overdue:** the deadline has passed and the issue is still open.
2. **Non-working deadline:** the deadline falls on a weekend, a holiday, or outside working hours. The effective deadline is the end of the previous working day; say so.
3. **Clustering:** two or more deadlines on the same day, or within one working day of each other.
4. **Capacity:** the sum of the stated estimates for deadlines in the window exceeds the free working hours left before them, after subtracting busy events. Count only issues that state an estimate, and say how many had none.
5. **Meeting overlap:** a busy event overlaps a deadline block, or the last working day before a deadline is mostly booked.

Report conflicts; do not resolve them. Moving a meeting or changing a deadline is a decision for the user and the issue's owner.

## Step 6: Apply and report

Apply the planned creates and updates, then report in the user's language:

1. One line: what changed (for example "Created 1, updated 2, no change 3").
2. A table: Issue | Deadline | Source | Action | event link.
3. Conflicts, most urgent first.
4. Issues without a deadline: count and numbers only.
5. Limitations: unreadable sources (with the fix command), ambiguous mentions, and sources that disagree.

Leave out any section that has nothing in it.

## Single-issue touch

When you start, analyze, implement, or close an issue, or create an issue or document that states a due date:

1. Run the collector with `--issue N`. When you create a new issue, do it after creation, because the sync key needs the issue number.
2. If the issue has a deadline, apply Steps 2–4 for that issue only and add one line to your final report (for example "Calendar: deadline for #1286 updated to 17 Oct 06:00").
3. If it has no deadline, do nothing and say nothing.

Do this at most once per issue per session, and never let it interrupt the main task. If the calendar connector is missing here, note it in one line and carry on with the main task.

## Safety rules

- Never delete events without an explicit instruction.
- Never invite attendees or send notifications.
- Never write to a calendar the user does not own or have writer access to.
- Never invent a deadline or silently resolve an ambiguous one.
- Never copy issue bodies into events.
- Before changing an event you did not create (no sync key), show its before → after.
