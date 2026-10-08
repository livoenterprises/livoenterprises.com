#!/usr/bin/env python3
"""
build_content.py v2 - turns the Markdown files in content/ into the site's pages.

Run from the repository root:   python3 tools/build_content.py
(GitHub Actions runs it after every change to content/ or tools/; see
 .github/workflows/build-content.yml. LivoContent.sh publish also runs it
 on Ken's Mac when the "markdown" package is installed:  pip3 install markdown)

What it builds
  content/privacy.md, support.md, about-livo.md  -> the page named by "web:"
  content/guide/<topic>.md                        -> guide/<topic>.html, guide/index.html
  content/blog/<slug>.md                          -> blog/<slug>.html            (v2)
  content/blog/images/*                           -> blog/images/*  (copied)      (v2)
  blog/index.html   the list between <!-- POSTS:begin --> and <!-- POSTS:end -->  (v2)
  index.html        the newest notes between the same two markers                (v2)
  feed.xml          written whole from the listed posts                          (v2)
  sitemap.xml       written whole: the fixed pages + everything generated        (v2)

A page file (content/*.md, guide/) starts with a header between two "---" lines:

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

Its body is the Livo Markdown subset (content/README.md): ## and ###
headings, paragraphs, **bold**, *italic*, [links](https://...), - bullets,
1. numbered lists. Nothing else, so the app's own renderer can show the
same file.

A note (content/blog/<slug>.md) is web-only; the app never shows it. Header:

    ---
    title: The thread I didn't see until I wrote it down
    description: One sentence: the summary under the title in lists and the feed.
    date: 2026-09-18           # published; the slug is the file name
    updated: 2026-09-18        # optional; defaults to date
    topics: Own your data, Technology that serves you
    author: Ken Jones          # optional; this is the default
    listed: yes                # no = the page exists but is not in Notes, the feed or the front page
    front: yes                 # no = in Notes and the feed, not on the front page
    draft: no                  # yes = built with noindex, never listed; for looking at it before it goes out
    ---

Its body may also use > quotes and images: ![caption](images/photo.jpg),
with the file in content/blog/images/. The builder warns (does not stop)
when an image is wider than 1600 px or larger than 500 KB.

Generated pages carry a comment naming the source file and version so a
page edited by hand (instead of through its .md) is easy to spot.
"""

import os
import re
import sys
import html
import shutil
import struct
import subprocess
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("The 'markdown' package is missing. Run: pip3 install markdown")

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TEMPLATE = ROOT / "tools" / "page_template.html"
POST_TEMPLATE = ROOT / "tools" / "post_template.html"
SITE = "https://livoenterprises.com"
NAV_ITEMS = [("LivoCapsule", "/livocapsule.html"), ("About", "/about.html"),
             ("Notes", "/blog/"), ("Support", "/support.html")]
ALLOWED_KEYS = {"title", "description", "version", "updated", "web", "nav",
                "style", "app", "lede", "order", "screen"}
POST_KEYS = {"title", "description", "date", "updated", "topics", "author",
             "listed", "front", "draft", "web"}
FRONT_PAGE_NOTES = 3          # how many notes the front page lists
IMAGE_MAX_WIDTH = 1600        # px; wider is a warning
IMAGE_MAX_BYTES = 500 * 1024  # bytes; larger is a warning
IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
# Pages that are not generated but belong in the sitemap, with the file
# whose last commit date is their lastmod.
FIXED_PAGES = [("", "index.html"), ("about.html", "about.html"),
               ("livocapsule.html", "livocapsule.html"), ("blog/", "blog/index.html")]
MARK_BEGIN = "<!-- POSTS:begin -->"
MARK_END = "<!-- POSTS:end -->"

warnings = []


def warn(msg):
    warnings.append(msg)
    print(f"  WARNING    {msg}")


def read_front_matter(text, path, allowed, required):
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
        if key not in allowed:
            sys.exit(f"{path}: unknown header key '{key}' (allowed: {sorted(allowed)})")
        meta[key] = value.strip()
    for key in required:
        if key not in meta:
            sys.exit(f"{path}: header is missing '{key}'")
    return meta, body


