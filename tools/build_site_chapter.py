#!/usr/bin/env python3
"""Build the website chapter of the Livo Guide pack: the Livo Enterprises website in plain Markdown.

Run from the root of the Livo Content Edits folder (the one that holds content/ and site/):
    python3 site/tools/build_site_chapter.py
It reads the built pages in site/ (index.html, about.html, products.html, livocapsule.html, blog/*.html)
and writes site/pack/20-site.md, which build_pack.py adds to the pack. Run it after build_content.py,
and before build_pack.py. Python 3 only, nothing to install.
"""
import glob, html, os, re, sys
from html.parser import HTMLParser

ROOT = os.getcwd()
SITE = os.path.join(ROOT, "site") if os.path.isdir(os.path.join(ROOT, "site")) else ROOT
BASE = "https://livoenterprises.com"
SKIP_TAGS = {"script", "style", "svg", "nav", "header", "footer", "button", "form", "noscript", "template"}
BLOCKS = {"p", "h1", "h2", "h3", "h4", "li", "blockquote", "figcaption", "dt", "dd", "div", "section", "article", "ul", "ol", "br", "tr"}
NOISE = {"Mom", "Dad", "Grandma", "▶", "Skip to content"}


class Md(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.cur, self.skip, self.href, self.in_main = [], "", 0, None, 0
        self.kind, self.depth_main = None, 0

    def flush(self):
        t = re.sub(r"\s+", " ", self.cur).strip()
        self.cur = ""
        if t and t not in NOISE:
            if self.kind == "li":
                t = "- " + t
            elif self.kind in ("h1", "h2", "h3", "h4"):
                t = "#" * int(self.kind[1]) + " " + t
            self.out.append(t)
        self.kind = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("main", "article"):
            self.in_main += 1
        if tag in SKIP_TAGS or a.get("aria-hidden") == "true" or "gift-mock" in (a.get("class") or ""):
            self.skip += 1
            self._skipping = getattr(self, "_skipping", []) + [tag]
            return
        if self.skip:
            if tag not in ("br", "img", "hr", "input", "meta", "link"):
                self._skipping = getattr(self, "_skipping", []) + [tag]
                self.skip += 1
            return
        if tag in BLOCKS:
            self.flush()
            if tag in ("li", "h1", "h2", "h3", "h4"):
                self.kind = tag
        if tag == "a":
            self.href = a.get("href")
            self.cur += "\u0001"

    def handle_endtag(self, tag):
        if tag in ("main", "article"):
            self.in_main = max(0, self.in_main - 1)
        if self.skip:
            sk = getattr(self, "_skipping", [])
            if sk and sk[-1] == tag:
                sk.pop()
                self.skip -= 1
            return
        if tag == "a":
            self.cur += "\u0002" + (self.href or "") + "\u0003"
            self.href = None
        if tag in BLOCKS:
            self.flush()

    def handle_data(self, data):
        if not self.skip:
            self.cur += data


def link_fix(text):
    def sub(m):
        label, href = m.group(1).strip(), m.group(2).strip()
        if href.startswith("mailto:"):
            addr = href[7:].split("?")[0]
            return addr if label == addr else "%s (%s)" % (label, addr)
        if href.startswith("#") or not href:
            return label
        if href.startswith("/"):
            href = BASE + href
        if href.startswith(BASE) or href.startswith("http"):
            return "[%s](%s)" % (label, href)
        return label
    return re.sub(r"\u0001(.*?)\u0002(.*?)\u0003", sub, text)


def drop_dup_heading(md, label):
    """Remove the page's own first heading when the chapter heading above it already says the same."""
    lines = md.split("\n")
    for i, l in enumerate(lines):
        if l.strip():
            m = re.match(r"^#{1,6} (.*)$", l)
            if m:
                t = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", m.group(1)).strip().lower()
                if t and t in label.lower():
                    del lines[i]
            break
    return "\n".join(lines).strip()


def page_md(path, shift=1):
    """The main text of one built page, as Markdown, with headings pushed down `shift` levels."""
    raw = open(path, encoding="utf-8").read()
    m = re.search(r"<main\b.*?</main>", raw, re.S)
    body = m.group(0) if m else raw
    p = Md()
    p.feed(body)
    p.flush()
    lines = []
    for l in p.out:
        l = link_fix(l)
        l = re.sub(r"^(#{1,4}) ", lambda mm: "#" * min(6, len(mm.group(1)) + shift) + " ", l)
        lines.append(l)
    # a blank line between blocks, but list items stay together
    res = []
    for i, l in enumerate(lines):
        if i and not (l.startswith("- ") and lines[i - 1].startswith("- ")):
            res.append("")
        res.append(l)
    return "\n".join(res).strip()


def meta(path, prop):
    raw = open(path, encoding="utf-8").read()
    m = re.search(r'<meta[^>]+(?:name|property)="%s"[^>]+content="([^"]*)"' % re.escape(prop), raw)
    return html.unescape(m.group(1)) if m else ""


def title(path):
    raw = open(path, encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", raw, re.S)
    return html.unescape(m.group(1)).strip() if m else os.path.basename(path)


def pg(name):
    return os.path.join(SITE, name)


out = []
out.append("# The Livo Enterprises website\n\nThis chapter is the rest of livoenterprises.com: the company, the products, LivoCapsule's own page, our Notes, and every way to reach us. The topics above cover how to use the app; the Privacy Policy, Support and About Livo are the pages of the same names.")
out.append("## Contact links\n\n"
           "- Questions, help, or interest in a product: support@livoenterprises.com\n"
           "- Ideas, or a reply to one of our Notes: feedback@livoenterprises.com\n"
           "- Privacy questions: privacy@livoenterprises.com\n"
           "- In the app: **Send Feedback** (Settings › About)\n"
           "- Website: https://livoenterprises.com · Notes by RSS: https://livoenterprises.com/feed.xml\n"
           "- To say you are interested in a product that is not out yet, write to support@livoenterprises.com and name the product (LivoCapsule or LivoMinder). We use your email only to tell you when it is available.")
for name, label, url in (("index.html", "Home page: Livo Enterprises", "/"),
                         ("about.html", "Why Livo: a note from the founder", "/about.html"),
                         ("products.html", "Products", "/products.html"),
                         ("livocapsule.html", "LivoCapsule, the product page", "/livocapsule.html")):
    if os.path.exists(pg(name)):
        out.append("## %s\n\n*%s%s*\n\n%s" % (label, BASE, url, drop_dup_heading(page_md(pg(name), shift=1), label)))
posts = []
for f in glob.glob(pg("blog/*.html")):
    stem = os.path.basename(f)[:-5]
    if stem in ("index", "post-template"):
        continue
    src = os.path.join(ROOT, "content", "blog", stem + ".md")
    if os.path.exists(src) and re.search(r"^listed:\s*no\s*$", open(src, encoding="utf-8").read().split("\n---", 2)[0], re.M):
        continue  # an unlisted note is not part of the public Notes, so it is not here either
    raw = open(f, encoding="utf-8").read()
    dm = re.search(r'<time[^>]*datetime="([0-9-]+)"', raw)
    posts.append((dm.group(1) if dm else "0000", stem, f))
posts.sort(reverse=True)
if os.path.exists(pg("blog/index.html")):
    out.append("## Notes\n\n*%s/blog/*\n\n%s" % (BASE, drop_dup_heading(page_md(pg("blog/index.html"), shift=1), "Notes")))
for date, stem, f in posts:
    nt = re.sub(r"\s*[|·–—]\s*Livo.*$", "", title(f))
    out.append("### Note: %s\n\n*%s/blog/%s.html · %s*\n\n%s" % (nt, BASE, stem, date, drop_dup_heading(page_md(f, shift=2), nt)))
text = "\n\n".join(out).strip() + "\n"
if "\u0001" in text or "\u0002" in text or "\u0003" in text:
    sys.exit("A link marker was left in the text.")
dest = os.path.join(SITE, "pack", "20-site.md")
with open(dest, "w", encoding="utf-8") as fh:
    fh.write(text)
print("Wrote %s: %d listed notes, %d words, %d bytes." % (dest, len(posts), len(text.split()), len(text.encode("utf-8"))))
