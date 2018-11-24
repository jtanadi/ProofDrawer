"""
Test importing JSON, editing group
"""

import os.path
import unittest
from proofPreset import ProofPreset, ProofGroup

class TestPresetGroup(unittest.TestCase):
    def setUp(self):
        currentDir = os.path.dirname(__file__)
        jsonPath = os.path.join(currentDir, "resources", "jsonExportTest.json")

        self.preset = ProofPreset()
        self.preset.importFromJSON(jsonPath)
    
    def test_baseEditGroup(self):
        self.preset.editGroup(0, {"typeSize": 14})
        actual = self.preset.groups[0]
        expected = {
            'name': 'UC',
            'typeSize': 14,
            'leading': 12,
            'print': True,
            'contents': ['ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        }

        self.assertEqual(actual, expected)
        

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
