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
| `config/*.txt` | — | the tag stop list and other word lists (`# version: N` at the top) |
| `blog/<slug>.md` | `/blog/<slug>.html`, listed at `/blog/`, in the feed and on the front page | — (the website's alone) |
| `blog/images/*` | `/blog/images/*` | — |

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
Guide files take `order: 1`, `2`, … for the list at `/guide/`, and `screen:`
(the screen whose (i) button opens this topic in the app).

## A note's header

```
---
title: The thread I didn't see until I wrote it down
description: One sentence: the summary under the title in lists and the feed.
date: 2026-09-18
updated: 2026-09-18
topics: Own your data, Technology that serves you
author: Ken Jones
listed: yes
front: yes
draft: no
---
```

`title`, `description` and `date` are required; the file name is the
page's address (`the-thread.md` → `/blog/the-thread.html`: lower-case
letters, digits and hyphens). `updated` defaults to `date`. `listed: no`
builds the page but keeps it out of Notes, the feed and the front page;
`front: no` keeps it off the front page only; `draft: yes` builds it with
`noindex` and never lists it, for looking at it before it goes out. The
topics in use: Own your data · Technology that serves you · Building with
AI · Keeping memories.

A note's body may use everything below and also `> ` quotes and pictures:
`![Caption shown under it](images/photo.jpg)` with the file in
`content/blog/images/`. Keep a picture at most 1600 px wide and under
500 KB (the builder warns, and does not stop, when one is bigger).

## The Livo Markdown subset

So that the app's own renderer can show the same file, only these are
used in the body:

- `##` and `###` headings (the title comes from the header; no `#`)
- paragraphs, separated by a blank line
- `**bold**` and `*italic*`
- `[links](https://…)` and `[mail](mailto:…)`
- `- ` bullet lists and `1. ` numbered lists
- **app links**: `[Open Organize › Family](livo://organize/family)` opens that
  screen inside Livo; on the website the builder shows the words with a
  dotted underline. Links only open screens; they never act. Targets:
  `livo://gallery`, `livo://memory-lane`, `livo://vault`, `livo://search`,
  `livo://gallery/filter`, `livo://gallery/moments`, `livo://organize`,
  `livo://organize/<getting-started|people|places|buckets|life-events|family|backup|activity|trash|settings>`,
  `livo://settings/<your-name|appearance|onedrive|family-share|about>`,
  `livo://vault/places`, `livo://getting-started`

No tables, images, code blocks or raw HTML. The builder refuses a file
that uses them.

## How a change reaches the site and the app

1. Edit the `.md` in the OneDrive editing folder (or ask Claude for the
   new version and `./LivoContent.sh apply` the zip), raise `version`,
   set `updated` (a note: `updated`).
2. `./LivoContent.sh publish "what changed"` copies it here, builds the
   pages, commits and pushes. Cloudflare Pages publishes within about a
   minute. (GitHub's "Add file › Upload files" still works for one file;
   then GitHub Actions builds the pages. Check the Actions tab if a page
   does not change.)
3. `./LivoContent.sh sync` copies the pages, the guide and `config/` into
   the app (`Livo/Content/`); press Run in Xcode. The notes never go into
   the app.
