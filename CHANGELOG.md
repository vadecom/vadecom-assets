# Changelog

Every change to every standard in this repository, newest first. One line per
file per change, in the form `- path X.Y.Z — what changed`. Superseded rules
and artefacts are recorded here; they are never silently deleted.

## 2026-10-19

- brand/colors.md 2.1.1 — palette brought in line with vadecom.net (live since 2026-09-25, owner-approved 2026-09-26): closed set of eight. Yellow reinstated as `yellow-cta` (CTA buttons; accent on blue-base); `green-success` added as a functional colour (ticks, pricing, comparisons) with two tints for success components; three white overlays on blue-base added. Supersedes 2.0.0.
- README.md 1.0.1 — repository map updated to brand/colors.md 2.1.1.

## 2026-09-21

- README.md 1.0.0 — repository governance: the four stability rules, status vocabulary, version policy, change procedure, AI reading order.
- brand/colors.md 2.0.0 — colour palette defined as a closed set of six tokens with per-colour rules, opacity steps of blue-base, approved pairings, and a machine-readable block. Supersedes the April 2026 PDF colour guide; yellow removed from the palette.
- brand/archive/vadecom COLOR GUIDE2.pdf — SUPERSEDED by brand/colors.md 2.0.0; moved from brand/logos/ to brand/archive/.
- brand/archive/README.md 1.0.0 — archive index and rules.
- brand/logos/README.md 0.1.0 — logo asset index (draft; logo usage rules not yet decided).
- scripts/check_standards.py — consistency check added (frontmatter, one-authority-per-topic, changelog cross-check, palette drift).
- .github/workflows/standards.yml — CI added: secret scan (gitleaks, full history) and consistency check on every push and pull request.
