from proofPreset.proofPreset import ProofPreset
import unittest

class TestImportExport(unittest.TestCase):
    def setUp(self):
        self.testPreset = ProofPreset("testPreset")

    def test_addGroup(self):
        groupToAdd = {"name": "new test", "contents": "abcde"}
        self.testPreset.addGroup(groupToAdd)

        expected = self.testPreset.getGroups()

        self.assertIn(groupToAdd, expected)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
