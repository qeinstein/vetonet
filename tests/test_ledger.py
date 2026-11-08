import unittest
from dataclasses import replace
from vetobench.ledger import Action, Record, Verdict, evaluate

class LedgerTests(unittest.TestCase):
    def test_scope_freshness_and_conflict(self):
        action = Action('alice', 'write', 'record-1', 1, 2)
        positive = Record(action, 'registry', Verdict.ALLOW, 10)
        attack = Record(action, 'worker', Verdict.DENY, 10)
        trusted = {'registry'}
        self.assertEqual(evaluate(action, [positive, attack], trusted, 9), Verdict.ALLOW)
        self.assertEqual(evaluate(action, [positive], trusted, 10), Verdict.UNKNOWN)
        self.assertEqual(evaluate(replace(action, state_version=3), [positive], trusted, 9), Verdict.UNKNOWN)
        self.assertEqual(evaluate(action, [positive, replace(attack, source='registry')], trusted, 9), Verdict.UNKNOWN)
        self.assertEqual(evaluate(action, [attack], trusted, 9), Verdict.UNKNOWN)

if __name__ == '__main__':
    unittest.main()
