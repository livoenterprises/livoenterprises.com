# livoenterprises.com

The public website for Livo Enterprises. Plain HTML and CSS, no build step,
hosted on Cloudflare Pages from this repository. Every push to `main`
publishes within about a minute.

## Pages

- `index.html` — front page: mission, the two promises, products, latest notes
- `about.html` — why Ken started the company
- `livocapsule.html` — product page
- `support.html` — support and FAQ
- `privacy.html` — privacy policy (Apple requires this URL)
- `blog/` — Notes (the blog). `blog/index.html` lists the posts
- `404.html` — not-found page

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
