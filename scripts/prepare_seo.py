"""SEO for real static pages; preview copies are separately marked noindex."""
from pathlib import Path
from urllib.parse import urljoin
from html import escape
import json,re,os
ROOT=Path(__file__).resolve().parents[1]
def prepare_seo(config):
 public=ROOT/'public';origin=config['url'].rstrip('/');paths=['/','/privacy.html']
 for f in sorted((public/'tools/repurpose').rglob('*.html')):
  rel='/'+str(f.relative_to(public));canonical=origin+(rel[:-10] if rel.endswith('index.html') else rel)
  text=f.read_text();text=re.sub(r'<meta name="robots" content="[^"]*">','',text);text=re.sub(r'<link rel="canonical" href="[^"]*">','',text);text=re.sub(r'<meta property="og:[^"]*"[^>]*>','',text);text=re.sub(r'<meta name="twitter:[^"]*"[^>]*>','',text);text=re.sub(r'<script type="application/ld\+json">.*?</script>','',text,flags=re.S)
  title=re.search(r'<title>(.*?)</title>',text).group(1)
  dm=re.search(r'<meta name="description" content="([^"]*)">',text);desc=dm.group(1) if dm else '無料ツールの使い方と、日々の発信に役立つ実践ガイド。'
  text=text.replace('未公開の試作品','無料ツール').replace('無料の試作品','無料ツール').replace('この試作','このツール')
  meta=f'<link rel="canonical" href="{escape(canonical,quote=True)}"><meta property="og:type" content="website"><meta property="og:locale" content="ja_JP"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{escape(canonical,quote=True)}"><meta property="og:image" content="{origin}/og-tools.png"><meta name="twitter:card" content="summary_large_image">'
  schema={'@context':'https://schema.org','@type':'WebApplication'if rel=='/tools/repurpose/index.html'else'WebPage','name':title,'url':canonical,'inLanguage':'ja','isAccessibleForFree':True}
  if schema['@type']=='WebApplication':schema.update({'applicationCategory':'ProductivityApplication','operatingSystem':'Web browser','offers':{'@type':'Offer','price':'0','priceCurrency':'JPY'}})
  meta+='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>'
  if '/analytics.js' not in text:meta+='<script src="/analytics.js" defer></script>'
  text=text.replace('</head>',meta+'</head>');f.write_text(text);paths.append(canonical.removeprefix(origin))
 (public/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(origin+p)+'</loc></url>'for p in paths)+'</urlset>')
 (public/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+origin+'/sitemap.xml\n')

 # Netlify deploy/branch previews must remain outside the search index.
 if os.environ.get('CONTEXT') in ('deploy-preview','branch-deploy'):
  for file in public.rglob('*.html'):
   t=file.read_text();t=re.sub(r'<meta name="robots" content="[^"]*">','',t);file.write_text(t.replace('</head>','<meta name="robots" content="noindex,nofollow"></head>'))
  (public/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
