#!/usr/bin/env python3
"""Reachability check over the built site.

Two failure modes this catches, both of which have already happened here:

  orphan  — a file ships but nothing links to it, so it exists at a URL
            nobody can find (the measurement protocol sat like this for
            weeks; the generated schematics landed the same way)
  broken  — a link points at something the build did not produce

Run against `_site` after a build:
    python3 tools/linkcheck.py _site
"""
import os
import pathlib
import re
import sys
from collections import defaultdict

HREF = re.compile(r'(?:href|src)="([^"]+)"')
BASEURL = "/refrhus"

# Files that are meant to exist without an inbound link.
EXEMPT = {
    "index.html",          # the front door
    "assets/css/style.css",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "feed.xml",
}


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")

    shipped = set()
    for dirpath, _, names in os.walk(root):
        for n in names:
            shipped.add(str(pathlib.Path(dirpath, n).relative_to(root)))

    # Every URL any page points at, and which page pointed at it.
    refs = defaultdict(set)
    for rel in sorted(shipped):
        if not rel.endswith((".html", ".css")):
            continue
        text = (root / rel).read_text(encoding="utf-8", errors="replace")
        for raw in HREF.findall(text):
            u = raw.split("#")[0].split("?")[0]
            if not u or u.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            if u.startswith(BASEURL + "/"):
                u = u[len(BASEURL) + 1:]
            elif u.startswith("/"):
                u = u[1:]
            else:
                u = os.path.normpath(os.path.join(os.path.dirname(rel), u))
            refs[u.rstrip("/") or "index.html"].add(rel)

    # A pretty URL `foo/` is served by `foo/index.html`.
    def resolve(u):
        for cand in (u, f"{u}/index.html", f"{u}.html"):
            if cand in shipped:
                return cand
        return None

    linked = set()
    broken = []
    for u, sources in sorted(refs.items()):
        hit = resolve(u)
        if hit:
            linked.add(hit)
        else:
            broken.append((u, sorted(sources)))

    orphans = []
    for rel in sorted(shipped):
        if rel in EXEMPT or rel in linked:
            continue
        # Assets a page pulls in are reached via their own directory index.
        if rel.endswith((".scss", ".map")):
            continue
        orphans.append(rel)

    print(f"{len(shipped)} files shipped, {len(linked)} reachable\n")

    if broken:
        print(f"BROKEN LINKS ({len(broken)})")
        for u, sources in broken:
            print(f"  {u}")
            for s in sources[:4]:
                print(f"      from {s}")
        print()

    if orphans:
        print(f"ORPHANS — shipped but nothing links to them ({len(orphans)})")
        for o in orphans:
            print(f"  {o}")
        print()

    if not broken and not orphans:
        print("No broken links, no orphans.")
    return 1 if (broken or orphans) else 0


if __name__ == "__main__":
    sys.exit(main())
