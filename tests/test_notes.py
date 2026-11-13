import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from update_notes import parse_rss, update, valid_profile
from build import remote_url
URL='https://note.com/crisp_auk8183'
def rss(name='変更後の表示名',url=URL):
    return f'''<rss><channel><title>{name}</title><link>{url}</link><item><title>実在テスト記事</title><link>{url}/n/nabc123</link><pubDate>Fri, 13 Nov 2026 12:00:00 +0900</pubDate></item></channel></rss>'''.encode()
class NotesTests(unittest.TestCase):
    def setUp(self):
        self.config={'notes':[{'url':URL,'category':'AI・テクノロジー'}]}
        self.previous={'notes':[{'url':URL,'displayName':'以前の表示名','fetchedAt':'2026-11-12T00:00:00+00:00','articles':[{'title':'前回の記事'}],'status':'ok'}]}
    def test_current_rss_name(self):
        name, articles=parse_rss(rss(),URL)
        self.assertEqual(name,'変更後の表示名');self.assertEqual(len(articles),1)
    def test_name_change_replaces_cached_name(self):
        result=update(self.config,self.previous,lambda _:rss())
        self.assertEqual(result['notes'][0]['displayName'],'変更後の表示名')
    def test_network_failure_preserves_previous_data(self):
        def fail(_):raise TimeoutError()
        result=update(self.config,self.previous,fail)['notes'][0]
        self.assertEqual(result['displayName'],'以前の表示名');self.assertEqual(result['articles'],self.previous['notes'][0]['articles']);self.assertEqual(result['fetchedAt'],self.previous['notes'][0]['fetchedAt']);self.assertEqual(result['status'],'cached')
    def test_first_failure_has_generic_fallback(self):
        result=update(self.config,{},lambda _:b'invalid')['notes'][0]
        self.assertEqual(result['displayName'],'AI・テクノロジーのnote');self.assertEqual(result['articles'],[]);self.assertEqual(result['status'],'fallback')
    def test_wrong_account_rejected(self):
        with self.assertRaises(ValueError):parse_rss(rss(url='https://note.com/another'),URL)
    def test_blank_name_preserves_previous(self):
        result=update(self.config,self.previous,lambda _:rss(name=' '))['notes'][0]
        self.assertEqual(result['displayName'],'以前の表示名')
    def test_other_account_articles_rejected(self):
        raw=rss().replace((URL+'/n/').encode(),b'https://note.com/another/n/')
        self.assertEqual(parse_rss(raw,URL)[1],[])
    def test_dtd_rejected(self):
        with self.assertRaises(ValueError):parse_rss(b'<!DOCTYPE rss>'+rss(),URL)
    def test_fifth_account_needs_only_url_and_category(self):
        config=copy.deepcopy(self.config);config['notes'].append({'url':'https://note.com/new_account','category':'新しいテーマ'})
        result=update(config,{},lambda url:rss(url=url))
        self.assertEqual(len(result['notes']),2);self.assertEqual(result['notes'][1]['status'],'ok')
    def test_partial_failure_does_not_affect_other_account(self):
        config=copy.deepcopy(self.config);config['notes'].append({'url':'https://note.com/second','category':'第二テーマ'})
        result=update(config,self.previous,lambda url:rss(url=url) if url.endswith('second') else b'broken')
        self.assertEqual([n['status'] for n in result['notes']],['cached','ok'])
    def test_profile_url_validation(self):
        for url in ['http://note.com/a','https://note.com.evil/a','https://note.com/a?x=1','https://note.com/a/b']:
            self.assertFalse(valid_profile(url))
    def test_remote_source_auto_configuration(self):
        with patch.dict('os.environ',{'REPOSITORY_URL':'https://github.com/owner/project.git'}):
            self.assertEqual(remote_url({}),'https://raw.githubusercontent.com/owner/project/HEAD/data/notes.json')
    def test_remote_url_validation(self):
        with self.assertRaises(ValueError):remote_url({'remoteDataUrl':'https://untrusted.example/data/notes.json'})
    def test_real_snapshot_contains_four_names(self):
        data=json.loads((ROOT/'data/notes.json').read_text());self.assertEqual(len(data['notes']),4)
        self.assertTrue(all(n['displayName'] and n['fetchedAt'] and n['articles'] for n in data['notes']))
if __name__=='__main__':unittest.main()
