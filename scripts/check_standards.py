#!/usr/bin/env python3
"""
Consistency check for vadecom-assets (stability rule 4: drift is checked, not trusted).

Checks
  1. Frontmatter  — every rule file (*.md, except CHANGELOG.md and brand/archive/**)
                    that has frontmatter must carry title, version (semver),
                    updated (YYYY-MM-DD, not in the future), status
                    (draft | authoritative | superseded). A file WITHOUT
                    frontmatter is reported as a draft (warning, not failure).
  2. One authority — no two files with status: authoritative share a `topic`.
  3. Announced     — every non-draft rule file has a "## Changelog" section that
                    mentions its current version, and CHANGELOG.md has a line
                    containing both the file path and that version.
  4. Palette drift — brand/colors.md's ```json block is the closed set. Every hex
                    colour in text files under brand/ (excluding brand/archive/
                    and brand/almonaseb/, which has its own palette) must be in
                    that set. Lines carrying an [off-palette] marker are skipped. An
                    8-digit hex (with alpha) is allowed only for a token whose
                    opacity_steps is true. The table in colors.md and its json
                    block must list the same hex values.

Exit code 1 on any failure. Run from the repository root:  python3 scripts/check_standards.py
"""
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PALETTE_FILE = "brand/colors.md"
CHANGELOG = "CHANGELOG.md"
RULE_FILE_EXCLUDE_DIRS = ("brand/archive",)
DRIFT_SCAN_DIRS = ("brand",)
DRIFT_EXCLUDE_DIRS = ("brand/archive", "brand/almonaseb")
DRIFT_EXTENSIONS = (".md", ".svg", ".html", ".htm", ".css", ".json", ".yml", ".yaml", ".txt")
OFF_PALETTE_MARKER = "[off-palette"  # matches [off-palette] and [off-palette: #XXXXXX]
STATUSES = {"draft", "authoritative", "superseded"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
HEX = re.compile(r"#([0-9A-Fa-f]{8}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})(?![0-9A-Za-z])")

failures, warnings = [], []


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def walk(subdirs, exts, exclude):
    for sub in subdirs:
        base = os.path.join(ROOT, sub)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            r = rel(dirpath)
            if any(r == e or r.startswith(e + "/") for e in exclude):
                dirnames[:] = []
                continue
            for f in sorted(filenames):
                if f.lower().endswith(exts):
                    yield os.path.join(dirpath, f)


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def normalise_hex(h):
    h = h.upper()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return h


# ---------------------------------------------------------------- 1–3: rule files
rule_files = [
    p for p in walk((".",), (".md",), RULE_FILE_EXCLUDE_DIRS)
    if rel(p) != CHANGELOG and "/." not in "/" + rel(p)
]
changelog_text = read(os.path.join(ROOT, CHANGELOG)) if os.path.exists(os.path.join(ROOT, CHANGELOG)) else ""
if not changelog_text:
    failures.append(f"{CHANGELOG}: missing")

authoritative_topics = {}
today = dt.date.today()

for path in rule_files:
    r = rel(path)
    text = read(path)
    fm = parse_frontmatter(text)
    if fm is None:
        warnings.append(f"{r}: no frontmatter — treated as DRAFT, not a standard (rule 2)")
        continue
    for key in ("title", "version", "updated", "status"):
        if not fm.get(key):
            failures.append(f"{r}: frontmatter missing `{key}` (rule 2)")
    version, updated, status, topic = fm.get("version", ""), fm.get("updated", ""), fm.get("status", ""), fm.get("topic")
    if version and not SEMVER.match(version):
        failures.append(f"{r}: version `{version}` is not semver X.Y.Z (rule 2)")
    if updated:
        try:
            d = dt.date.fromisoformat(updated)
            if d > today + dt.timedelta(days=1):  # one day of slack for time zones
                failures.append(f"{r}: updated `{updated}` is in the future")
        except ValueError:
            failures.append(f"{r}: updated `{updated}` is not YYYY-MM-DD (rule 2)")
    if status and status not in STATUSES:
        failures.append(f"{r}: status `{status}` not in {sorted(STATUSES)} (rule 2)")
    if status == "authoritative" and topic:
        if topic in authoritative_topics:
            failures.append(f"{r}: topic `{topic}` already owned by {authoritative_topics[topic]} (rule 1)")
        else:
            authoritative_topics[topic] = r
    if status == "authoritative" and not topic:
        warnings.append(f"{r}: authoritative but no `topic` — rule 1 cannot be checked for it")
    if status and status != "draft" and version:
        m = re.search(r"^## Changelog\s*$(.*)", text, re.M | re.S)
        if not m:
            failures.append(f"{r}: no `## Changelog` section (rule 3)")
        elif version not in m.group(1):
            failures.append(f"{r}: `## Changelog` does not mention current version {version} (rule 3)")
        if changelog_text and not any(r in line and version in line for line in changelog_text.splitlines()):
            failures.append(f"{r}: {CHANGELOG} has no line with `{r}` and `{version}` (rule 3)")

# ---------------------------------------------------------------- 4: palette drift
palette_path = os.path.join(ROOT, PALETTE_FILE)
if not os.path.exists(palette_path):
    failures.append(f"{PALETTE_FILE}: missing — no colour authority")
else:
    ptext = read(palette_path)
    m = re.search(r"```json\s*\n(.*?)\n```", ptext, re.S)
    if not m:
        failures.append(f"{PALETTE_FILE}: no ```json palette block")
    else:
        try:
            pal = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            failures.append(f"{PALETTE_FILE}: palette json invalid: {e}")
            pal = {}
        tokens = pal.get("tokens", {})
        allowed = {normalise_hex(t["hex"].lstrip("#")): name for name, t in tokens.items()}
        alpha_ok = {normalise_hex(t["hex"].lstrip("#")) for t in tokens.values() if t.get("opacity_steps") is True}
        if pal.get("version") and pal["version"] != (parse_frontmatter(ptext) or {}).get("version"):
            failures.append(f"{PALETTE_FILE}: json block version {pal['version']} != frontmatter version")

        # table ↔ json agreement
        table_hex = {normalise_hex(h) for h in re.findall(r"^\|\s*`[\w-]+`\s*\|\s*`#([0-9A-Fa-f]{6})`", ptext, re.M)}
        if table_hex and table_hex != set(allowed):
            failures.append(
                f"{PALETTE_FILE}: table hex set {sorted(table_hex)} != json hex set {sorted(allowed)}"
            )

        if allowed:
            for path in walk(DRIFT_SCAN_DIRS, DRIFT_EXTENSIONS, DRIFT_EXCLUDE_DIRS):
                r = rel(path)
                for n, line in enumerate(read(path).splitlines(), 1):
                    if OFF_PALETTE_MARKER in line:
                        continue
                    for h in HEX.findall(line):
                        base, alpha = (h[:6], h[6:]) if len(h) == 8 else (h, "")
                        base = normalise_hex(base)
                        if base not in allowed:
                            failures.append(f"{r}:{n}: #{h} is not in the palette (closed set)")
                        elif alpha and base not in alpha_ok:
                            failures.append(f"{r}:{n}: #{h} — opacity steps are not allowed for {allowed[base]}")

# ---------------------------------------------------------------- report
for w in warnings:
    print(f"WARN  {w}")
for f in failures:
    print(f"FAIL  {f}")
print(f"\n{len(failures)} failure(s), {len(warnings)} warning(s); "
      f"authoritative topics: {', '.join(f'{t}={p}' for t, p in sorted(authoritative_topics.items())) or 'none'}")
sys.exit(1 if failures else 0)
