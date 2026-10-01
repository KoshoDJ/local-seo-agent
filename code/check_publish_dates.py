#!/usr/bin/env python3
"""The stamp on the page and the row in the registry must agree.

The page's own `publishDate` is what makes it 404 before its date.
`SCHEDULE` in lib/publishing.ts is what keeps it out of the sitemap, the
listings and every inbound link. If those two ever drift, a page hides itself
while its links stay live, or the reverse. This catches that.
"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "website"
schedule_src = (root / "lib" / "publishing.ts").read_text()
block = re.search(r"SCHEDULE: Record<string, string> = \{(.*?)\};", schedule_src, re.S).group(1)
STAMP = r"\d{4}-\d{2}-\d{2}(?:T[\d:]+Z)?"  # a date, or a full timestamp for an exact-moment publish
registry = dict(re.findall(r'"([^"]+)":\s*"(%s)"' % STAMP, block))

stamps = {}
for page in sorted((root / "app").rglob("page.tsx")):
    m = re.search(r'^const publishDate = "(%s)";' % STAMP, page.read_text(), re.M)
    if m:
        route = "/" + str(page.parent.relative_to(root / "app"))
        stamps[route] = m.group(1)

problems = []
for route, date in stamps.items():
    if registry.get(route) != date:
        problems.append(f"{route}: page says {date}, registry says {registry.get(route) or 'nothing'}")
for route, date in registry.items():
    if route not in stamps:
        problems.append(f"{route}: in the registry ({date}) but the page carries no stamp")

if problems:
    print("FAIL - the schedule and the pages disagree:")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print(f"PASS - {len(stamps)} scheduled page(s), every stamp matches the registry")
for route, date in sorted(stamps.items()):
    print(f"  {route} -> {date}")
