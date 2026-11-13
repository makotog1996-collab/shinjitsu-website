"""Static HTML snapshots + same-origin JSON. All RSS acquisition is separate."""
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from update_notes import atomic_json, valid_profile
ESC = lambda value: html.escape(str(value), quote=True)
ICONS = {
'spark':'<path d="m16 3 3.5 9.5L29 16l-9.5 3.5L16 29l-3.5-9.5L3 16l9.5-3.5Z"/><path d="M27 2v6M24 5h6"/>',
'dialogue':'<path d="M27 14a11 11 0 0 1-11 11H7l-5 4 2-9A11 11 0 1 1 27 14Z"/><path d="M10 12h10M10 17h6"/>',
'leaf':'<path d="M26 4C10 2 3 11 8 20s21 5 18-16Z"/><path d="M5 29 21 12M12 22v-8M15 19h8"/>',
'home':'<path d="m3 14 13-11 13 11M7 12v16h18V12M13 28V18h6v10"/>',
'x':'<path d="m6 5 20 22M25 5 6 27M6 5h6l14 22h-6Z"/>',
'music':'<path d="M19 4v18a5 5 0 1 1-5-5M19 4c1 6 4 8 9 8"/>',
'camera':'<rect x="4" y="4" width="24" height="24" rx="7"/><circle cx="16" cy="16" r="6"/><circle cx="24" cy="8" r="1"/>',
}
def icon(name): return '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS.get(name,ICONS['spark'])+'</svg>'
def external(url, cls, body, extra=''): return f'<a class="{cls}" href="{ESC(url)}" target="_blank" rel="noopener noreferrer" {extra}>{body}</a>'
def date_label(raw):
    try: return datetime.fromisoformat(raw).astimezone(ZoneInfo('Asia/Tokyo')).strftime('%Y.%m.%d')
    except (ValueError,TypeError): return ''
