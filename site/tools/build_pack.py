#!/usr/bin/env python3
"""Build the Livo Guide pack: one Markdown file from the guide pages and the pack-only chapters.

Run from the root of the Livo Content Edits folder (the one that holds content/ and site/):
    python3 site/tools/build_pack.py
It reads content/guide/*.md, content/privacy.md, content/support.md, content/about-livo.md and
site/pack/*.md (+ pack.txt), and writes site/livo-guide-pack.md. Python 3 only, nothing to install.
Rules: livo:// links keep their words and lose the link (they only work inside the app);
/guide/<topic>.html links become https://livoenterprises.com/guide/<topic>.html; front matter is
turned into a heading and a version line.
"""
import glob, os, re, sys

ROOT = os.getcwd()
def p(*a): return os.path.join(ROOT, *a)

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def split(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    head = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            head[k.strip()] = v.strip()
    return head, m.group(2).strip("\n")

def links(body):
    body = re.sub(r"\[([^\]]+)\]\(livo://[^)]*\)", r"\1", body)
    body = re.sub(r"\]\(/guide/([^)]*)\)", r"](https://livoenterprises.com/guide/\1)", body)
    body = re.sub(r"\]\(/([a-z0-9-]+\.html)\)", r"](https://livoenterprises.com/\1)", body)
    return body

def demote(body):
    # topic headings go one level down: ## -> ###, ### -> ####
    return re.sub(r"^(#{2,3}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)

cfg = {}
for line in read(p("site", "pack", "pack.txt")).split("\n"):
    if ":" in line:
        k, v = line.split(":", 1); cfg[k.strip()] = v.strip()

def fill(text):
    for k, v in cfg.items():
        text = text.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[^}]*\}\}", text)
    if left:
        sys.exit("Unfilled placeholder(s): " + ", ".join(left))
    return text

topics = []
for fn in glob.glob(p("content", "guide", "*.md")):
    head, body = split(read(fn))
    topics.append((int(head.get("order", "999")), head.get("title", os.path.basename(fn)), head, body, os.path.basename(fn)[:-3]))
topics.sort(key=lambda t: (t[0], t[1].lower()))

out = []
out.append(fill(read(p("site", "pack", "00-instructions.md")).strip()))
out.append(fill(read(p("site", "pack", "10-map.md")).strip()))
toc = ["# Contents", "", "The topics, in order. Each is also at " + cfg["guide_url"] + "<name>.html.", ""]
for order, title, head, body, stem in topics:
    toc.append("%d. **%s** — %s" % (order, title, head.get("description", "")))
toc.append("%d. **Privacy Policy** — what Livo keeps and where." % (len(topics) + 1))
toc.append("%d. **Support** — questions and how to reach us." % (len(topics) + 2))
toc.append("%d. **About Livo** — what Livo is and what it promises." % (len(topics) + 3))
out.append("\n".join(toc))
for order, title, head, body, stem in topics:
    out.append("# Topic: %s\n\n*Guide topic %d · version %s · updated %s · %s%s.html*\n\n%s\n\n%s" % (
        title, order, head.get("version", "?"), head.get("updated", "?"), cfg["guide_url"], stem,
        head.get("lede", ""), demote(links(body))))
for fn, label in (("privacy.md", "Privacy Policy"), ("support.md", "Support"), ("about-livo.md", "About Livo")):
    head, body = split(read(p("content", fn)))
    out.append("# %s\n\n*Version %s · updated %s*\n\n%s\n\n%s" % (
        label, head.get("version", "?"), head.get("updated", "?"), head.get("lede", ""), demote(links(body))))
out.append(fill(read(p("site", "pack", "90-glossary.md")).strip()))
text = "\n\n---\n\n".join(out) + "\n"
if "](livo://" in text:
    sys.exit("A livo:// link was left in the pack.")
dest = p("site", "livo-guide-pack.md")
with open(dest, "w", encoding="utf-8") as f:
    f.write(text)
print("Wrote %s: %d topics, %d words, %d bytes." % (dest, len(topics), len(text.split()), len(text.encode("utf-8"))))
