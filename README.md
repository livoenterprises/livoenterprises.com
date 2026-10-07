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

Easiest: hand Claude the draft text and this folder, and ask for the new post
plus the four updates below. By hand:

1. Copy `blog/post-template.html` to `blog/your-post-slug.html`.
2. In the new file, replace every `POST TITLE`, `ONE-SENTENCE SUMMARY`,
   `POST-SLUG`, `TOPIC` and the two dates, delete the `noindex` line marked
   DELETE, and put the text in `<p>` paragraphs.
3. Add an `<li>` for it at the top of the list in `blog/index.html`
   (copy an existing one). Do the same in `index.html` if it should show on the front page.
4. Add an `<item>` at the top of `feed.xml` (copy an existing one).
5. Add a `<url>` line to `sitemap.xml`.
6. Commit and push.

## Topics used on notes

Own your data · Technology that serves you · Building with AI · Keeping memories

## When a second product ships

Add `livominder.html` (copy `livocapsule.html`), link it from the Products
section of `index.html`, and change the first nav link on every page from
"LivoCapsule" to "Products" pointing at `/#products`.
