from lib.utils.convertProofToPreset import removeXMLtags
import unittest

class TestRemoveXMLtags(unittest.TestCase):
    def test_base(self):
        """Base case"""
        taggedString = "<group>UC, lc, etc.</group>"
        cleanedString = removeXMLtags(taggedString, "group")
        expected = "UC, lc, etc."

        self.assertEqual(cleanedString, expected)

    def test_noClosingTag(self):
        """In case someone forgets to use a closing tag"""
        taggedString = "<group>Upper case<group>"

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