def remote_url(config):
    if config.get('remoteDataUrl'):
        if not re.fullmatch(r'https://raw\.githubusercontent\.com/[\w.-]+/[\w.-]+/[^\s]+/data/notes\.json',config['remoteDataUrl']): raise ValueError('Use a public GitHub raw data URL')
        return config['remoteDataUrl']
    repo = os.environ.get('REPOSITORY_URL','')
    match = re.fullmatch(r'(?:https://github.com/|git@github.com:)([\w.-]+/[\w.-]+?)(?:\.git)?', repo)
    if not match:
        try:
            repo = subprocess.check_output(['git','remote','get-url','origin'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
            match = re.fullmatch(r'(?:https://github.com/|git@github.com:)([\w.-]+/[\w.-]+?)(?:\.git)?', repo)
        except (subprocess.CalledProcessError,FileNotFoundError): pass
    return 'https://raw.githubusercontent.com/'+match[1]+'/main/data/notes.json' if match else ''
def build():
    config = json.loads((ROOT/'config/site.json').read_text())
    try: cache = json.loads((ROOT/'data/notes.json').read_text())
    except (FileNotFoundError,json.JSONDecodeError): cache = {'schemaVersion':1,'notes':[]}
    cards=[]; footer=[]; theme_chips=[]; notes=[]
    saved={n['url']:n for n in cache['notes']}
    for index,item in enumerate(config['notes']):
        if not valid_profile(item['url']): raise ValueError('Invalid note URL')
        entry=saved.get(item['url'],{})
        name=entry.get('displayName') or item['category']+'のnote'
        notes.append({**item,'displayName':name})
        cards.append(external(item['url'],f'theme-card {item.get("color","sage")}',f'<div class="theme-top"><span class="theme-icon">{icon(item.get("symbol","spark"))}</span><span class="card-number">{index+1:02}</span></div><h3>{ESC(item["category"])}</h3><p class="note-name" data-note-name="{ESC(item["url"])}">{ESC(name)}</p><p class="theme-description">{ESC(item.get("description", "このテーマの発信をnoteで読む。"))}</p><span class="card-link">noteを読む <span aria-hidden="true">↗</span></span>'))
        footer.append(external(item['url'],'',ESC(item['category'])))
        theme_chips.append(f'<a href="#theme-{index+1}" class="topic-chip">{ESC(item["category"].split("・")[0])}<span aria-hidden="true">↗</span></a>')
        cards[-1]=cards[-1].replace('target="_blank"',f'id="theme-{index+1}" target="_blank"',1)
    articles=[]
    for item in config['notes']:
        for article in saved.get(item['url'],{}).get('articles',[]): articles.append({**article,'category':item['category']})
    articles.sort(key=lambda item:item['publishedAt'],reverse=True)
    articles=articles[:6]
    article_cards=[]
    for article in articles:
        image = f'<img src="{ESC(article["image"])}" alt="" width="640" height="336" loading="lazy" decoding="async" referrerpolicy="no-referrer">' if article.get('image') else '<span class="article-placeholder" aria-hidden="true">'+icon('leaf')+'</span>'
        article_cards.append(external(article['url'],'article-card',f'<div class="article-image">{image}</div><div class="article-body"><p class="article-meta"><span>{ESC(article["category"].split("・")[0])}</span><time datetime="{ESC(article["publishedAt"])}">{date_label(article["publishedAt"])}</time></p><h3>{ESC(article["title"])}</h3><span class="article-link">noteで読む <span aria-hidden="true">↗</span></span></div>'))
    socials=[]
    for item in config['socials']:
        socials.append(external(item['url'],'social-card',f'<span class="social-icon">{icon(item.get("symbol","spark"))}</span><div><h3>{ESC(item["name"])}</h3><p>{ESC(item["description"])}</p><span class="social-handle">{ESC(item["handle"])}</span></div><span class="social-arrow" aria-hidden="true">↗</span>'))
    recommended=[external(i['url'],'recommended-card',f'<span>{ESC(i["category"].split("・")[0])}</span><h3>{ESC(i["title"])}</h3><span class="recommended-arrow" aria-hidden="true">↗</span>') for i in config['recommended']]
    offers=[]
    for item in config.get('offers',[]):
        if not item.get('url','').startswith('https://'): raise ValueError('Offer must have an HTTPS URL')
        offers.append(external(item['url'],'recommended-card',f'<span>{ESC(item.get("disclosure",""))}</span><h3>{ESC(item["title"])}</h3><p>{ESC(item["description"])}</p>'))
    template=(ROOT/'templates/index.html').read_text()
    data={'NAME':ESC(config['name']),'TAGLINE':ESC(config['tagline']),'DESCRIPTION':ESC(config['description']),'SITE_URL':ESC(config['url']),'THEMES':''.join(cards),'CHIPS':''.join(theme_chips),'ARTICLES':''.join(article_cards),'SOCIALS':''.join(socials),'FOOTER_NOTES':''.join(footer),'FOOTER_SOCIALS':''.join(external(i['url'],'',ESC(i['name'])) for i in config['socials']),'RECOMMENDED':''.join(recommended),'YEAR':str(datetime.now().year),'ARTICLE_HIDDEN':' hidden' if not articles else '', 'OFFERS':''.join(offers) if offers else '<div class="offer-empty"><span class="offer-icon" aria-hidden="true">＋</span><div><h3>暮らしに、学びに。次の小さな一歩を。</h3><p>役立つアイテムやコンテンツを、ここで少しずつご紹介していきます。</p><span class="preparing">ただいま準備中です</span></div></div>'}
    for key,value in data.items(): template=template.replace('{{'+key+'}}',value)
    if '{{' in template: raise ValueError('Unfilled template')
    (ROOT/'public/index.html').write_text(template)
    atomic_json(ROOT/'public/data/notes.json',cache)
    atomic_json(ROOT/'public/data/site.json',{'notes':notes,'remoteDataUrl':remote_url(config)})
    structured={'@context':'https://schema.org','@type':'WebSite','name':config['name'],'url':config['url']+'/','inLanguage':'ja','author':{'@type':'Person','name':'真実','sameAs':[i['url'] for i in config['notes']+config['socials']]}}
    (ROOT/'public/structured-data.json').write_text(json.dumps(structured,ensure_ascii=False))
    # Inline JSON-LD escaped independently from HTML text.
    template=template.replace('<!-- STRUCTURED_DATA -->','<script type="application/ld+json">'+json.dumps(structured,ensure_ascii=False).replace('<','\\u003c')+'</script>')
    (ROOT/'public/index.html').write_text(template)
    print('Built public/:',len(cards),'themes,',len(articles),'articles; remote updates', 'configured' if remote_url(config) else 'not configured')
if __name__=='__main__': build()
