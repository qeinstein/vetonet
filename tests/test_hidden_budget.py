import unittest
from vetobench.hidden_budget import coordinate
from vetobench.evidence_service import EvidenceService,GrantRecord

class HiddenBudgetTests(unittest.TestCase):
 def test_allocator_never_receives_truth_and_query_is_charged(self):
  c=dict(id='x',principal='p',resource='r',operation='write',state_version=2,risk=.5,cost=1,source_reliability=.9,compromised_draw=.1,request='q',worker='DEFER',critic='DEFER')
  service=EvidenceService({'x':GrantRecord('p','r','write',2,True,'registry')},set())
  self.assertFalse(coordinate([c],service,0,'fifo')[0]['executed'])
  self.assertTrue(coordinate([c],service,1,'fifo')[0]['executed'])
  with self.assertRaises(ValueError): coordinate([{**c,'authorized':True}],service,1,'fifo')
