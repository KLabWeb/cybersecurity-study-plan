# CLAUDE.md — Claude Code handoff for the AppSec Study Plan build repo

Read this whole file before doing anything. It is the contract for every session.

## What this repo is

A Python/reportlab build system that renders a 56-page PDF, *Application Security
Engineering — Study Plan*, from `appsec_content.py`. The plan is a 33-week,
25-hour-per-week self-study curriculum taking the user (Kyle, five years full-stack
SWE, Philadelphia) from software engineering into an entry-level Application
Security Engineer role. The user is at the end of Week 4 (Phase I) as of 2026-09-16.

Current state: **build-61**, committed and tagged. Rendered PDF is in
`pdfs/Study_Plan_2026-09-16_build-61.pdf`. Working tree is clean.

The user reviews everything and decides everything. Your job is to make edits they
ask for, run the gates, show the diff, and commit only when told to.

## Standing rules (the user has had to repeat these — do not make them repeat again)

1. **Change only what was asked.** No unrequested restyling, rewording, added sections,
   "improvements," or tidying. If you notice something else wrong, say so in one line
   and wait.
2. **Never implement a decision the user has not made.** Mechanical fixes (a wrong
   number, a stale week reference, a broken cross-reference) can be applied and shown.
   Anything involving a choice — moving a step, picking a format, choosing a resource,
   adding or removing content — gets a question first.
3. **One question at a time.** Multiple questions in one message overwhelm the user.
   Ask one, wait, then the next.
4. **Every recommendation comes with reasons.** An opinion without reasoning is a
   failure. When presenting options, say which you think is best and why. Do not
   pressure for a decision; if the user says they are not ready, stop asking.
5. **Define every security term, tool, or acronym on first use** before relying on it.
   The user is new to cybersecurity. "DAST," "DVWA," "ZAP," "STRIDE" etc. all need a
   plain-language definition the first time they appear in a session.
6. **No ambiguous references.** Never say "option B" or "the second one." State the
   actual thing every time.
7. **Short responses.** The user has repeatedly flagged answers as too long. Say what
   is needed and stop.
8. **Verify before claiming.** Never say "all errors found," "everything checked," or
   "gates pass" without having run the check in that session. A pass on a gate means
   "nothing the gate looks for," not "the plan is correct." Read files; do not answer
   from memory of what they contained.
9. **No tappable option cards / multiple-choice widgets.** Ask in prose.
10. **Never announce what you are about to do instead of doing it.** If a change is
    approved, make it and show the diff.
11. **No data means ask, never guess.** If a claim depends on something you cannot read
    in this session (a TryHackMe room's contents, a lab, a page behind a login or a
    rate limit), do not infer it from the title or from what similar things usually
    contain. Say what you cannot see and ask the user to get it for you. Build-61's
    Phase I step 04 was written this way and was wrong.
12. **Verify against the whole file, every time.** When checking your own output against
    this file or any other, read all of its lines, not the one line you remember.

## Workflow (from COMMANDS.md — that file is the authority if they ever disagree)

### Draft + diff (no commit)
1. Edit `appsec_content.py` (source only; never edit the PDF).
2. Validate:
   ```
   python3 -c "import ast; ast.parse(open('appsec_content.py', encoding='utf-8').read())"
   python3 edit_check.py
   python3 timeline_ref_check.py
   python3 phase_partition_check.py
   python3 timeline_boundary_check.py
   python3 timeline_audit.py
   python3 prereq_check.py
   python3 structure_check.py
   python3 claim_check.py
   python3 step_dedup_check.py
   python3 step_actions_check.py      # informational; check its PREREQUISITE block says "none"
   ```
   All must pass. If one fails because of your change, fix the change. If one fails
   because the check's own assertion is stale (it has happened — see structure_check
   BSCP price, prereq_check step count in the changelog), fix the check and say so.
3. `git diff` and show it to the user. Stop. Wait for confirmation.

### Commit (only after the user says commit / continue)
4. Append an entry to `CHANGELOG_APPLIED.md` describing what changed and why, in the
   style of the existing entries (see the build-61 entry at the bottom).
5. `git add` the changed files; `git commit`; `git tag build-N` (N = last tag + 1).
   Meta/tooling commits do not get a build tag.
6. Render: `python3 build_appsec.py`. It runs the gates again and writes
   `Study_Plan_-_<today>.pdf` next to the scripts (or to `/mnt/user-data/outputs`
   if that directory exists). Copy the PDF to `pdfs/Study_Plan_<date>_build-N.pdf`
   and commit it. PDFs are tracked in git; `.zip` and `__pycache__` are not.
