#!/usr/bin/env python3
"""Check inline Markdown links and media targets in the guides."""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
TARGET = re.compile(r"\]\(\s*(?:<([^>]+)>|([^\s)]+))")
PLACEHOLDER = re.compile(r"\{[A-Za-z_]\w*\}")


def errors(path):
    fence = None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token, rest = marker.groups()
            if fence is None:
                fence = token
                continue
            if token.startswith(fence) and not rest.strip():
                fence = None
                continue
        if fence:
            continue
        for angle, bare in TARGET.findall(line):
            target = angle or bare
            if PLACEHOLDER.search(unquote(target)):
                yield number, f"unresolved placeholder: {target}"
                continue
            parts = urlsplit(target)
            if not (parts.scheme or parts.netloc) and parts.path:
                local = unquote(parts.path)
                candidate = ROOT / local.lstrip("/") if local.startswith("/") else path.parent / local
                if not candidate.exists():
                    yield number, f"missing local target: {target}"


def main():
    guides = sorted((ROOT / "guides").rglob("*.md"))
    failures = 0
    for path in guides:
        for line, error in errors(path):
            failures += 1
            print(f"{path.relative_to(ROOT)}:{line}: {error}")
    print(f"Checked {len(guides)} Markdown guides: {failures} link errors")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
