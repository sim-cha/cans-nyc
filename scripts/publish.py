#!/usr/bin/env python3
"""Publish a new article to cans.nyc.

Usage:
  python3 scripts/publish.py --title "Article title" --body body.html [--slug my-slug] [--date "September 10, 2026"] [--summary "One-line summary for the news index"]

Body file is HTML (paragraphs wrapped in <p>). Run from the repo root.
Creates articles/<slug>.html and inserts a linked item at the top of news.html.
"""
import argparse, datetime, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def slugify(t):
    s = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    return s[:60]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--title', required=True)
    ap.add_argument('--body', required=True, help='path to HTML body file')
    ap.add_argument('--slug')
    ap.add_argument('--date', default=datetime.date.today().strftime('%B %-d, %Y'))
    ap.add_argument('--summary', default='')
    a = ap.parse_args()

    slug = a.slug or slugify(a.title)
    top = (ROOT/'parts/top.html').read_text()
    top = top.replace('__TITLE__', f'{a.title} - cans.nyc')
    top = top.replace('__DESC__', a.summary or a.title)
    for i in range(1, 6):
        top = top.replace(f'__ACT{i}__', ' class="active"' if i == 4 else '')
    # article pages live one level down
    top = top.replace('href="assets/', 'href="../assets/').replace('href="index.html"', 'href="../index.html"')
    top = top.replace('href="timeline.html"', 'href="../timeline.html"').replace('href="faq.html"', 'href="../faq.html"')
    top = top.replace('href="news.html"', 'href="../news.html"').replace('href="about.html"', 'href="../about.html"')

    bottom = (ROOT/'parts/bottom.html').read_text()
    for page in ['index','timeline','faq','news','about']:
        bottom = bottom.replace(f'href="{page}.html"', f'href="../{page}.html"')

    body = Path(a.body).read_text()
    article = f'''{top}
<article>
  <p><a href="../news.html">&larr; News</a></p>
  <h2 style="font-size:28px">{a.title}</h2>
  <p class="updated">{a.date}</p>
{body}
</article>
{bottom}'''
    out = ROOT/'articles'/f'{slug}.html'
    out.write_text(article)

    news = ROOT/'news.html'
    s = news.read_text()
    item = f'''
<div class="news-item">
  <div class="date">{a.date}</div>
  <h3><a href="articles/{slug}.html">{a.title}</a></h3>
  <p>{a.summary}</p>
</div>
<!-- NEW-ARTICLES-HERE -->'''
    if '<!-- NEW-ARTICLES-HERE -->' not in s:
        sys.exit('news.html is missing the NEW-ARTICLES-HERE marker')
    s = s.replace('<!-- NEW-ARTICLES-HERE -->', item, 1)
    news.write_text(s)
    print(f'published articles/{slug}.html and updated news.html')

if __name__ == '__main__':
    main()
