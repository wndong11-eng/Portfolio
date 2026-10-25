"""Embed the approved source as static HTML; run from repository root."""
from pathlib import Path
import html
import re

source = Path('articles/ad-agency-pricing.md').read_text(encoding='utf-8-sig')
body = source.split('---', 2)[2].strip()
def inline(s):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html.escape(s))
lines = body.splitlines()
parts = []
heading_ids = iter(['article-scope', 'article-return', 'article-readiness'])
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    if line.startswith('## '):
        parts.append(f'<h3 id="{next(heading_ids)}">{inline(line[3:])}</h3>')
    elif line == '---':
        parts.append('<hr>')
    elif line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            rows.append([s.strip() for s in lines[i].strip().strip('|').split('|')])
            i += 1
        head = ''.join(f'<th scope="col">{inline(s)}</th>' for s in rows[0])
        data = ''.join('<tr>'+''.join(f'<td>{inline(s)}</td>' for s in r)+'</tr>' for r in rows[2:])
        parts.append(f'<div class="article-table"><table><caption>單一廣告組合預算試算（原文範例）</caption><thead><tr>{head}</tr></thead><tbody>{data}</tbody></table></div>')
        continue
    elif line.startswith('- '):
        items = []
        while i < len(lines) and lines[i].strip().startswith('- '):
            items.append('<li>'+inline(lines[i].strip()[2:])+'</li>')
            i += 1
        parts.append('<ul>'+''.join(items)+'</ul>')
        continue
    elif line.startswith('> '):
        parts.append('<blockquote>'+inline(line[2:])+'</blockquote>')
    else:
        parts.append('<p>'+inline(line)+'</p>')
    i += 1

section = '''
  <!-- Advertising cooperation guide: full article is present before interaction -->
  <section id="insights" aria-labelledby="insights-heading" class="article-section">
    <div class="article-container">
      <h2 id="insights-heading">廣告合作指南</h2>
      <p class="article-intro">從實務經驗出發，釐清廣告合作前值得先想清楚的事。</p>
      <details id="ad-pricing-article" class="article-card">
        <summary>
          <span class="article-card-copy">
            <span class="article-eyebrow">廣告代操・費用評估</span>
            <span class="article-card-title">廣告代操費用怎麼算？</span>
            <span class="article-card-subtitle">報價之外，更該確認的三件事</span>
            <span class="article-card-description">比較報價前，先釐清服務範圍、投入與回報，以及目前是否適合外包。</span>
            <span class="article-meta">溫浩東 <span aria-hidden="true">｜</span> <time datetime="2026-10-25">2026.10.25</time></span>
          </span>
          <span class="article-toggle"><span class="article-open-label">展開閱讀 ＋</span><span class="article-close-label">收合文章 −</span></span>
        </summary>
        <article aria-label="廣告代操費用怎麼算？報價之外，更該確認的三件事" class="article-content">
          <nav class="article-contents" aria-label="文章目錄">
            <a href="#article-scope">報價範圍</a><a href="#article-return">投入與回報</a><a href="#article-readiness">外包評估</a>
          </nav>
          <div class="article-prose">BODY</div>
          <div class="article-actions">
            <a class="article-contact" href="#contact">討論我的廣告需求 <span aria-hidden="true">→</span></a>
            <button type="button" data-close-article hidden>收合文章 −</button>
          </div>
        </article>
      </details>
    </div>
  </section>
  <script>
    (() => {
      const article = document.getElementById('ad-pricing-article');
      article.querySelector('[data-close-article]').hidden = false;
      article.querySelector('[data-close-article]').addEventListener('click', () => {
        article.open = false;
        article.querySelector('summary').focus({ preventScroll: true });
        article.scrollIntoView({ block: 'start', behavior: 'instant' });
      });
    })();
  </script>
'''.replace('BODY', '\n'.join(parts))

