---
title: VadeCom Standards — How this repository works
topic: governance
version: 1.0.0
updated: 2026-09-21
status: authoritative
---

# VadeCom Standards (`vadecom-assets`)

The single authoritative reference for VadeCom brand, design and policy
standards. It is public on purpose: humans and AI tools (ChatGPT, Claude,
image and design generators) read it when they produce anything for VadeCom.

**A standard here is a decision.** Existing designs, decks, templates and
brand kits are measured against these files — they are never evidence for what
a file should say. No rule in this repo is justified by "we always did it this
way" or "the last batch used this"; rules are stated as decisions and changed
by decision.

الملخص بالعربية: هذا الريبو هو المرجع الوحيد لمعايير هوية وتصميم وسياسات فاديكوم.
المعيار هنا قرار، والتصاميم القائمة تُقاس عليه ولا تُستخدم دليلاً عليه.

## The four stability rules

1. **One authority per topic.** Exactly one file owns each topic (the
   `topic:` key in its frontmatter). Anything anywhere that disagrees with it —
   another file, a template, a deck, a generated image — is a bug to be fixed,
   not a second opinion.
2. **Every rule file carries frontmatter:** `title`, `version` (semver),
   `updated` (`YYYY-MM-DD`), `status`. Without it, the file is a **draft, not a
   standard**, and nothing may be measured against it.
3. **Changes are announced.** Bump the version, add a `## Changelog` entry in
   the file, and add a line in [`CHANGELOG.md`](CHANGELOG.md). Superseded rules
   are recorded as superseded — in the file's changelog, in `CHANGELOG.md`, and
   by moving the old artefact to `brand/archive/` — never silently deleted.
4. **Drift is checked, not trusted.** CI runs a secret scan and a consistency
   check on every push ([`.github/workflows/standards.yml`](.github/workflows/standards.yml)).
   A red check is a bug in the repo, not in the check.

### Status vocabulary

| `status`        | Meaning                                                              |
|-----------------|----------------------------------------------------------------------|
| `authoritative` | The standard. Measure everything against it.                         |
| `draft`         | Proposed or incomplete. Not binding. (Also any file without frontmatter.) |
| `superseded`    | Replaced by a newer version or file. Kept for the record; do not use. |

### Version bumps

- **MAJOR** — a rule changes meaning (a colour removed, a "never" becomes an
  "only", a topic moves to another file).
- **MINOR** — a rule is added without contradicting existing ones.
- **PATCH** — wording, typos, formatting, added examples.

## Repository map

| Path | Owns | Status |
|------|------|--------|
| [`brand/colors.md`](brand/colors.md) | **Colour** — the closed palette, per-colour rules, pairings, machine-readable block | authoritative 2.0.0 |
| [`brand/logos/`](brand/logos/) | VadeCom logo files and their index | draft |
| [`brand/almonaseb/`](brand/almonaseb/) | Almonaseb sub-brand assets (own palette and fonts) | draft |
| [`brand/archive/`](brand/archive/) | Superseded artefacts, kept for the record | superseded |
| [`proposals/`](proposals/) | Proposal sources and publishing notes | not a standard |
| [`CHANGELOG.md`](CHANGELOG.md) | Every change to every standard, newest first | — |
| [`scripts/check_standards.py`](scripts/check_standards.py) | The consistency check CI runs | — |

Topics that do not yet have a file (typography, logo usage, layout, tone of
voice, social templates) are **undecided**, not implicitly decided by existing
work. Until a file with `status: authoritative` exists, the only binding rule
for those topics is `brand/colors.md`.

## How to change a standard

1. Edit the owning file only. If two files would need to change for one topic,
   the topic has two owners — fix that first.
2. Bump `version` and `updated` in the frontmatter.
3. Add the entry at the top of the file's `## Changelog`.
4. Add one line under today's date in `CHANGELOG.md`:
   `- path/to/file.md X.Y.Z — what changed`.
5. If a rule or artefact is replaced: mark it superseded in both changelogs and
   move any old file to `brand/archive/`.
6. Push. CI must be green before the change counts.

A hex value quoted deliberately as a counter-example or a superseded value
carries the marker `[off-palette]` (or `[off-palette: #XXXXXX]`) **on the same
line**, so the drift check knows it is intentional.

## For AI tools

Read [`brand/colors.md`](brand/colors.md) first — the palette is a closed set;
use nothing outside it. Parse the first ```` ```json ```` block in that file
(`"id": "vadecom-palette"`) for the exact tokens. Treat any file without
frontmatter, or with `status: draft`, as non-binding. Never infer a rule from a
logo PNG, a proposal, or a previous design in this repo.

## What lives elsewhere

Internal material — client work, pricing, CRM configuration, server details,
credentials — belongs in the private `Vadecom-os` repository. Only public-safe
standards are published here.

## Changelog

- **1.0.0 — 2026-09-21** — Repository governance established: the four
  stability rules, status vocabulary, version bump policy, repository map,
  change procedure, AI reading order.
