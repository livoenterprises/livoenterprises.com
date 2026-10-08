# livoenterprises.com

The public website for Livo Enterprises. Plain HTML and CSS, no build step,
hosted on Cloudflare Pages from this repository. Every push to `main`
publishes within about a minute.

## Pages

- `index.html` — front page: mission, the two promises, products, latest notes
- `about.html` — why Ken started the company
- `livocapsule.html` — product page
- `support.html` — support and FAQ. Generated from `content/support.md`
- `privacy.html` — privacy policy (Apple requires this URL). Generated from `content/privacy.md`
- `about-livo.html` — what Livo is (the app's About Livo text). Generated from `content/about-livo.md`
- `guide/` — the Livo guide, one page per topic. Generated from `content/guide/*.md`
- `blog/` — Notes (the blog). `blog/index.html` lists the posts
- `404.html` — not-found page

## Content: the words the site and the Livo app share (Oct 2026)

`content/` holds Markdown masters for the privacy policy, the support page,
About Livo and the Livo guide. `tools/build_content.py` turns them into
`privacy.html`, `support.html`, `about-livo.html` and `guide/*.html`;
GitHub Actions (`.github/workflows/build-content.yml`) runs it after every
change to `content/` and commits the pages, and Cloudflare publishes as
usual. The Livo app carries the same `content/` files and shows them on
its own screens. **Edit the `.md`, never those generated pages** (each
starts with a GENERATED comment). `content/README.md` has the header
format, the Markdown subset and the steps.

## Plumbing

- `assets/style.css` — the one stylesheet
- `assets/social-card.png` — the image shown when a link is shared
- `feed.xml` — RSS feed for Notes
- `sitemap.xml` — list of pages for search engines
- `robots.txt` — points search engines at the sitemap
- `_headers`, `_redirects` — Cloudflare Pages configuration

## Publishing a new note

A note is a Markdown file, `content/blog/<slug>.md` (the slug is the
page's address: lower-case letters, digits and hyphens). Its pictures go
in `content/blog/images/`. The builder makes `blog/<slug>.html`, the list
in `blog/index.html`, the newest notes on the front page, `feed.xml` and
`sitemap.xml`. `content/README.md` has the header and what the body may
use. Easiest: hand Claude the draft text and the pictures; it returns the
file(s), you apply and publish them with `LivoContent.sh` (below).

The content loop on Ken's Mac (`~/Developer/Projects/LivoContent.sh`,
v2): `fetch` mirrors this repo into the OneDrive editing folder
(`content/` and `site/`; generated pages are never fetched), `status`
says what differs, `apply <zip>` drops a delivered zip in, `publish`
copies the editing folder here, builds the pages, commits and pushes
(the site is live about a minute later), `sync` carries `content/` into
the Livo app. `pulls` and `restore <stamp>` keep every fetch and put one
back. GitHub's web "Upload files" still works for a single file.

`blog/post-template.html` is from before the builder made notes; it is
kept for reference only.

Topics used on notes

Own your data · Technology that serves you · Building with AI · Keeping memories

## When a second product ships

Add `livominder.html` (copy `livocapsule.html`), link it from the Products
section of `index.html`, and change the first nav link on every page from
"LivoCapsule" to "Products" pointing at `/#products`.
