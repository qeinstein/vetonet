import unittest
from dataclasses import replace
from vetobench.evidence_service import Request,GrantRecord,EvidenceService,monitor

class EvidenceServiceTests(unittest.TestCase):
 def test_no_evidence_stale_wrong_scope_or_issuer(self):
  request=Request('p','r','write',2);record=GrantRecord('p','r','write',2,True,'registry')
  service=EvidenceService({'x':record},{'offline'})
  self.assertTrue(monitor(request,service.lookup('x'),{'registry'}))
  self.assertFalse(monitor(request,service.lookup('offline'),{'registry'}))
  for bad in (replace(record,state_version=1),replace(record,issuer='attacker'),replace(record,resource='other'),replace(record,allowed=False)):
   self.assertFalse(monitor(request,bad,{'registry'}))
