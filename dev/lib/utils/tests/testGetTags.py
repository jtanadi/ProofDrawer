from lib.utils.convertProofToPreset import getTags, XMLtagError
import unittest

class TestGetTags(unittest.TestCase):
    def test_base(self):
        """
        Base test
        """
        inputList = ["<group>", "UC, lc, numerals", "</group>", "<group>", "control chars", "</group>"]
        expected= ["<group>", "</group>", "<group>", "</group>"]
        self.assertEqual(getTags(inputList, "group"), expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
