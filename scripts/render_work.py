"""Render the static business sections without adding a server or external API."""
import html,json,re
from pathlib import Path
from urllib.parse import urlencode,urlsplit
ROOT=Path(__file__).resolve().parents[1]
def esc(value):return html.escape(str(value),quote=True)
def replace(template,values):
    for key,value in values.items():template=template.replace('{{'+key+'}}',value)
    if '{{' in template:raise ValueError('Unfilled work template')
    return template

def render_work(icon):
    work=json.loads((ROOT/'config/work.json').read_text())
    contact=work['contact']
    url=urlsplit(contact['lineUrl'])
    if url.scheme!='https' or url.netloc!='lin.ee' or not re.fullmatch(r'/[A-Za-z0-9]+',url.path) or url.query or url.fragment:raise ValueError('Invalid LINE link')
    if not re.fullmatch(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}',contact['email']):raise ValueError('Invalid contact email')
    mail='mailto:'+contact['email']+'?'+urlencode({'subject':'Webサイトからのお問い合わせ'})
    values={'LINE_URL':esc(contact['lineUrl']),'LINE_NAME':esc(contact['lineName']),'LINE_ID':esc(contact['lineId']),'EMAIL_URL':esc(mail),'EMAIL':esc(contact['email']),'CONTACT_HEADING':esc(contact['heading']),'CONTACT_DESCRIPTION':esc(contact['description']),'ABOUT_PARAGRAPHS':''.join('<p>'+esc(p)+'</p>' for p in work['about']['paragraphs']),'ACTIVITIES':''.join('<li>'+esc(s)+'</li>' for s in work['about']['activities'])}
    services=[]
    for i,s in enumerate(work['services']):
        services.append('<article class="service-card"><div class="service-top"><span class="service-icon">'+icon(s['symbol'])+'</span><span>'+f'{i+1:02}'+'</span></div><h3>'+esc(s['title'])+'</h3><p>'+esc(s['description'])+'</p></article>')
    portfolios=[]
    for item in work['portfolio']:
        u=urlsplit(item['url'])
        if u.scheme!='https' or not u.netloc or u.username or u.password:raise ValueError('Invalid portfolio URL')
        if not re.fullmatch(r'[a-z0-9-]{1,70}',item['id']):raise ValueError('Invalid portfolio identifier')
        image=item.get('image','')
        if image and (not re.fullmatch(r'/images/[a-z0-9-]+\.(jpg|png|webp)',image) or not (ROOT/'public'/image.lstrip('/')).is_file()):raise ValueError('Portfolio image missing or invalid')
        photo='<img src="'+esc(image)+'" alt="'+esc(item['imageAlt'])+'" width="1200" height="760" loading="lazy" decoding="async">' if image else ''
        body=photo+'<div class="portfolio-body"><span class="work-label">自主制作・公開作品</span><h3>'+esc(item['name'])+'</h3><p class="portfolio-subtitle">'+esc(item['subtitle'])+'</p><p>'+esc(item['description'])+'</p><p class="portfolio-purpose"><b>制作の目的</b>'+esc(item['purpose'])+'</p><ul class="technology-list" aria-label="確認できた使用技術">'+''.join('<li>'+esc(t)+'</li>' for t in item['technologies'])+'</ul><span class="card-link">公開ページを開く <span aria-hidden="true">↗</span></span></div>'
        portfolios.append('<a class="portfolio-card" href="'+esc(item['url'])+'" data-portfolio-id="'+esc(item['id'])+'" target="_blank" rel="noopener noreferrer">'+body+'</a>')
    steps=[]
    for i,s in enumerate(work['steps']):steps.append('<li><span class="step-number">STEP '+str(i+1)+'</span><h3>'+esc(s['title'])+'</h3><p>'+esc(s['description'])+'</p></li>')
    faqs=['<details class="faq-item"><summary><span aria-hidden="true">Q.</span>'+esc(f['question'])+'</summary><p>'+esc(f['answer'])+'</p></details>' for f in work['faqs']]
    values.update({'SERVICES':''.join(services),'PORTFOLIO':''.join(portfolios),'STEPS':''.join(steps),'FAQS':''.join(faqs)})
    values['CONTACT_SECTION']=replace((ROOT/'templates/work-contact.html').read_text(),values)
    values['WORK_SECTION']=replace((ROOT/'templates/work-content.html').read_text(),values)
    faq_schema={'@type':'FAQPage','mainEntity':[{'@type':'Question','name':f['question'],'acceptedAnswer':{'@type':'Answer','text':f['answer']}} for f in work['faqs']]}
    return values,work,faq_schema
