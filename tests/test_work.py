import copy,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from render_work import render_work
class WorkTests(unittest.TestCase):
 def setUp(self):self.work=json.loads((ROOT/'config/work.json').read_text())
 def render(self,value):
  with patch('render_work.json.loads',return_value=value):return render_work(lambda name:'')
 def test_rejects_non_https_line(self):
  self.work['contact']['lineUrl']='http://lin.ee/W3766xA'
  with self.assertRaises(ValueError):self.render(self.work)
 def test_rejects_mail_header_injection(self):
  self.work['contact']['email']='owner@example.com\r\nBcc:other@example.com'
  with self.assertRaises(ValueError):self.render(self.work)
 def test_rejects_script_portfolio_url(self):
  self.work['portfolio'][0]['url']='javascript:alert(1)'
  with self.assertRaises(ValueError):self.render(self.work)
 def test_rejects_outside_screenshot(self):
  self.work['portfolio'][0]['image']='https://unverified.example/fake.png'
  with self.assertRaises(ValueError):self.render(self.work)
 def test_escapes_editor_content(self):
  self.work['about']['paragraphs']=['<script>alert(1)</script>']
  values,_,_=self.render(self.work)
  self.assertIn('&lt;script&gt;',values['ABOUT_PARAGRAPHS']);self.assertNotIn('<script>',values['WORK_SECTION'])
 def test_future_portfolio_without_screenshot(self):
  item=copy.deepcopy(self.work['portfolio'][0]);item.update(id='third-work',image='',imageAlt='');self.work['portfolio'].append(item)
  values,_,_=self.render(self.work);self.assertIn('data-portfolio-id="third-work"',values['PORTFOLIO'])
 def test_faq_schema_matches_visible_answers(self):
  values,work,schema=self.render(self.work)
  self.assertEqual([q['acceptedAnswer']['text'] for q in schema['mainEntity']],[f['answer'] for f in work['faqs']])
if __name__=='__main__':unittest.main()
