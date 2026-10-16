#!/usr/bin/env python3
"""Collect deadlines from GitHub issues as JSON for calendar sync.

Reads issues through the `gh` CLI and extracts an explicit deadline for each one
from (in priority order) a GitHub Projects date field, a title tag such as
`[Duedate: 17-Oct-2026 06:00]`, the newest comment that states one, the issue
body, and finally the milestone due date. A deadline is only reported when a
keyword is followed by a complete date; anything vaguer is reported as
ambiguous instead of guessed.

Usage:
  collect_deadlines.py                       # open issues assigned to @me in the current repo
  collect_deadlines.py --repo OWNER/REPO
  collect_deadlines.py --issue 1286 --issue 1290   # specific issues, any state
  collect_deadlines.py --assignee someone

Standard library only. Output goes to stdout as JSON.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys

ISSUE_FIELDS = "number,title,url,state,assignees,milestone,body,comments,updatedAt,closedAt"

EN_MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "oct": 10,
    "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}
TH_MONTHS = {
    "ม.ค.": 1, "มกราคม": 1, "ก.พ.": 2, "กุมภาพันธ์": 2, "มี.ค.": 3, "มีนาคม": 3,
    "เม.ย.": 4, "เมษายน": 4, "พ.ค.": 5, "พฤษภาคม": 5, "มิ.ย.": 6, "มิถุนายน": 6,
    "ก.ค.": 7, "กรกฎาคม": 7, "ส.ค.": 8, "สิงหาคม": 8, "ก.ย.": 9, "กันยายน": 9,
    "ต.ค.": 10, "ตุลาคม": 10, "พ.ย.": 11, "พฤศจิกายน": 11, "ธ.ค.": 12, "ธันวาคม": 12,
}
TH_MONTH_ALT = "|".join(sorted((re.escape(m) for m in TH_MONTHS), key=len, reverse=True))

# A keyword must be followed by a date for the line to count as a deadline.
# Plain "due" is allowed only when a date follows directly, so "due to ..." never matches.
KEYWORD_RE = re.compile(
    r"(?i)(?:\bdue\s*date\b|\bduedate\b|\bdeadline\b|\btarget\s*date\b|\bdue\s*(?:by|on)\b|\bdue\b"
    r"|กำหนดส่ง|กำหนดเสร็จ|ครบกำหนด|ภายในวันที่|ส่งภายใน)"
)
LEAD_RE = re.compile(r"^[\s:：=\-–—*_\[\(]*(?:(?:on|by|at)\s+|วันที่\s*|วัน\s*)?", re.I)
TIME_RE = r"(?:[\s,T]+(?:at\s+|เวลา\s*)?(\d{1,2})[:.](\d{2})\s*(am|pm|น\.?)?)?"
TZ_RE = r"(?:\s*(?:GMT|UTC)?\s*(Z|[+-]\d{2}:?\d{2})(?![\d:]))?"

DATE_PATTERNS = [
    # 2026-10-17, 2026-10-17 06:00, 2026-10-17T06:00
    ("iso", re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})" + TIME_RE + TZ_RE)),
    # 17-Oct-2026, 17 Oct 2026, 17 October 2026 06:00
    ("dmy_en", re.compile(r"(\d{1,2})[\s\-/]+([A-Za-z]{3,9})\.?[\s\-/,]+(\d{4})" + TIME_RE + TZ_RE)),
    # Oct 17, 2026
    ("mdy_en", re.compile(r"([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})" + TIME_RE + TZ_RE)),
    # 17 ต.ค. 2569, 17 ตุลาคม 2026
    ("dmy_th", re.compile(r"(\d{1,2})\s*(" + TH_MONTH_ALT + r")\s*(\d{4})" + TIME_RE + TZ_RE)),
    # 17/10/2026 (read as day/month/year)
    ("dmy_num", re.compile(r"(\d{1,2})/(\d{1,2})/(\d{4})" + TIME_RE + TZ_RE)),
]

# "md" counts only right after a number ("3 md", "0.5md"), so file names like CONTEXT.md never match.
ESTIMATE_RE = re.compile(
    r"(?i)(?:(?:man-?days?|mandays?|story\s*points?|\bestimate[sd]?\b|ประมาณการ|เวลาที่ใช้)[^\n]{0,80}?\d"
    r"|\b\d+(?:\.\d+)?\s*md\b)"
)
FENCE_RE = re.compile(r"```.*?```", re.S)


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:3])} failed: {proc.stderr.strip()}")
    return proc.stdout


def build_value(year: int, month: int, day: int, hh, mm, ampm, tz):
    if year >= 2400:  # Buddhist Era year
        year -= 543
    try:
        date = dt.date(year, month, day)
    except ValueError:
        return None
    if hh is None:
        return {"value": date.isoformat(), "has_time": False, "tz": None}
    hour, minute = int(hh), int(mm)
    if ampm and ampm.lower() in ("am", "pm"):
        if hour == 12:
            hour = 0
        if ampm.lower() == "pm":
            hour += 12
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    return {"value": f"{date.isoformat()}T{hour:02d}:{minute:02d}", "has_time": True, "tz": tz}


def parse_date(text: str):
    """Parse a date at the very start of `text`; return a deadline dict or None."""
    for kind, pattern in DATE_PATTERNS:
        m = pattern.match(text)
        if not m:
            continue
        g = m.groups()
        if kind == "iso":
            year, month, day = int(g[0]), int(g[1]), int(g[2])
            rest = g[3:]
        elif kind == "dmy_en":
            month = EN_MONTHS.get(g[1].lower())
            if not month:
                continue
            day, year = int(g[0]), int(g[2])
            rest = g[3:]
        elif kind == "mdy_en":
            month = EN_MONTHS.get(g[0].lower())
            if not month:
                continue
            day, year = int(g[1]), int(g[2])
            rest = g[3:]
        elif kind == "dmy_th":
            day, month, year = int(g[0]), TH_MONTHS[g[1]], int(g[2])
            rest = g[3:]
        else:  # dmy_num
            day, month, year = int(g[0]), int(g[1]), int(g[2])
            rest = g[3:]
        value = build_value(year, month, day, rest[0], rest[1], rest[2], rest[3])
        if value:
            value["format"] = kind
            return value, m.group(0)
    return None


def scan_text(text: str, source: str, url: str | None, created_at: str | None):
    """Return (deadlines, ambiguous) found in one text segment."""
    found, ambiguous = [], []
    clean = FENCE_RE.sub(" ", text or "")
    for line in clean.splitlines():
        for km in KEYWORD_RE.finditer(line):
            tail = line[km.end():]
            tail = tail[LEAD_RE.match(tail).end():]
            parsed = parse_date(tail)
            snippet = (km.group(0) + line[km.end():km.end() + 60]).strip()
            if parsed:
                value, matched = parsed
                found.append({**value, "source": source, "raw": (km.group(0) + " " + matched).strip(),
                              "source_url": url, "stated_at": created_at})
            elif re.match(r"\d", tail) or re.match(r"(?:" + TH_MONTH_ALT + r")", tail):
                ambiguous.append({"source": source, "raw": snippet[:100], "source_url": url,
                                  "reason": "keyword followed by an incomplete or invalid date"})
    return found, ambiguous


def extract_estimate(texts: list[str]):
    for text in texts:
        for line in FENCE_RE.sub(" ", text or "").splitlines():
            if ESTIMATE_RE.search(line):
                return re.sub(r"[*_`#>|]", "", line).strip()[:160]
    return None


def fetch_projects(repo: str, numbers: list[int]):
    """Map issue number -> list of project date fields. Returns (map, readable, warning)."""
    owner, name = repo.split("/", 1)
    result: dict[int, list[dict]] = {}
    for i in range(0, len(numbers), 40):
        chunk = numbers[i:i + 40]
        aliases = "\n".join(
            f"i{n}: issue(number: {n}) {{ projectItems(first: 10) {{ nodes {{ project {{ title }} "
            f"fieldValues(first: 40) {{ nodes {{ ... on ProjectV2ItemFieldDateValue {{ date "
            f"field {{ ... on ProjectV2FieldCommon {{ name }} }} }} }} }} }} }} }}"
            for n in chunk
        )
        query = f'query {{ repository(owner: "{owner}", name: "{name}") {{ {aliases} }} }}'
        proc = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}"], capture_output=True, text=True)
        if proc.returncode != 0:
            if "read:project" in proc.stderr or "read:project" in proc.stdout:
                return {}, False, ("GitHub Projects fields are unreadable: the gh token lacks the read:project "
                                   "scope. Fix: gh auth refresh -h github.com -s read:project")
            return {}, False, f"GitHub Projects query failed: {proc.stderr.strip()[:200]}"
        data = json.loads(proc.stdout).get("data", {}).get("repository", {}) or {}
        for n in chunk:
            items = ((data.get(f"i{n}") or {}).get("projectItems") or {}).get("nodes") or []
            for item in items:
                ptitle = (item.get("project") or {}).get("title")
                for fv in (item.get("fieldValues") or {}).get("nodes") or []:
                    if fv and fv.get("date"):
                        result.setdefault(n, []).append(
                            {"project": ptitle, "field": (fv.get("field") or {}).get("name"), "date": fv["date"]})
    return result, True, None


DEADLINE_FIELD_RE = re.compile(r"(?i)due|deadline|target|end|finish|กำหนด")


def collect(repo: str, assignee: str, issues: list[int], all_states: bool):
    if issues:
        raw = [json.loads(run(["gh", "issue", "view", str(n), "--repo", repo, "--json", ISSUE_FIELDS]))
               for n in issues]
    else:
        raw = json.loads(run(["gh", "issue", "list", "--repo", repo, "--assignee", assignee,
                              "--state", "all" if all_states else "open", "--limit", "300",
                              "--json", ISSUE_FIELDS]))

    projects, projects_readable, project_warning = fetch_projects(repo, [i["number"] for i in raw]) if raw else ({}, True, None)
    warnings = [project_warning] if project_warning else []

    out = []
    for issue in raw:
        n = issue["number"]
        candidates, ambiguous = [], []

        for pf in projects.get(n, []):
            if pf["field"] and DEADLINE_FIELD_RE.search(pf["field"]) and not re.search(r"(?i)start", pf["field"]):
                candidates.append({"value": pf["date"], "has_time": False, "tz": None, "format": "project",
                                   "source": f"project:{pf['project']}/{pf['field']}", "raw": pf["date"],
                                   "source_url": issue["url"], "stated_at": None})

        f, a = scan_text(issue["title"], "title", issue["url"], None)
        candidates += f
        ambiguous += a

        comments = sorted(issue.get("comments") or [], key=lambda c: c.get("createdAt") or "", reverse=True)
        comment_hits = []
        for c in comments:
            f, a = scan_text(c.get("body"), "comment", c.get("url"), c.get("createdAt"))
            comment_hits += f
            ambiguous += a
        candidates += comment_hits[:1]  # newest comment that states a deadline

        f, a = scan_text(issue.get("body"), "body", issue["url"], None)
        candidates += f[:1]
        ambiguous += a

        ms = issue.get("milestone") or {}
        if ms.get("dueOn"):
            candidates.append({"value": ms["dueOn"][:10], "has_time": False, "tz": None, "format": "milestone",
                               "source": f"milestone:{ms.get('title')}", "raw": ms["dueOn"],
                               "source_url": issue["url"], "stated_at": None})

        distinct = {c["value"] for c in candidates}
        out.append({
            "number": n,
            "title": issue["title"],
            "url": issue["url"],
            "state": issue["state"],
            "closed_at": issue.get("closedAt"),
            "updated_at": issue.get("updatedAt"),
            "assignees": [a["login"] for a in issue.get("assignees") or []],
            "sync_key": f"{repo}#{n}",
            "deadline": candidates[0] if candidates else None,
            "sources_disagree": len(distinct) > 1,
            "candidates": candidates,
            "ambiguous": ambiguous,
            "estimate": extract_estimate([issue.get("body") or ""] + [c.get("body") or "" for c in comments]),
        })

    return {
        "repo": repo,
        "assignee": None if issues else assignee,
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "projects_readable": projects_readable,
        "warnings": warnings,
        "issues": out,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", help="OWNER/REPO (default: repo of the current directory)")
    parser.add_argument("--assignee", default="@me", help="assignee filter for list mode (default: @me)")
    parser.add_argument("--issue", type=int, action="append", default=[], help="specific issue number (repeatable)")
    parser.add_argument("--all-states", action="store_true", help="list mode: include closed issues")
    args = parser.parse_args()

    try:
        repo = args.repo or run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]).strip()
        json.dump(collect(repo, args.assignee, args.issue, args.all_states), sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    except RuntimeError as exc:
        json.dump({"error": str(exc)}, sys.stdout)
        sys.stdout.write("\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
