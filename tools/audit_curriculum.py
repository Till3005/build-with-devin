#!/usr/bin/env python3
"""Audit build-with-devin curriculum integrity.

Hard failures are integrity problems that make the curriculum unreliable:
missing translations, broken README guide links, duplicate guide numbers,
missing core sections, or a coverage matrix that references files that do
not exist. Coverage gaps are reported but do not fail the build.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("zh", "ja", "pt")
COVERAGE = ROOT / "ops" / "curriculum" / "coverage.json"
VALID_STATUSES = {"covered", "partial", "gap", "watch"}

REQUIRED_MARKERS = {
    "goal": "**Goal:**",
    "level": "**Level:**",
    "source_header": "**Source",
    "verification": "Verify",
    "pitfalls": "Pitfall",
    "knowledge_check": "Knowledge check",
    "sources_section": "## Sources",
}


def guide_links(md_text):
    return sorted(set(re.findall(r"guides/[a-z0-9/-]+\.md", md_text)))


def english_guide_number(text):
    first = text.splitlines()[0] if text.splitlines() else ""
    match = re.match(r"# Guide (\d+)\b", first)
    return int(match.group(1)) if match else None


def audit_guides():
    errors = []
    warnings = []
    guides = sorted((ROOT / "guides").glob("*.md"))
    numbers = {}

    for path in guides:
        text = path.read_text()
        rel = path.relative_to(ROOT)
        for name, marker in REQUIRED_MARKERS.items():
            if marker not in text:
                errors.append(f"{rel}: missing {name} marker {marker!r}")

        number = english_guide_number(text)
        if number is not None:
            numbers.setdefault(number, []).append(str(rel))

        for lang in LANGS:
            translated = ROOT / "guides" / lang / path.name
            if not translated.exists():
                errors.append(f"missing translation: {translated.relative_to(ROOT)}")

    for number, paths in sorted(numbers.items()):
        if len(paths) > 1:
            errors.append(f"duplicate guide number {number}: {', '.join(paths)}")

    readme = (ROOT / "README.md").read_text()
    for link in guide_links(readme):
        if link.startswith("guides/") and not (ROOT / link).exists():
            errors.append(f"README.md links missing file: {link}")

    for lang in LANGS:
        lang_readme = ROOT / f"README.{lang}.md"
        if not lang_readme.exists():
            errors.append(f"missing README.{lang}.md")
            continue
        for link in guide_links(lang_readme.read_text()):
            if link.startswith(f"guides/{lang}/") and not (ROOT / link).exists():
                errors.append(f"README.{lang}.md links missing file: {link}")

    return errors, warnings, len(guides)


def audit_coverage():
    errors = []
    rows = []
    if not COVERAGE.exists():
        return [f"missing coverage matrix: {COVERAGE.relative_to(ROOT)}"], rows

    try:
        data = json.loads(COVERAGE.read_text())
    except json.JSONDecodeError as exc:
        return [f"coverage matrix is invalid JSON: {exc}"], rows

    rows = data.get("areas")
    if not isinstance(rows, list):
        return ["coverage matrix must contain an 'areas' list"], []

    seen = set()
    for index, row in enumerate(rows, start=1):
        label = row.get("id", f"row {index}")
        if label in seen:
            errors.append(f"coverage matrix duplicate id: {label}")
        seen.add(label)

        for field in ("id", "area", "status", "priority"):
            if field not in row:
                errors.append(f"coverage matrix {label}: missing {field}")
        if row.get("status") not in VALID_STATUSES:
            errors.append(f"coverage matrix {label}: invalid status {row.get('status')!r}")
        if row.get("priority") not in {"P0", "P1", "P2"}:
            errors.append(f"coverage matrix {label}: invalid priority {row.get('priority')!r}")
        if not row.get("official_sources"):
            errors.append(f"coverage matrix {label}: missing official_sources")

        for guide in row.get("guides", []):
            if not (ROOT / guide).exists():
                errors.append(f"coverage matrix {label}: missing guide file {guide}")

    return errors, rows


def main():
    errors, warnings, guide_count = audit_guides()
    coverage_errors, rows = audit_coverage()
    errors.extend(coverage_errors)

    counts = {status: 0 for status in sorted(VALID_STATUSES)}
    for row in rows:
        counts[row.get("status")] = counts.get(row.get("status"), 0) + 1

    print(f"guides audited: {guide_count}")
    if rows:
        print("coverage: " + ", ".join(f"{k}={counts[k]}" for k in sorted(counts)))
        gaps = [row["id"] for row in rows if row.get("status") in {"gap", "partial"}]
        print("open coverage gaps/partials: " + (", ".join(gaps) if gaps else "none"))

    for warning in warnings:
        print("WARN: " + warning)
    if errors:
        for error in errors:
            print("ERROR: " + error)
        return 1
    print("curriculum audit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
