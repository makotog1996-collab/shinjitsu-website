import copy,json,threading,functools
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];results=[]
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path=='/privacy':self.path='/privacy.html'
  super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(root/'public')))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
config=json.loads((root/'public/data/site.json').read_text());data=json.loads((root/'data/notes.json').read_text())
shots=root/'test-results/screenshots';shots.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1000},locale='ja-JP',timezone_id='Asia/Tokyo')
 page=context.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base,wait_until='networkidle');page.screenshot(path=str(shots/'desktop.png'),full_page=True)
 assert page.title()=='真実｜日々をアップデート'
 assert page.locator('.theme-card').count()==4
 for n in data['notes']:
  assert page.locator('[data-note-name]').filter(has_text=n['displayName']).count()==1
 for social in ['https://x.com/abp12f','https://www.tiktok.com/@otokomigaki.lab2','https://www.instagram.com/shinjitsu_aiai/']:
  assert page.locator('#social a[href="'+social+'"]').count()==1
 assert page.locator('#latest-articles .article-card').count()==6
 assert page.locator('h1').count()==1
 assert page.evaluate('getComputedStyle(document.body).backgroundColor')=='rgb(248, 247, 242)'
 assert not errors,errors
 results.append('Desktop title, 4 live names, 3 original SNS URLs, 6 articles, light background, no JS exceptions: PASS')
 for width in [320,375,390,430,768,1440]:
  page.set_viewport_size({'width':width,'height':844});page.reload(wait_until='networkidle')
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'overflow {width}'
  cards=page.locator('.theme-card').all()
  assert all(c.bounding_box()['height']>=44 for c in cards)
  if width==390:page.screenshot(path=str(shots/'mobile.png'),full_page=True)
 results.append('320, 375, 390, 430, 768, 1440 px: no horizontal overflow; theme tap areas >=44px: PASS')
 page.goto(base+'/privacy',wait_until='networkidle');assert '真実｜日々をアップデート' in page.title();assert 'MAKOTO LINKS' not in page.content()
 results.append('Privacy route and renewed brand: PASS')
 context.close()
 # JavaScript disabled: static snapshot still supplies all names, links and articles.
 ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});pg=ctx.new_page();pg.goto(base)
 assert pg.locator('.theme-card').count()==4;assert pg.locator('#latest-articles .article-card').count()==6
 results.append('JavaScript disabled: static names, themes and articles remain: PASS');ctx.close()
 # Offline JSON: generated snapshot remains navigable.
 ctx=browser.new_context();pg=ctx.new_page();pg.route('**/data/*',lambda route:route.abort());pg.goto(base,wait_until='networkidle')
 assert pg.locator('.theme-card').count()==4;assert pg.locator('#latest-articles .article-card').count()==6
 results.append('JSON network failure: snapshot remains usable: PASS');ctx.close()
 # Remote refresh simulates the next successful daily update, without changing note.
 remote='https://raw.githubusercontent.com/example/site/HEAD/data/notes.json'
 cfg={**config,'remoteDataUrl':remote};changed=copy.deepcopy(data);changed['notes'][0]['displayName']='名前変更のテスト <script>alert(1)</script>';changed['notes'][0]['fetchedAt']='2099-01-01T00:00:00+00:00'
 ctx=browser.new_context();pg=ctx.new_page();pg.route('**/data/site.json',lambda r:r.fulfill(json=cfg));pg.route(remote+'?*',lambda r:r.fulfill(json=changed));pg.goto(base,wait_until='networkidle')
 assert pg.locator('[data-note-name]').first.text_content()==changed['notes'][0]['displayName']
 assert pg.locator('[data-note-name] script').count()==0
 results.append('Remote name change automatically reflected as text, without HTML execution: PASS')
 # A failed remote request preserves browser cache across reloads.
 pg.unroute(remote+'?*');pg.route(remote+'?*',lambda r:r.abort());pg.reload(wait_until='networkidle')
 assert pg.locator('[data-note-name]').first.text_content()==changed['notes'][0]['displayName']
 results.append('Remote outage after successful update: latest cached name preserved: PASS');ctx.close()
 # Foreign/malicious article URL must never replace the site links.
 malicious=copy.deepcopy(data);malicious['notes'][0]['articles']=[{'url':'javascript:alert(1)','title':'MALICIOUS','publishedAt':'2099-01-01T00:00:00+00:00'}]
 ctx=browser.new_context();pg=ctx.new_page();pg.route('**/data/site.json',lambda r:r.fulfill(json=cfg));pg.route(remote+'?*',lambda r:r.fulfill(json=malicious));pg.goto(base,wait_until='networkidle');assert pg.locator('a[href^="javascript:"]').count()==0
 results.append('Malicious external article URL rejected: PASS');ctx.close()
 # Share clipboard fallback: deterministic mock, no public-site traffic.
 ctx=browser.new_context();pg=ctx.new_page();pg.add_init_script("Object.defineProperty(navigator,'share',{value:undefined});Object.defineProperty(navigator,'clipboard',{value:{writeText:async url=>{window.copiedUrl=url}}});")
 pg.goto(base,wait_until='networkidle');pg.locator('#share').click();assert pg.evaluate('window.copiedUrl')=='https://neon-empanada-519607.netlify.app/'
 results.append('Share button copies canonical URL: PASS');ctx.close();browser.close()
server.shutdown();(root/'test-results/browser-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print('\n'.join(results))
