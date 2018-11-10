"""
Test helper functions
"""

import utils.helperFunctions as hf
import unittest

class TestHelperFunctions(unittest.TestCase):
    def setUp(self):
        self.inputList = [
            {
                "key1": "key1Val1",
                "key2": "key2Val1",
                "key3": "key3Val1",
                "key4": "key4Val1"
            },
            {
                "key1": "key1Val2",
                "key2": "key2Val2",
                "key3": "key3Val2",
                "key4": "key4Val2"
            },
            {
                "key1": "key1Val3",
                "key2": "key2Val3",
                "key3": "key3Val3",
                "key4": "key4Val3"
            }
        ]

    def test_baseGetValuesFromListOfDicts(self):
        """
        Base case for hf.getValuesFromListOfDicts()
        """
        actual = hf.getValuesFromListOfDicts(self.inputList, "key1")
        expected = ["key1Val1", "key1Val2", "key1Val3"]

        self.assertEqual(actual, expected)

    def test_baseConvertToListOfPyDicts(self):
        """
        Base case for hf.convertToListOfPyDicts()
        """
        actual = hf.convertToListOfPyDicts(self.inputList)
        expected = [
            {
                "key1": "key1Val1",
                "key2": "key2Val1",
                "key3": "key3Val1",
                "key4": "key4Val1"
            },
            {
                "key1": "key1Val2",
                "key2": "key2Val2",
                "key3": "key3Val2",
                "key4": "key4Val2"
            },
            {
                "key1": "key1Val3",
                "key2": "key2Val3",
                "key3": "key3Val3",
                "key4": "key4Val3"
            }
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