FORBIDDEN = [
    (re.compile(r"^\s*#(?!#)", re.M), "a single-# heading (the title comes from the header; use ##)"),
    (re.compile(r"^\s*\|", re.M), "a table"),
    (re.compile(r"^\s*<[a-zA-Z]", re.M), "raw HTML"),
    (re.compile(r"^```", re.M), "a code block"),
    (re.compile(r"!\[", re.M), "an image"),
    (re.compile(r"^\s*>", re.M), "a quote"),
]
FORBIDDEN_IN_NOTES = [
    (re.compile(r"^\s*#(?!#)", re.M), "a single-# heading (the title comes from the header; use ##)"),
    (re.compile(r"^\s*\|", re.M), "a table"),
    (re.compile(r"^\s*<[a-zA-Z]", re.M), "raw HTML"),
    (re.compile(r"^```", re.M), "a code block"),
]


def check_subset(body, path, rules=FORBIDDEN):
    for pattern, what in rules:
        if pattern.search(body):
            sys.exit(f"{path}: uses {what}, which is outside the Livo Markdown subset")


APP_LINK = re.compile(r'<a href="livo://[^"]*">(.*?)</a>')
IMG = re.compile(r'<p>\s*<img alt="([^"]*)" src="([^"]+)"\s*/?>\s*</p>')


def render_body(body):
    html_out = markdown.markdown(body, output_format="html5", extensions=["smarty"])
    # A livo:// link opens a screen inside the app. On the web it is the
    # path in words, marked "in Livo"; it never leaves the page.
    return APP_LINK.sub(r'<span class="app-link" title="Opens this screen in Livo">\1</span>', html_out)


def render_note_body(body, path):
    html_out = render_body(body)

    def figure(m):
        alt, src = m.group(1), m.group(2)
        if src.startswith("images/"):
            if not (CONTENT / "blog" / src).is_file():
                sys.exit(f"{path}: image not found: content/blog/{src}")
            src = "/blog/" + src
        elif not src.startswith(("/", "http://", "https://")):
            sys.exit(f"{path}: an image is images/<file> (in content/blog/images/) or a full address: {src}")
        cap = f"<figcaption>{alt}</figcaption>" if alt else ""
        return f'<figure><img src="{src}" alt="{html.escape(alt, quote=True)}" loading="lazy">{cap}</figure>'
    return IMG.sub(figure, html_out)


MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def ymd(iso, path="?"):
    try:
        y, m, d = (int(x) for x in iso.split("-"))
        return y, m, d
    except Exception:
        sys.exit(f"{path}: a date must be YYYY-MM-DD, not '{iso}'")


def pretty_date(iso):            # pages: 7 October 2026
    try:
        y, m, d = ymd(iso)
        return f"{d} {MONTHS[m - 1]} {y}"
    except SystemExit:
        return iso


def post_date(iso, path):        # notes: September 18, 2026 (as the first notes had it)
    y, m, d = ymd(iso, path)
    return f"{MONTHS[m - 1]} {d}, {y}"


def rfc822(iso, path):
    import datetime
    y, m, d = ymd(iso, path)
    dt = datetime.date(y, m, d)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return f"{days[dt.weekday()]}, {d:02d} {MONTHS[m - 1][:3]} {y} 12:00:00 GMT"


def nav_html(current):
    out = []
    for label, href in NAV_ITEMS:
        cur = ' aria-current="page"' if label == current else ""
        out.append(f'      <a href="{href}"{cur}>{label}</a>')
    return "\n".join(out)


def smart(s):
    """Typographer's quotes and dashes in a header value (title, description, lede),
    the same as the smarty extension gives the body; returns plain characters."""
    out = markdown.markdown(s, extensions=["smarty"])
    out = re.sub(r"^<p>|</p>$", "", out.strip())
    return html.unescape(out)


