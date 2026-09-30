"""Loopback-only GUI/API. Provider credentials stay in the adapter process."""
import argparse,json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from .pipeline import ROOT
from .retrieval import RetrievalHarness,load_adapter

def make_handler(harness):
    class Handler(BaseHTTPRequestHandler):
        def send(self,status,data,content_type='application/json'):
            body=data if isinstance(data,bytes) else json.dumps(data).encode()
            self.send_response(status);self.send_header('Content-Type',content_type)
            self.send_header('Content-Length',str(len(body)));self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
        def do_GET(self):
            if self.path=='/':self.send(200,(ROOT/'web/index.html').read_bytes(),'text/html; charset=utf-8')
            elif self.path=='/api/status':self.send(200,{'mode':'model' if harness.adapter else 'metadata'})
            else:self.send(404,{'error':'Not found'})
        def do_POST(self):
            if self.path!='/api/search':return self.send(404,{'error':'Not found'})
            # Reject cross-origin browser calls to a credential-bearing local process.
            origin=self.headers.get('Origin')
            expected=f'http://{self.headers.get("Host")}'
            if origin and origin!=expected:return self.send(403,{'error':'Cross-origin request rejected'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 1<=length<=10000:raise ValueError('Invalid request size')
                data=json.loads(self.rfile.read(length))
                result=harness.search(data.get('query'),data.get('limit',3));self.send(200,result)
            except (ValueError,TypeError) as e:self.send(400,{'error':str(e)})
            except Exception:self.send(502,{'error':'Search failed. Check the server console or adapter configuration.'})
    return Handler

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);p.add_argument('--adapter')
    a=p.parse_args();h=RetrievalHarness(load_adapter(a.adapter) if a.adapter else None)
    print(f'Case search: http://127.0.0.1:{a.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',a.port),make_handler(h)).serve_forever()
if __name__=='__main__':main()
