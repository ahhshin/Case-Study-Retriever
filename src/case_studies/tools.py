"""Small, bounded evidence tools for a future model-driven harness."""
import json
from .pipeline import ROOT

def list_cases():
    return json.loads((ROOT/'data/case-catalogue.json').read_text())

def read_pages(source_id: str, pages: list[int], max_characters: int = 16000):
    sources={s['id'] for s in json.loads((ROOT/'data/sources.json').read_text())}
    if source_id not in sources: raise ValueError('Unknown source')
    if not 1<=len(pages)<=5: raise ValueError('Request 1–5 pages')
    if not 1<=max_characters<=32000: raise ValueError('Invalid output budget')
    doc=json.loads((ROOT/'data/parsed'/f'{source_id}.json').read_text())
    indexed={p['page']:p for p in doc['pages']}
    if any(p not in indexed for p in pages): raise ValueError('Unknown page')
    result=[];remaining=max_characters
    for n in pages:
        p=indexed[n];t=p['text'][:remaining]
        result.append({'source_id':source_id,'page':n,'text':t,'truncated':len(t)<len(p['text']),
                       'source_url':doc['source']['source_url']+f'#page={n}'})
        remaining-=len(t)
    return result

def verify_evidence(source_id: str, page: int, quote: str):
    import re
    if not quote.strip(): return False
    normalize=lambda x: re.sub(r'\s+',' ',x).strip()
    return normalize(quote) in normalize(read_pages(source_id,[page],32000)[0]['text'])
