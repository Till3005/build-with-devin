#!/usr/bin/env python3
"""Single-source-of-truth sync for build-with-devin.

README.md (English) is the source of truth. Counts guides/ entries, rewrites
the stats line in every README.<lang>.md, and checks guide-link parity
(every guide linked in the English README must appear in each translated
README; README.zh links guides/zh/* paths).
Usage: python3 tools/sync.py [--write]
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LANGS = ['zh', 'de', 'es', 'ja', 'pt']

def guide_links(md):
    return sorted(set(re.findall(r'guides/[a-z0-9/-]+\.md', md)))

def main():
    en = (ROOT / 'README.md').read_text()
    guides = [p for p in (ROOT / 'guides').glob('*.md')]
    n = len(guides)
    print(f'guide files: {n}')

    drift = []
    # stats line in each README — the first bolded count inside <sub>
    for f in ['README.md'] + [f'README.{l}.md' for l in LANGS]:
        p = ROOT / f
        if not p.exists():
            drift.append(f'{f}: missing'); continue
        t = p.read_text()
        m = re.search(r'<sub>\*\*(\d+)\*\*', t)
        if not m:
            drift.append(f'{f}: no stats line'); continue
        if int(m.group(1)) != n:
            drift.append(f'{f}: stats say {m.group(1)} guides, want {n}')
            if '--write' in sys.argv:
                p.write_text(t[:m.start(1)] + str(n) + t[m.end(1):])

    # link parity vs en guide links
    en_links = guide_links(en)
    for lang in LANGS:
        t = (ROOT / f'README.{lang}.md').read_text()
        lang_links = set(guide_links(t))
        for g in en_links:
            if lang == 'zh':
                want = 'guides/zh/' + g.split('/')[-1]
                if want not in lang_links:
                    drift.append(f'README.zh.md: missing {want}')
            elif g not in lang_links:
                drift.append(f'README.{lang}.md: missing {g}')

    # zh guide files exist for every zh-linked path
    for g in guide_links((ROOT / 'README.zh.md').read_text()):
        if g.startswith('guides/zh/') and not (ROOT / g).exists():
            drift.append(f'missing file: {g}')

    if drift:
        print('\n'.join('DRIFT: ' + d for d in drift)); sys.exit(1)
    print('in sync')

if __name__ == '__main__':
    main()
