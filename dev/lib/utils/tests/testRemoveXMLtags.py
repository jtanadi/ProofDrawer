from lib.utils.convertProofToPreset import removeXMLtags, XMLtagError
import unittest

class TestRemoveXMLtags(unittest.TestCase):
    def test_base(self):
        """
        Base case
        """
        taggedString = "<group>UC, lc, etc.</group>"
        cleanedString = removeXMLtags(taggedString, "group")
        expected = "UC, lc, etc."

        self.assertEqual(cleanedString, expected)

    def test_noClosingTag1(self):
        """
        In case someone uses open tag as close tag
        The function should disregard tags and not do anything
        """
        taggedString = "<group>Upper case<group>"
        with self.assertRaises(XMLtagError):
            removeXMLtags(taggedString, "group")

    def test_noClosingTag2(self):
        """
        In case someone forgets to use a closing tag
        The function should disregard tags and not do anything
        """
        taggedString = "<group>Upper case"
        with self.assertRaises(XMLtagError):
            removeXMLtags(taggedString, "group")

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