def yes(value, default="yes"):
    return (value or default).strip().lower() in ("yes", "y", "true", "1")


def build_page(meta, body_html, web_path, source_name, extra_top=""):
    template = TEMPLATE.read_text(encoding="utf-8")
    title = html.escape(smart(meta["title"]), quote=False)
    description = html.escape(smart(meta.get("description", "")), quote=False)
    lede = smart(meta.get("lede", ""))
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


def build_post(meta, body_html, web_path, source_name):
    template = POST_TEMPLATE.read_text(encoding="utf-8")
    title = html.escape(smart(meta["title"]), quote=False)
    title_json = smart(meta["title"]).replace("\\", "\\\\").replace('"', '\\"')
    description = html.escape(smart(meta["description"]), quote=False)
    topics = ", ".join(t.strip() for t in meta.get("topics", "").split(",") if t.strip())
    topics_html = (f'    <p class="topics">Filed under: {html.escape(topics, quote=False)}</p>\n'
                   if topics else "")
    author = meta.get("author", "Ken Jones")
    noindex = ('  <meta name="robots" content="noindex">\n' if yes(meta.get("draft"), "no") else "")
    page = (template
            .replace("{{title}}", title)
            .replace("{{title_json}}", title_json)
            .replace("{{description}}", description)
            .replace("{{canonical}}", f"{SITE}/{web_path}")
            .replace("{{noindex}}", noindex)
            .replace("{{nav}}", nav_html("Notes"))
            .replace("{{date_iso}}", meta["date"])
            .replace("{{date_pretty}}", post_date(meta["date"], source_name))
            .replace("{{author}}", html.escape(author, quote=False))
            .replace("{{author_json}}", author.replace('"', '\\"'))
            .replace("{{body}}", body_html)
            .replace("{{topics}}", topics_html)
            .replace("{{source}}", f"content/{source_name} ({meta['updated']})"))
    return page


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        print(f"  unchanged  {path.relative_to(ROOT)}")
        return
    path.write_text(text, encoding="utf-8")
    print(f"  wrote      {path.relative_to(ROOT)}")


def replace_block(path, inner, what):
    """Replace what sits between MARK_BEGIN and MARK_END in a hand-written page."""
    if not path.exists():
        warn(f"{path.relative_to(ROOT)} is missing; {what} not written")
        return
    text = path.read_text(encoding="utf-8")
    a = text.find(MARK_BEGIN)
    b = text.find(MARK_END)
    if a < 0 or b < 0 or b < a:
        warn(f"{path.relative_to(ROOT)} has no {MARK_BEGIN} ... {MARK_END} pair; {what} not written")
        return
    new = text[:a + len(MARK_BEGIN)] + "\n" + inner + text[b:]
    write(path, new)