css = '''
  <style id="article-styles">
    .article-section{padding:88px 24px;background:#0a0a0a;border-top:1px solid #222;color:#bbb;scroll-margin-top:100px}
    .article-container{max-width:1088px;margin:auto}
    .article-eyebrow{display:block;color:#c9a84c;font-size:12px;letter-spacing:.14em;margin:0 0 14px}
    .article-section h2{font-size:36px;font-weight:700;color:#fff;line-height:1.4;margin:0 0 16px}
    .article-intro{margin:0 0 36px;line-height:1.8}
    .article-card{background:linear-gradient(120deg,#1b1914,#111 70%);border:1px solid #756039;border-radius:14px;scroll-margin-top:104px;overflow:hidden}
    .article-card summary{padding:36px 40px;display:flex;align-items:center;justify-content:space-between;gap:28px;cursor:pointer;list-style:none}
    .article-card summary::-webkit-details-marker{display:none}
    .article-card summary:focus-visible,.article-card a:focus-visible,.article-card button:focus-visible{outline:2px solid #e8c97a;outline-offset:-4px}
    .article-card-copy{display:block;min-width:0}
    .article-card-title{display:block;color:#fff;font-size:30px;font-weight:700;line-height:1.5}
    .article-card-subtitle{display:block;font-size:20px;color:#eee;line-height:1.7;margin:5px 0 16px}
    .article-card-description{display:block;line-height:1.9;max-width:650px;font-size:14px}
    .article-meta{display:block;font-size:12px;color:#aaa;margin-top:18px}
    .article-toggle,.article-actions button{border:1px solid #c9a84c;color:#e8c97a;border-radius:5px;padding:12px 20px;font-size:14px;white-space:nowrap;background:transparent}
    .article-close-label{display:none}.article-card[open] .article-open-label{display:none}.article-card[open] .article-close-label{display:inline}
    .article-content{padding:0 40px 36px}
    .article-contents{display:flex;flex-wrap:wrap;gap:12px 28px;border-block:1px solid #54452c;padding:18px 0;margin-bottom:30px}
    .article-contents a{color:#e8c97a;font-size:14px;text-decoration:none}.article-contents a:hover{text-decoration:underline}
    .article-prose{max-width:800px;margin:auto;font-size:16px;line-height:2;color:#c7c7c7;overflow-wrap:anywhere}
    .article-prose h3{font-size:24px;font-weight:700;color:#fff;margin:40px 0 20px;scroll-margin-top:110px;line-height:1.6}
    .article-prose p{margin:0 0 22px}.article-prose strong{color:#f0e5ce;font-weight:700}
    .article-prose ul{list-style:disc;padding-left:24px;margin:0 0 24px}.article-prose li{margin:8px 0}
    .article-prose blockquote{padding:20px 24px;border-left:3px solid #c9a84c;background:#232016;margin:26px 0}
    .article-prose hr{border:0;border-top:1px solid #3b3427;margin:36px 0}
    .article-table{margin:24px 0}.article-table table{width:100%;border-collapse:collapse;font-size:14px;table-layout:fixed}
    .article-table caption{text-align:left;font-size:12px;color:#aaa;margin-bottom:10px}
    .article-table th,.article-table td{padding:12px 8px;border:1px solid #403828;text-align:left;overflow-wrap:anywhere}
    .article-table th{color:#e8c97a;background:#211e16;font-weight:500}
    .article-actions{max-width:800px;margin:36px auto 0;display:flex;flex-wrap:wrap;gap:16px;padding-top:28px;border-top:1px solid #403828}
    .article-contact{display:inline-flex;gap:36px;align-items:center;padding:13px 24px;background:#c9a84c;color:#0a0a0a;border-radius:5px;font-weight:700;text-decoration:none}
    .article-actions button{cursor:pointer}.article-actions button:hover,.article-toggle:hover{background:#c9a84c15}
    @media(max-width:640px){.article-section{padding:56px 16px}.article-section h2{font-size:28px}.article-intro{font-size:14px;margin-bottom:26px}.article-card summary{padding:24px 20px;align-items:flex-start;flex-direction:column;gap:22px}.article-card-title{font-size:23px}.article-card-subtitle{font-size:16px}.article-toggle{align-self:flex-start}.article-content{padding:0 20px 26px}.article-contents{gap:12px 18px}.article-contents a{font-size:13px}.article-prose{font-size:15px;line-height:1.95}.article-prose h3{font-size:21px}.article-table th,.article-table td{padding:10px 4px;font-size:12px}.article-prose blockquote{padding:16px}.article-actions{flex-direction:column}.article-contact{justify-content:center}.article-actions button{min-height:46px}}
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important}}
  </style>
'''
path = Path('index.html')
page = path.read_text(encoding='utf-8')
assert 'id="insights"' not in page, 'Already embedded'
page = page.replace('</head>', css+'\n</head>')
marker = '  <!-- ==================== Contact Section ==================== -->'
assert marker in page
page = page.replace(marker,section+'\n'+marker)
path.write_text(page, encoding='utf-8',newline='\n')
print('Article embedded; original Markdown preserved.')
