import unittest
from vetobench.allocation import Candidate, allocate

class AllocationTests(unittest.TestCase):
    def test_cost_and_determinism(self):
        cases=[Candidate('a',1,.5,.8,2,0), Candidate('b',.2,.8,.9,1,1), Candidate('c',.9,.4,.5,1,2)]
        for strategy in ('fifo','random','risk','evidence_aware'):
            ids=allocate(cases,2,strategy,4)
            self.assertLessEqual(sum(c.cost for c in cases if c.case_id in ids),2)
            self.assertEqual(ids,allocate(cases,2,strategy,4))
        self.assertEqual(allocate(cases,0,'fifo'),[])
    def test_no_oracle_inputs(self):
        self.assertNotIn('authorized',Candidate.__dataclass_fields__)
        with self.assertRaises(ValueError): allocate([Candidate('x',1,1,1,0,0)],1,'fifo')
