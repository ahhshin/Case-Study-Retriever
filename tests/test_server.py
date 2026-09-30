import json,threading,unittest
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from case_studies.server import make_handler
from case_studies.retrieval import RetrievalHarness

class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(RetrievalHarness()))
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def test_page_and_query(self):
        with urlopen(self.url) as r:self.assertIn(b'id="query"',r.read())
        req=Request(self.url+'/api/search',data=json.dumps({'query':'luxury brands'}).encode(),headers={'Content-Type':'application/json'})
        with urlopen(req) as r:self.assertEqual(json.load(r)['results'][0]['case_id'],'burberry')
    def test_invalid_query(self):
        req=Request(self.url+'/api/search',data=b'{"query":""}',headers={'Content-Type':'application/json'})
        with self.assertRaises(HTTPError) as e:urlopen(req)
        self.assertEqual(e.exception.code,400)
    def test_cross_origin(self):
        req=Request(self.url+'/api/search',data=b'{"query":"luxury"}',headers={'Content-Type':'application/json','Origin':'https://example.com'})
        with self.assertRaises(HTTPError) as e:urlopen(req)
        self.assertEqual(e.exception.code,403)
