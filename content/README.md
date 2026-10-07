# content/ — the words Livo and livoenterprises.com share

Every file here is a master copy. The website's pages are built from
these files (by `tools/build_content.py`, run by GitHub Actions after
each change), and the Livo app carries the same files in its bundle and
shows them on its own screens. Change the `.md`, never the generated
`.html`.

## Files

| File | Website | In Livo |
|---|---|---|
| `privacy.md` | `/privacy.html` (the URL Apple has) | Settings › About › Privacy Policy |
| `support.md` | `/support.html` | Settings › About › Support |
| `about-livo.md` | `/about-livo.html` | Settings › About › About Livo, and Getting Started's About door |
| `guide/*.md` | `/guide/<name>.html`, listed at `/guide/` | Organize › Guide |

## The header

Each file starts with a header between two `---` lines:

```
---
title: Privacy Policy
description: One sentence for search engines and link previews.
version: 2
updated: 2026-10-07
web: privacy.html
nav: Support
style: policy
app: privacy
lede: One sentence shown large under the title.
---
```

`title`, `version` and `updated` are required. Raise `version` by one
and set `updated` whenever the words change; the website shows both
under the title, and so does the app, so anyone can tell which words
they are reading. `web` is where the page is written (leave it out for
a file the app shows but the site does not). `nav` names the top-bar
item to mark as current. `style: policy` gives the privacy page its
tighter headings. `app` records which screen in Livo shows the file.
Guide files take `order: 1`, `2`, … for the list at `/guide/`.

## The Livo Markdown subset

So that the app's own renderer can show the same file, only these are
used in the body:

- `##` and `###` headings (the title comes from the header; no `#`)
- paragraphs, separated by a blank line
- `**bold**` and `*italic*`
- `[links](https://…)` and `[mail](mailto:…)`
- `- ` bullet lists and `1. ` numbered lists

No tables, images, code blocks or raw HTML. The builder refuses a file
that uses them.

## How a change reaches the site and the app

1. Edit the `.md` (or ask Claude for the new version), raise `version`,
   set `updated`.
2. Upload it here through GitHub's "Add file › Upload files" and commit.
3. GitHub Actions rebuilds the pages and commits them; Cloudflare Pages
   publishes within about a minute. Check the Actions tab if a page does
   not change.
4. The next Livo code script copies `content/` into the app
   (`Livo/Content/`), naming the content version it carries. The words
   on the phone change with that build.
