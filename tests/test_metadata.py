import copy,hashlib,unittest
from pydantic import ValidationError
from case_studies.models import CaseRecord
from case_studies.metadata import validate_record

class MetadataIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.raw=b'fixture PDF bytes';digest=hashlib.sha256(self.raw).hexdigest()
        self.doc={'sha256':digest,'pages':[{'page':1,'text':'An energy company uses AI. Productivity improved 20%.'}]}
        self.source={'id':'fixture','case_pages':[1]}
        self.taxonomy={'version':'1.0','dimensions':{'industry':{'labels':['energy']}}}
        claim={'text':'Energy company uses AI.','evidence_ids':['a']}
        self.data={'case_id':'fixture','title':'Example','source_id':'fixture','pages':[1],
         'summaries':{x:claim for x in ('challenge','solution','outcome')},
         'observed_tags':[{'dimension':'industry','value':'energy','evidence_ids':['a']}],
         'evidence':{'a':{'source_id':'fixture','page':1,'quote':'energy company uses AI.'}},
         'classification_metadata':{'method':'assistant_curated','classifier':'fixture','classified_on':'2026-09-30','taxonomy_version':'1.0','source_sha256':digest}}
    def validate(self,data=None):
        return validate_record(CaseRecord.model_validate(data or self.data),self.source,self.doc,self.taxonomy,self.raw)
    def test_valid_evidence(self):self.assertEqual(self.validate(),1)
    def test_fabricated_quote(self):
        d=copy.deepcopy(self.data);d['evidence']['a']['quote']='90% improvement'
        with self.assertRaisesRegex(ValueError,'Evidence not found'):self.validate(d)
    def test_unknown_reference(self):
        d=copy.deepcopy(self.data);d['observed_tags'][0]['evidence_ids']=['missing']
        with self.assertRaises(ValidationError):self.validate(d)
    def test_cross_source_evidence(self):
        d=copy.deepcopy(self.data);d['evidence']['a']['source_id']='other'
        with self.assertRaises(ValidationError):self.validate(d)
    def test_unknown_tag(self):
        d=copy.deepcopy(self.data);d['observed_tags'][0]['value']='unregistered'
        with self.assertRaisesRegex(ValueError,'Unknown label'):self.validate(d)
    def test_changed_source(self):
        self.raw=b'changed bytes'
        with self.assertRaisesRegex(ValueError,'Source hash differs'):self.validate()
    def test_unselected_page(self):
        d=copy.deepcopy(self.data);d['evidence']['a']['page']=2
        with self.assertRaises(ValidationError):self.validate(d)
