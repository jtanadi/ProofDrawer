from proofPreset.proofPreset import ProofPreset
import unittest

class TestImportExport(unittest.TestCase):
    def setUp(self):
        self.testPreset = ProofPreset("testPreset")

    def test_addGroup(self):
        groupToAdd = {"name": "new test", "contents": "abcde"}
        expectedPreset = {
            "name": "testPreset",
            "groups": [groupToAdd]
        }
        self.testPreset.addGroup(groupToAdd)

        actual = self.testPreset.getPreset()

        self.assertEqual(expectedPreset, actual)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
