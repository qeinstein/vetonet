import unittest
from vetobench.budget_eval import run

class BudgetTests(unittest.TestCase):
 def test_monitor_fails_closed_and_budget_charged_for_unavailable(self):
  cs=[dict(id='a',worker='APPROVE',critic='REFUSE',retry='APPROVE',risk=.5,source_reliability=.8,cost=1,compromised_draw=.1,authorized=True,source_available=False),
      dict(id='b',worker='APPROVE',critic='REFUSE',retry='APPROVE',risk=.5,source_reliability=.8,cost=1,compromised_draw=.1,authorized=False,source_available=True)]
  out=run(cs,1,1,'gate_fifo')
  self.assertTrue(out[0]['queried']); self.assertFalse(out[0]['executed']);self.assertFalse(out[1]['queried']);self.assertFalse(out[1]['executed'])
  self.assertFalse(any(x['executed'] for x in run(cs,2,1,'evidence_aware')))
