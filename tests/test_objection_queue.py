import unittest
from vetobench.objection_queue import Job,serve

class QueueTests(unittest.TestCase):
 def test_duplicate_flood_and_distinct_target_evasion(self):
  legitimate=[Job('legit','target',1,True)]
  duplicates=[Job('d'+str(i),'decoy',1,False) for i in range(5)]
  unique=[Job('d'+str(i),'decoy'+str(i),1,False) for i in range(5)]
  self.assertNotIn('legit',serve(duplicates+legitimate,2,False)['served'])
  self.assertIn('legit',serve(duplicates+legitimate,2,True)['served'])
  self.assertNotIn('legit',serve(unique+legitimate,2,True)['served'])
 def test_same_key_different_cost_rejected(self):
  with self.assertRaises(ValueError):serve([Job('a','x',1,False),Job('b','x',2,True)],2,True)
