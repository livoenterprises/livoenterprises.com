#!/usr/bin/env python3
"""
build_content.py - turns the Markdown files in content/ into the site's HTML pages.

Run from the repository root:   python3 tools/build_content.py
(GitHub Actions runs it after every change to content/; see
 .github/workflows/build-content.yml. It needs the "markdown" package:
 pip install markdown)

Each content/*.md file starts with a header between two "---" lines:

    ---
    title: Privacy Policy
    description: One sentence for search engines and link previews.
    version: 2
    updated: 2026-10-07
    web: privacy.html          # where the page is written (omit = no web page)
    nav: Support               # which top-nav item is "current" (optional)
    style: policy              # extra CSS class on the page body (optional)
    app: privacy               # the screen in Livo that shows this file (informational)
    lede: One sentence shown large under the title. (optional)
    ---

The body is the Livo Markdown subset (content/README.md): ## and ###
headings, paragraphs, **bold**, *italic*, [links](https://...), - bullets,
1. numbered lists. Nothing else, so the app's own renderer can show the
same file.

Files in content/guide/ are the user guide. Each becomes guide/<name>.html
and guide/index.html lists them in "order:" order.

Generated pages carry a comment naming the source file and version so a
page edited by hand (instead of through its .md) is easy to spot.
"""

import os
import re
import sys
import html
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("The 'markdown' package is missing. Run: pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TEMPLATE = ROOT / "tools" / "page_template.html"
SITE = "https://livoenterprises.com"
NAV_ITEMS = [("LivoCapsule", "/livocapsule.html"), ("About", "/about.html"),
             ("Notes", "/blog/"), ("Support", "/support.html")]
ALLOWED_KEYS = {"title", "description", "version", "updated", "web", "nav",
                "style", "app", "lede", "order"}


def read_front_matter(text, path):
    if not text.startswith("---"):
        sys.exit(f"{path}: no header (the file must start with ---)")
    rest = text[3:].lstrip("\n")
    parts = rest.split("\n---", 1)
    if len(parts) < 2:
        sys.exit(f"{path}: header not closed (second --- missing)")
    head = parts[0]
    body = parts[1].lstrip("\n")
    meta = {}
    for line in head.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            sys.exit(f"{path}: header line without a colon: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in ALLOWED_KEYS:
            sys.exit(f"{path}: unknown header key '{key}' (allowed: {sorted(ALLOWED_KEYS)})")
        meta[key] = value.strip()
    for required in ("title", "version", "updated"):
        if required not in meta:
            sys.exit(f"{path}: header is missing '{required}'")
    return meta, body


FORBIDDEN = [
    (re.compile(r"^\s*#(?!#)", re.M), "a single-# heading (the title comes from the header; use ##)"),
    (re.compile(r"^\s*\|", re.M), "a table"),
    (re.compile(r"^\s*<[a-zA-Z]", re.M), "raw HTML"),
    (re.compile(r"^```", re.M), "a code block"),
    (re.compile(r"!\[", re.M), "an image"),
]


def check_subset(body, path):
    for pattern, what in FORBIDDEN:
        if pattern.search(body):
            sys.exit(f"{path}: uses {what}, which is outside the Livo Markdown subset")


def render_body(body):
    return markdown.markdown(body, output_format="html5", extensions=["smarty"])


def pretty_date(iso):
    try:
        y, m, d = (int(x) for x in iso.split("-"))
        months = ["January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]
        return f"{d} {months[m - 1]} {y}"
    except Exception:
        return iso


def nav_html(current):
    out = []
    for label, href in NAV_ITEMS:
        cur = ' aria-current="page"' if label == current else ""
        out.append(f'      <a href="{href}"{cur}>{label}</a>')
    return "\n".join(out)


def build_page(meta, body_html, web_path, source_name, extra_top=""):
    template = TEMPLATE.read_text(encoding="utf-8")
    title = html.escape(meta["title"], quote=False)
    description = html.escape(meta.get("description", ""), quote=False)
    lede = meta.get("lede", "")
    lede_html = f'    <p class="lede">{html.escape(lede, quote=False)}</p>\n' if lede else ""
    updated = ('    <p class="updated">Version ' + html.escape(meta["version"]) +
               " &middot; Last updated " + pretty_date(meta["updated"]) + "</p>\n")
    style = meta.get("style", "")
    wrap_class = "wrap" + (f" {style}" if style else "")
    page = (template
            .replace("{{title}}", title)
            .replace("{{description}}", description)
            .replace("{{canonical}}", f"{SITE}/{web_path}")
            .replace("{{nav}}", nav_html(meta.get("nav", "")))
            .replace("{{wrap_class}}", wrap_class)
            .replace("{{h1}}", title)
            .replace("{{updated}}", updated)
            .replace("{{lede}}", lede_html)
            .replace("{{extra_top}}", extra_top)
            .replace("{{body}}", body_html)
            .replace("{{source}}", f"content/{source_name} v{meta['version']} ({meta['updated']})"))
    return page


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        print(f"  unchanged  {path.relative_to(ROOT)}")
        return
    path.write_text(text, encoding="utf-8")
    print(f"  wrote      {path.relative_to(ROOT)}")


def main():
    if not CONTENT.is_dir():
        sys.exit("No content/ folder next to tools/")
    print("Building pages from content/")
    pages = sorted(p for p in CONTENT.glob("*.md") if p.name != "README.md")
    for path in pages:
        meta, body = read_front_matter(path.read_text(encoding="utf-8"), path)
        check_subset(body, path)
        web = meta.get("web", "")
        if not web:
            print(f"  app only   content/{path.name} (no web: line)")
            continue
        page = build_page(meta, render_body(body), web, path.name)
        write(ROOT / web, page)

    guide = sorted(p for p in (CONTENT / "guide").glob("*.md") if p.name != "index.md")
    entries = []
    for path in guide:
        meta, body = read_front_matter(path.read_text(encoding="utf-8"), path)
        check_subset(body, path)
        web = meta.get("web") or f"guide/{path.stem}.html"
        meta.setdefault("nav", "Support")
        back = '    <p class="small"><a href="/guide/">&larr; Livo guide</a></p>\n'
        page = build_page(meta, render_body(body), web, f"guide/{path.name}", extra_top=back)
        write(ROOT / web, page)
        entries.append((int(meta.get("order", "999")), meta, web))
    if entries:
        entries.sort(key=lambda e: (e[0], e[1]["title"]))
        items = []
        for _, meta, web in entries:
            items.append(f'<li><a href="/{web}">{html.escape(meta["title"], quote=False)}</a>'
                         f'<span class="sum">{html.escape(meta.get("description", ""), quote=False)}</span></li>')
        index_meta = {"title": "Livo guide", "version": str(len(entries)),
                      "updated": max(e[1]["updated"] for e in entries),
                      "description": "How to use Livo, one topic at a time. The same pages are in the app under Organize › Guide.",
                      "nav": "Support",
                      "lede": "How to use Livo, one topic at a time. The same pages are inside the app."}
        index_body = '<ul class="posts">\n' + "\n".join(items) + "\n</ul>\n"
        page = build_page(index_meta, index_body, "guide/index.html", "guide/")
        page = page.replace("<p class=\"updated\">Version " + str(len(entries)),
                            "<p class=\"updated\">" + str(len(entries)) + " topics")
        write(ROOT / "guide" / "index.html", page)
    print("Done.")


if __name__ == "__main__":
    main()