7. Report the build number.

### Step numbering
Steps are `step("NN", ...)` calls with literal numbers. If you insert or remove a
step, renumber the rest of that phase, then update:
- every `(step NN)` reference inside that phase (`grep -n 'step [0-9][0-9]' appsec_content.py`);
- the hand-encoded table in `step_actions_check.py` (`("PHASE","NN"): {...}`);
- the step count assertion in `prereq_check.py` (currently 62);
- any marker string in `prereq_check.py` HARD_CONCEPTS that pointed at moved text.
`claim_check.py` will catch a dangling step reference; it will not catch a wrong
action-table row.

## What the gates check (and what they cannot)

| Script | Catches |
|---|---|
| edit_check | OWASP LLM ID order, `<a>` balance, dead `#anchor` links |
| timeline_* / phase_partition / timeline_audit | week ranges partition 1–33, banners vs step tags, stale prose week numbers |
| prereq_check | tools/skills used before the step that teaches them; step count |
| structure_check | URL well-formedness, numbering, acronym expansion, Burp Pro/BSCP prices |
| claim_check | step-reference targets, Python-only tools aimed at Java/JS targets, orphan resources, tools used without a resource entry, one writeup-format definition, "N weeks" prose vs banner span, "end of Week N" milestones, Phase Summary achievements backed by steps |
| step_dedup / step_cross / step_actions | duplicate steps and actions; used-before-set-up (hand-encoded) |
| mentor_check / month_consistency | specific content facts |

None of them can check: whether a lab, room, or book chapter exists or has the described
content; whether a title matches its bullets; pedagogical fit. Those need a human or a
manual read. `LINE_BY_LINE_AUDIT.md` is the last full manual read (2026-09-13, against
build-60) with its findings F1–F20; all twenty are resolved in build-61.

Network: the chat container had no egress, so URL liveness has never been verified by a
script. In Claude Code you may have network — if so, a URL-liveness pass over every
`res(...)` and `<a href>` in `appsec_content.py` is the single most useful new check.

## Key facts about the plan (so you don't re-derive them)

- 62 steps across Phases 0–VIII; Phase IX is prose only. Phase → weeks: 0=1–3, I=4,
  II=5–7, III=8–14, IV=15–21, V=22, VI=23–25, VII=26–28, VIII=29–32 (33 weeks incl. slack).
- One writeup format everywhere (defined in Methodology, taught in Phase I step 04):
  finding, CVSS risk rating, summary, technical details and evidence, impact,
  remediation, code-review pattern. Every other step references it; none redefine it.
- Applications start Week 15 (Phase IV step 07) with "a dozen published writeups";
  main push Week 28 (Phase VII step 04) at 1–2 tailored applications/day.
- The user's own Phase 0 FastAPI app is: the Week 5 auth-audit target (II.04), the
  SAST target (IV.03), the LLM-endpoint host (IV.19), and the threat-model target
  (VI.03). WebGoat and DVWA are the DAST targets (IV.05 setup, IV.06 ZAP). Juice Shop
  is the full-assessment target (IV.18).
- WebGoat lessons in Phase I are practice with a notes-only log, not portfolio writeups.
- Costs stated in the plan: Burp Pro $499/yr, BSCP exam $99/attempt, Security+ $404.
- The user's GitHub is KLabWeb; five repos (plan, notes, tracker, FastAPI app, Docker demo).

## Things NOT to do

- Do not read `TRANSCRIPT_*` files or old handoff transcripts unless the user asks for a
  specific fact from one. They are large and the changelog already captures outcomes.
- Do not "clean up," reorganize, or consolidate files. Not the changelog, not the checks.
- Do not delete or rewrite CHANGELOG entries; append only.
- Do not push, publish, or contact any external service on the user's behalf.
- Do not add steps, resources, or prose because they "would help." Suggest in one line;
  wait.

## Open items (not yet done; do not start them unasked)

- 121: the GitHub profile README says the plan runs at "35 hour / week"; plan says 25.
- 122: FastAPI project README typos ("leared", "as a teach application").
- A URL-liveness check (see above) once a networked session exists.
- The user is nervous about the Week 5 audit (II.04). It stays in Week 5 by their
  decision; if they raise it again after the Week 5 labs, moving it is a one-step edit
  (see the build-61 changelog entry for the two placements considered).
