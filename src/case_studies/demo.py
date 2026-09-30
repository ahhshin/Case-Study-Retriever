"""Build a standalone browser demo from the canonical metadata and ranking config."""
import json
from .pipeline import ROOT
from .tools import list_cases,read_case
from .retrieval import STOP,ALIASES

def main():
    data=[dict(c,record=read_case(c['case_id'])) for c in list_cases()]
    def safe(x):return json.dumps(x,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    text=(ROOT/'web/index.html').read_text().replace('const EMBEDDED = null;',f'const EMBEDDED = {safe(data)};').replace('const CONFIG = null;',f'const CONFIG = {safe({"stop":sorted(STOP),"aliases":ALIASES})};')
    (ROOT/'web/demo.html').write_text(text)
    print(ROOT/'web/demo.html')
if __name__=='__main__':main()
