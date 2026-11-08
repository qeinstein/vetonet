import unittest
from vetobench.protocols import Decision as D, Evidence, execute


class ProtocolTests(unittest.TestCase):
    def test_false_veto_and_verified_recovery(self):
        votes = [D.APPROVE, D.REFUSE]
        positive = Evidence(True, True)
        self.assertFalse(execute('veto', votes, positive))
        self.assertTrue(execute('evidence_escalation', votes, positive))
        self.assertTrue(execute('evidence_gate', votes, positive))

    def test_unknown_or_invalid_evidence_does_not_authorize(self):
        for evidence in (Evidence(None, True), Evidence(True, False), Evidence(False, True)):
            self.assertFalse(execute('evidence_escalation', [D.APPROVE], evidence))
            self.assertFalse(execute('evidence_gate', [D.APPROVE], evidence))

    def test_retry_can_reverse_a_refusal(self):
        votes = [D.REFUSE, D.APPROVE]
        self.assertTrue(execute('retry', votes, Evidence(None, False)))
        self.assertFalse(execute('veto', votes, Evidence(None, False)))


if __name__ == '__main__':
    unittest.main()
