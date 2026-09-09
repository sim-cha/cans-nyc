# cans.nyc

Static informational site about New York City's official NYC Bin mandate, sponsored by Primo Cans (https://primocans.com).

Plain HTML/CSS - no build step, no dependencies. Serve the folder as-is.

## Deploy to GitHub Pages

1. Create a repo (e.g. `cans-nyc`) and push this folder to `main`.
2. Repo Settings -> Pages -> Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Settings -> Pages -> Custom domain: `cans.nyc` (the CNAME file is already included). Enable "Enforce HTTPS" once the certificate provisions.
4. DNS at the cans.nyc registrar:
   - A records for `cans.nyc` -> 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - CNAME for `www.cans.nyc` -> `<github-username>.github.io`

## Publishing a new article (current workflow)

He texts the article/link/notes to Instinct on WhatsApp. Publishing is one command:

    python3 scripts/publish.py --title "Article title" --body body.html --summary "One-line teaser for the news index"

This creates `articles/<slug>.html` from the shared template and inserts a linked
item at the top of `news.html` (at the NEW-ARTICLES-HERE marker). Commit and push;
GitHub Pages deploys in about a minute.

## Social sharing (future)

Social accounts don't exist yet, so nothing is wired up. When they do:
- Preferred: connect the accounts to a free Buffer plan (3 channels) and queue each
  new article when it's published - no code changes needed.
- Alternative: a small GitHub Action that posts on merge to main.
Either way the site needs no rebuild; article pages carry the canonical URLs.