def image_size(path):
    """(width, height) for PNG, JPEG, GIF and WebP from the file's header; None otherwise."""
    try:
        with open(path, "rb") as f:
            head = f.read(32)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                return struct.unpack(">II", head[16:24])
            if head[:6] in (b"GIF87a", b"GIF89a"):
                return struct.unpack("<HH", head[6:10])
            if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
                if head[12:16] == b"VP8 ":
                    return struct.unpack("<HH", head[26:30])[0] & 0x3FFF, struct.unpack("<HH", head[26:30])[1] & 0x3FFF
                if head[12:16] == b"VP8L":
                    b0, b1, b2, b3 = head[21:25]
                    return 1 + (((b1 & 0x3F) << 8) | b0), 1 + (((b3 & 0xF) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
                if head[12:16] == b"VP8X":
                    return 1 + int.from_bytes(head[24:27], "little"), 1 + int.from_bytes(head[27:30], "little")
                return None
            if head[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    marker = f.read(2)
                    if len(marker) < 2 or marker[0] != 0xFF:
                        return None
                    if marker[1] in (0xC0, 0xC1, 0xC2):
                        f.read(3)
                        h, w = struct.unpack(">HH", f.read(4))
                        return w, h
                    seg = struct.unpack(">H", f.read(2))[0]
                    f.seek(seg - 2, 1)
    except Exception:
        return None
    return None


def copy_images():
    src = CONTENT / "blog" / "images"
    if not src.is_dir():
        return
    dst = ROOT / "blog" / "images"
    dst.mkdir(parents=True, exist_ok=True)
    for path in sorted(src.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() not in IMAGE_TYPES:
            warn(f"content/blog/images/{path.name} is not an image type the site uses; copied anyway")
        size = path.stat().st_size
        if size > IMAGE_MAX_BYTES:
            warn(f"content/blog/images/{path.name} is {size // 1024} KB (over {IMAGE_MAX_BYTES // 1024} KB); shrink it for readers on phones")
        dims = image_size(path)
        if dims and dims[0] > IMAGE_MAX_WIDTH:
            warn(f"content/blog/images/{path.name} is {dims[0]} px wide (over {IMAGE_MAX_WIDTH}); resize it")
        target = dst / path.name
        if target.exists() and target.read_bytes() == path.read_bytes():
            print(f"  unchanged  blog/images/{path.name}")
        else:
            shutil.copyfile(path, target)
            print(f"  copied     blog/images/{path.name}")


def git_date(rel):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT,
                             capture_output=True, text=True, timeout=20)
        d = out.stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            return d
    except Exception:
        pass
    import datetime
    return datetime.date.today().isoformat()


def post_li(meta, web):
    return (f'      <li><time datetime="{meta["date"]}">{post_date(meta["date"], web)}</time>'
            f'<a href="/{web}">{html.escape(smart(meta["title"]), quote=False)}</a>'
            f'<span class="sum">{html.escape(smart(meta["description"]), quote=False)}</span></li>')


def main():
    if not CONTENT.is_dir():
        sys.exit("No content/ folder next to tools/")
    print("Building pages from content/")
    sitemap = []   # (url path, lastmod)

    # --- the pages ---------------------------------------------------
    pages = sorted(p for p in CONTENT.glob("*.md") if p.name != "README.md")
    for path in pages:
        meta, body = read_front_matter(path.read_text(encoding="utf-8"), path, ALLOWED_KEYS,
                                       ("title", "version", "updated"))
        check_subset(body, path)
        web = meta.get("web", "")
        if not web:
            print(f"  app only   content/{path.name} (no web: line)")
            continue
        page = build_page(meta, render_body(body), web, path.name)
        write(ROOT / web, page)
        sitemap.append((web, meta["updated"]))

    # --- the guide ---------------------------------------------------
    guide = sorted(p for p in (CONTENT / "guide").glob("*.md") if p.name != "index.md")
    entries = []
    for path in guide:
        meta, body = read_front_matter(path.read_text(encoding="utf-8"), path, ALLOWED_KEYS,
                                       ("title", "version", "updated"))
        check_subset(body, path)
        web = meta.get("web") or f"guide/{path.stem}.html"
        meta.setdefault("nav", "Support")
        back = '    <p class="small"><a href="/guide/">&larr; Livo guide</a></p>\n'
        page = build_page(meta, render_body(body), web, f"guide/{path.name}", extra_top=back)
        write(ROOT / web, page)
        entries.append((int(meta.get("order", "999")), meta, web))
        sitemap.append((web, meta["updated"]))
    if entries:
        entries.sort(key=lambda e: (e[0], e[1]["title"]))
        items = []
        for _, meta, web in entries:
            items.append(f'<li><a href="/{web}">{html.escape(smart(meta["title"]), quote=False)}</a>'
                         f'<span class="sum">{html.escape(smart(meta.get("description", "")), quote=False)}</span></li>')
        newest = max(e[1]["updated"] for e in entries)
        index_meta = {"title": "Livo guide", "version": str(len(entries)),
                      "updated": newest,
                      "description": "How to use Livo, one topic at a time. The same pages are in the app under Organize › Guide.",
                      "nav": "Support",
                      "lede": "How to use Livo, one topic at a time. The same pages are inside the app."}
        index_body = '<ul class="posts">\n' + "\n".join(items) + "\n</ul>\n"
        page = build_page(index_meta, index_body, "guide/index.html", "guide/")
        page = page.replace("<p class=\"updated\">Version " + str(len(entries)),
                            "<p class=\"updated\">" + str(len(entries)) + " topics")
        write(ROOT / "guide" / "index.html", page)
        sitemap.append(("guide/", newest))

    # --- the notes (blog) --------------------------------------------
    posts = []
    blog_dir = CONTENT / "blog"
    if blog_dir.is_dir():
        copy_images()
        for path in sorted(blog_dir.glob("*.md")):
            if path.name == "README.md":
                continue
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", path.stem):
                sys.exit(f"{path}: a note's file name is its address: lower-case letters, digits and hyphens only")
            meta, body = read_front_matter(path.read_text(encoding="utf-8"), path, POST_KEYS,
                                           ("title", "description", "date"))
            meta.setdefault("updated", meta["date"])
            ymd(meta["date"], path); ymd(meta["updated"], path)
            check_subset(body, path, FORBIDDEN_IN_NOTES)
            web = meta.get("web") or f"blog/{path.stem}.html"
            draft = yes(meta.get("draft"), "no")
            listed = yes(meta.get("listed"), "yes") and not draft
            front = yes(meta.get("front"), "yes") and listed
            page = build_post(meta, render_note_body(body, path), web, f"blog/{path.name}")
            write(ROOT / web, page)
            state = "draft (noindex)" if draft else ("listed" if listed else "unlisted")
            print(f"             {web}: {state}" + ("" if front or not listed else ", not on the front page"))
            posts.append((meta, web, listed, front, draft))
            if not draft:
                sitemap.append((web, meta["updated"]))

        posts.sort(key=lambda p: (p[0]["date"], p[0]["title"]), reverse=True)
        listed_posts = [p for p in posts if p[2]]
        front_posts = [p for p in posts if p[3]][:FRONT_PAGE_NOTES]

        inner = "\n".join(post_li(m, w) for m, w, *_ in listed_posts) + "\n"
        replace_block(ROOT / "blog" / "index.html", inner, "the list of notes")
        inner = "\n".join(post_li(m, w) for m, w, *_ in front_posts) + "\n"
        replace_block(ROOT / "index.html", inner, "the front page's notes")

        items = []
        for meta, web, *_ in listed_posts:
            items.append(
                "  <item>\n"
                f"    <title>{html.escape(smart(meta['title']), quote=False)}</title>\n"
                f"    <link>{SITE}/{web}</link>\n"
                f"    <guid>{SITE}/{web}</guid>\n"
                f"    <pubDate>{rfc822(meta['date'], web)}</pubDate>\n"
                f"    <description>{html.escape(smart(meta['description']), quote=False)}</description>\n"
                "  </item>")
        feed = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
                "<channel>\n"
                "  <title>Livo Enterprises — Notes</title>\n"
                f"  <link>{SITE}/blog/</link>\n"
                f'  <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n'
                "  <description>Notes on owning your data, technology that works for people, and building software with AI.</description>\n"
                "  <language>en-us</language>\n"
                + "\n".join(items) + ("\n" if items else "") +
                "</channel>\n</rss>\n")
        write(ROOT / "feed.xml", feed)

    # --- the sitemap -------------------------------------------------
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    fixed = [(url, git_date(rel)) for url, rel in FIXED_PAGES if (ROOT / rel).exists()]
    seen = set()
    for url, lastmod in fixed + sitemap:
        if url in seen:
            continue
        seen.add(url)
        lines.append(f"  <url><loc>{SITE}/{url}</loc><lastmod>{lastmod}</lastmod></url>")
    lines.append("</urlset>")
    write(ROOT / "sitemap.xml", "\n".join(lines) + "\n")

    if warnings:
        print(f"Done, with {len(warnings)} warning(s) above.")
    else:
        print("Done.")


if __name__ == "__main__":
    main()
