import unittest
from vetobench.parsing import parse
from vetobench.protocols import Decision as D

class ParsingTests(unittest.TestCase):
    def test_conservative_formats(self):
        self.assertEqual(parse('REPLY: REFUSE', 'anchored'), D.REFUSE)
        self.assertEqual(parse('REJECT', 'anchored'), D.REFUSE)
        self.assertEqual(parse('APPROVE.', 'anchored'), D.APPROVE)
        self.assertEqual(parse('APPROVE but actually REFUSE', 'anchored'), D.DEFER)
        self.assertEqual(parse('REPLY: APPROVE', 'strict'), D.DEFER)

if __name__ == '__main__':
    unittest.main()
