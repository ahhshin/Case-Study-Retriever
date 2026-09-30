import unittest
from case_studies.retrieval import RetrievalHarness
from case_studies.adapters import CallableAdapter

class RetrievalTests(unittest.TestCase):
    def ids(self,q):return [r['case_id'] for r in RetrievalHarness().search(q)['results']]
    def test_luxury(self):self.assertEqual(self.ids('find me a case study about luxury brands'),['burberry'])
    def test_sdlc(self):
        ids=self.ids('AI that accelerates software delivery')
        self.assertEqual(set(ids),{'sdlc_agent','sdlc_modernization','sdlc_energy'})
    def test_marketing(self):self.assertEqual(self.ids('AI marketing content generation'),['pharma_marketing'])
    def test_no_luxury_ai(self):self.assertEqual(self.ids('luxury brands using AI'),[])
    def test_unrelated(self):self.assertEqual(self.ids('underwater archaeology'),[])
    def test_input(self):
        with self.assertRaises(ValueError):RetrievalHarness().search(' ')
    def test_model_protocol(self):
        actions=iter([{'action':'read_case','case_id':'burberry'}, {'action':'final','selections':[{'case_id':'burberry','evidence_ids':['a']}]}])
        result=RetrievalHarness(CallableAdapter(lambda m:next(actions))).search('luxury')
        self.assertEqual(result['results'][0]['evidence'][0]['page'],48)
        self.assertEqual(len(result['trace']),2)
    def test_fabricated_model_evidence(self):
        actions=iter([{'action':'read_case','case_id':'burberry'}, {'action':'final','selections':[{'case_id':'burberry','evidence_ids':['made-up']}]}])
        with self.assertRaisesRegex(ValueError,'Unknown model evidence'):RetrievalHarness(CallableAdapter(lambda m:next(actions))).search('luxury')
    def test_unread_model_case(self):
        adapter=CallableAdapter(lambda m:{'action':'final','selections':[{'case_id':'burberry','evidence_ids':['a']}]})
        with self.assertRaisesRegex(ValueError,'must read'):RetrievalHarness(adapter).search('luxury')
    def test_model_budget(self):
        adapter=CallableAdapter(lambda m:{'action':'read_case','case_id':'burberry'})
        with self.assertRaisesRegex(RuntimeError,'budget'):RetrievalHarness(adapter,max_calls=2).search('luxury')
    def test_model_abstention(self):
        result=RetrievalHarness(CallableAdapter(lambda m:{'action':'final','selections':[]})).search('none')
        self.assertEqual(result['results'],[])
    def test_unselected_model_page(self):
        adapter=CallableAdapter(lambda m:{'action':'read_pages','source_id':'burberry','pages':[1]})
        with self.assertRaisesRegex(ValueError,'outside'):RetrievalHarness(adapter).search('luxury')
