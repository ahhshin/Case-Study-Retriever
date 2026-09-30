"""Reproducible PDF ingestion. No model calls or retrieval engine yet."""
import argparse, concurrent.futures, hashlib, json, subprocess, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def ingest(source, force=False):
    for directory in ('raw','parsed'):
        (ROOT / 'data' / directory).mkdir(parents=True, exist_ok=True)
    sid = source['id']
    pdf = ROOT / 'data/raw' / f'{sid}.pdf'
    if force or not pdf.exists():
        req = urllib.request.Request(source['source_url'], headers={'User-Agent':'CaseStudyPrototype/0.1'})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read(50*1024*1024 + 1)
        if len(data)>50*1024*1024 or not data.startswith(b'%PDF-'):
            raise ValueError('Not a PDF or exceeds 50 MiB')
        pdf.write_bytes(data)
    text = subprocess.run(['pdftotext','-layout',str(pdf),'-'],check=True,capture_output=True,text=True).stdout
    pages = text.split('\f')
    if pages and not pages[-1].strip(): pages.pop()
    parsed = {'source':source,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
              'pages':[{'page':i,'text':t.strip(),'needs_visual_review':len(t.strip())<80} for i,t in enumerate(pages,1)]}
    out = ROOT/'data/parsed'
    (out/f'{sid}.json').write_text(json.dumps(parsed,ensure_ascii=False,indent=2))
    (out/f'{sid}.md').write_text(f"# {source['title']}\n\nSource: {source['source_url']}\n\n"+'\n\n'.join(f"## Page {p['page']}\n\n```text\n{p['text']}\n```" for p in parsed['pages']))
    (out/f'{sid}.txt').write_text('\n\n'.join(f"[Page {p['page']}]\n{p['text']}" for p in parsed['pages']))
    return {'id':sid,'status':'parsed','pages':len(pages),'characters':sum(len(p['text']) for p in parsed['pages']),'sha256':parsed['sha256']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--force',action='store_true');args=ap.parse_args()
    sources=json.loads((ROOT/'data/sources.json').read_text())
    def run(s):
        try:return ingest(s,args.force)
        except Exception as exc:return {'id':s['id'],'status':'failed','error':str(exc)}
    results=list(concurrent.futures.ThreadPoolExecutor(5).map(run,sources))
    (ROOT/'data/ingestion-report.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
    if any(r['status']=='failed' for r in results):raise SystemExit(1)
if __name__=='__main__':main()
