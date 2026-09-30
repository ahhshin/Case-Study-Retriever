"""Validate canonical case JSON against taxonomy and downloaded source evidence."""
import argparse, hashlib, json, re
from pathlib import Path
from .models import CaseRecord
from .pipeline import ROOT

def normalize(text):
    return re.sub(r'\s+', ' ', text).strip()

def validate_record(record, source, parsed, taxonomy, pdf_bytes):
    if record.source_id != source['id'] or record.pages != source['case_pages']:
        raise ValueError('Case boundaries differ from manifest')
    if record.classification_metadata.taxonomy_version != taxonomy['version']:
        raise ValueError('Taxonomy version differs')
    digest=hashlib.sha256(pdf_bytes).hexdigest()
    if digest != parsed['sha256'] or digest != record.classification_metadata.source_sha256:
        raise ValueError('Source hash differs; reparse and reclassify')
    pages={p['page']:normalize(p['text']) for p in parsed['pages']}
    for tag in record.observed_tags:
        if tag.value not in taxonomy['dimensions'][tag.dimension]['labels']:
            raise ValueError(f'Unknown label: {tag.dimension}/{tag.value}')
    for eid,evidence in record.evidence.items():
        if evidence.page not in pages or normalize(evidence.quote) not in pages[evidence.page]:
            raise ValueError(f'Evidence not found: {eid}')
    return len(record.evidence)

def build(root=ROOT):
    sources={s['id']:s for s in json.loads((root/'data/sources.json').read_text())}
    taxonomy=json.loads((root/'data/taxonomy.json').read_text())
    records=[];seen=set();evidence_count=0
    for path in sorted((root/'data/processed/cases').glob('*.json')):
        record=CaseRecord.model_validate_json(path.read_text())
        if record.case_id in seen:raise ValueError('Duplicate case ID')
        seen.add(record.case_id)
        source=sources[record.source_id]
        parsed=json.loads((root/'data/parsed'/f'{record.source_id}.json').read_text())
        evidence_count+=validate_record(record,source,parsed,taxonomy,(root/'data/raw'/f'{record.source_id}.pdf').read_bytes())
        records.append(record)
    if {r.source_id for r in records} != set(sources):
        raise ValueError('Corpus records must cover all manifest sources')
    catalogue=[]
    for r in records:
        s=sources[r.source_id];tags={}
        for t in r.observed_tags:tags.setdefault(t.dimension,[]).append(t.value)
        catalogue.append({'case_id':r.case_id,'title':r.title,'source_id':r.source_id,
                          'source_url':s['source_url'],'pages':r.pages,'observed_tags':tags,
                          'inferred_retrieval_concepts':r.inferred_retrieval_concepts,
                          'summary':' '.join(x.text for x in r.summaries.values()),
                          'metric_count':len(r.proof_points),'limitations':r.limitations,
                          'review_status':r.review_status,'record_path':f'data/processed/cases/{r.case_id}.json'})
    report={'status':'passed','records':len(records),'tags':sum(len(r.observed_tags) for r in records),
            'proof_points':sum(len(r.proof_points) for r in records),'evidence_fragments':evidence_count,
            'checks':['typed schema','taxonomy labels','evidence references','selected page boundaries','quote presence','source hashes','corpus coverage'],
            'semantic_review':'assistant-curated draft; independent human review pending'}
    (root/'data/processed/catalogue.json').write_text(json.dumps(catalogue,ensure_ascii=False,indent=2)+'\n')
    (root/'data/processed/validation-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(build(),indent=2))
if __name__=='__main__':main()
