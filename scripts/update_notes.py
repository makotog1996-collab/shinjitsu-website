"""Public RSS only. No API key, external dependencies, or browser CORS dependency."""
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 3 * 1024 * 1024

class SummaryParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.hidden += 1
        elif tag in ('p', 'br', 'div', 'li'): self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.hidden = max(0, self.hidden - 1)
        elif tag in ('p', 'div', 'li'): self.parts.append(' ')

    def handle_data(self, data):
        if not self.hidden: self.parts.append(data)

def plain_summary(raw):
    parser = SummaryParser()
    parser.feed(raw or '')
    text = ' '.join(''.join(parser.parts).split())
    return text[:180] + ('…' if len(text) > 180 else '')

def valid_profile(url):
    return isinstance(url, str) and re.fullmatch(r'https://note\.com/[A-Za-z0-9_]+', url) is not None

def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write('\n')
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def fetch_rss(url):
    if not valid_profile(url): raise ValueError('Invalid note profile URL')
    request = urllib.request.Request(url + '/rss', headers={'User-Agent':'ShinjitsuLinksRSS/1.0 (public RSS reader)', 'Accept':'application/rss+xml, application/xml, text/xml'})
    with urllib.request.urlopen(request, timeout=25) as response:
        if not response.url.startswith(url + '/rss'): raise ValueError('Unexpected redirect')
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES: raise ValueError('RSS too large')
    return raw

def parse_rss(raw, url):
    if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper(): raise ValueError('DTD is not supported')
    root = ET.fromstring(raw)
    channel = root.find('channel')
    if channel is None: raise ValueError('Missing channel')
    if (channel.findtext('link') or '').strip().rstrip('/') != url: raise ValueError('RSS account mismatch')
    name = (channel.findtext('title') or '').strip()
    if not name or len(name) > 300: raise ValueError('Missing/invalid display name')
    articles = []
    for item in channel.findall('item')[:30]:
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        if not re.fullmatch(re.escape(url) + r'/n/n[a-f0-9]+', link) or not title: continue
        try: date = parsedate_to_datetime(item.findtext('pubDate')).astimezone(timezone.utc).isoformat()
        except (ValueError, TypeError, AttributeError): continue
        image = (item.findtext('{http://search.yahoo.com/mrss/}thumbnail') or '').strip()
        if not re.match(r'^https://assets\.st-note\.com/', image): image = ''
        summary = plain_summary(item.findtext('description'))
        articles.append({'title':title[:500], 'url':link, 'publishedAt':date, 'image':image, 'summary':summary})
    return name, articles

def update(config, previous, fetch=fetch_rss, now=None):
    now = now or datetime.now(timezone.utc).isoformat()
    old = {item['url']:item for item in previous.get('notes', [])}
    results = []
    for item in config['notes']:
        url = item['url']
        if not valid_profile(url): raise ValueError('Invalid configured URL')
        cached = old.get(url, {})
        try:
            name, articles = parse_rss(fetch(url), url)
            results.append({'url':url, 'displayName':name, 'fetchedAt':now, 'articles':articles, 'status':'ok'})
        except Exception as error:
            print(f'RSS unavailable: {url} ({type(error).__name__}); keeping last good data', file=sys.stderr)
            results.append({'url':url, 'displayName':cached.get('displayName') or item['category']+'のnote', 'fetchedAt':cached.get('fetchedAt'), 'articles':cached.get('articles', []), 'status':'cached' if cached.get('fetchedAt') else 'fallback'})
    return {'schemaVersion':1, 'checkedAt':now, 'notes':results}

def main():
    config = json.loads((ROOT/'config/site.json').read_text())
    path = ROOT/'data/notes.json'
    try: previous = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError): previous = {}
    result = update(config, previous)
    atomic_json(path, result)
    atomic_json(ROOT/'public/data/notes.json', result)
    print('Cached',len(result['notes']),'profiles;',sum(n['status']=='ok' for n in result['notes']),'fetched successfully')

if __name__ == '__main__': main()
