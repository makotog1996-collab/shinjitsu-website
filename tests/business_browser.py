"""Business contact integration checks; requires existing Playwright/Chromium."""
import functools,json,threading,urllib.parse
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];PUBLIC=ROOT/'public';OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path.split('?')[0]=='/privacy':self.path='/privacy.html'
  super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(PUBLIC)));threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}';work=json.loads((ROOT/'config/work.json').read_text());site=json.loads((ROOT/'config/site.json').read_text());results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1000},locale='ja-JP');page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base,wait_until='networkidle');assert page.title()==site['seoTitle']
 assert page.locator('h1').count()==1
 assert page.locator('.service-card').count()==8
 assert page.locator('.portfolio-card').count()==2
 assert page.locator('.faq-item').count()==5
 assert page.locator('.process-list>li').count()==3
 for n in site['notes']:assert page.locator('#links a[href="'+n['url']+'"]').count()==1
 for s in site['socials']:assert page.locator('#social a[href="'+s['url']+'"]').count()==1
 assert page.locator('#latest-articles .article-card').count()==6
 assert page.locator('#approved-offers').count()==1
 assert page.locator('form').count()==0
 assert page.locator('#contact .contact-line').get_attribute('href')==work['contact']['lineUrl']
 mail=urllib.parse.urlsplit(page.locator('#contact .contact-email').get_attribute('href'));assert mail.scheme=='mailto' and mail.path==work['contact']['email']
 assert urllib.parse.parse_qs(mail.query)['subject']==['Webサイトからのお問い合わせ']
 assert page.locator('#contact').inner_text().find('合意後')>=0
 results.append('8 services, 2 genuine works, 3 steps, 5 FAQs; original notes/SNS/articles/offers retained; no nonfunctional form: PASS')
 page.locator('.portfolio-card img').evaluate_all("imgs=>imgs.forEach(img=>img.loading='eager')")
 page.wait_for_function("[...document.querySelectorAll('.portfolio-card img')].every(img=>img.complete && img.naturalWidth===1200)")
 results.append('Both real screenshots load; LINE target and decoded mailto recipient/subject are correct: PASS')
 page.locator('.faq-item summary').first.focus();page.keyboard.press('Enter');assert page.locator('.faq-item').first.get_attribute('open') is not None
 for width in [320,375,390,430,768,1024,1440]:
  page.set_viewport_size({'width':width,'height':844});page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Overflow at {width}'
  if width<=680:
   page.wait_for_function("!document.querySelector('.mobile-contact-bar').hidden")
   assert page.locator('.mobile-line-link').bounding_box()['height']>=44
   page.locator('#contact-title').scroll_into_view_if_needed();page.wait_for_function("document.querySelector('.mobile-contact-bar').hidden")
   page.locator('.work-footer-nav').scroll_into_view_if_needed();page.evaluate('scrollTo(0,document.body.scrollHeight)');page.wait_for_function("!document.querySelector('.mobile-contact-bar').hidden")
   footer_mail=page.locator('.work-footer-nav [data-contact-method=email]').bounding_box();bar=page.locator('.mobile-contact-bar').bounding_box();assert footer_mail['y']+footer_mail['height']<=bar['y'],f'Footer hidden at {width}'
  if width in [390,1440]:
   page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/f'business-{width}.png'),full_page=True)
 results.append('320/375/390/430/768/1024/1440px fit; mobile bar has 44px targets, hides over contact area and leaves footer accessible: PASS')
 page.goto(base+'/privacy#contact-privacy',wait_until='networkidle');assert page.locator('#contact-privacy').count()==1;assert work['contact']['email'] in page.locator('article').inner_text()
 assert not errors,errors
 results.append('Keyboard FAQ, inquiry privacy section, SEO title, one H1, no JavaScript exceptions: PASS')
 context.close()
 # Run the actual production-guarded tracker with local file responses and a
 # controlled GA script. Navigation is prevented ONLY in this test harness.
 ctx=browser.new_context(viewport={'width':1440,'height':1000});pg=ctx.new_page()
 def local_response(route):
  u=urllib.parse.urlsplit(route.request.url)
  if u.hostname=='neon-empanada-519607.netlify.app':
   path=PUBLIC/(urllib.parse.unquote(u.path).lstrip('/') or 'index.html')
   if u.path=='/privacy':path=PUBLIC/'privacy.html'
   if path.resolve().is_relative_to(PUBLIC.resolve()) and path.is_file():route.fulfill(path=str(path));return
  if u.hostname=='www.googletagmanager.com':route.fulfill(status=200,content_type='application/javascript',body='/* Test transport: GA dashboard receipt is not asserted. */');return
  route.abort()
 ctx.route('**/*',local_response);pg.goto(site['url'],wait_until='networkidle')
 pg.evaluate("document.addEventListener('click',e=>{if(e.target.closest('a'))e.preventDefault()},true)")
 pg.locator('#contact [data-contact-method=line]').click();pg.locator('#contact [data-contact-method=email]').click()
 pg.locator('.portfolio-card').first.click();pg.locator('#links .theme-card').first.click()
 pg.evaluate("document.querySelector('#approved-offers').insertAdjacentHTML('beforeend','<a id=offer-fixture href=\"https://example.com/product?private=test\" data-offer-id=fixture-product>Test fixture</a>')")
 pg.locator('#offer-fixture').click()
 events=pg.evaluate("(window.dataLayer||[]).map(x=>Array.from(x)).filter(x=>x[0]==='event')")
 assert [x[1] for x in events]==['contact_click','contact_click','portfolio_click','hub_link_click','hub_link_click'],events
 assert events[0][2]['contact_method']=='line' and events[1][2]['contact_method']=='email'
 assert events[2][2]['content_id']=='official-site';assert events[3][2]['content_id']=='note_ai';assert events[4][2]['content_id']=='fixture-product'
 encoded=json.dumps(events);assert work['contact']['email'] not in encoded and 'private=test' not in encoded and 'subject' not in encoded
 results.append('LINE/email, portfolio, original note and future offer events fire once with identifier-only parameters; no email address, message or query sent: PASS')
 results.append('GA4 property receipt, LINE message delivery and email delivery are not claimed; no messages were sent.')
 ctx.close();browser.close()
server.shutdown();(OUT/'business-browser.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print('\n'.join(results))
