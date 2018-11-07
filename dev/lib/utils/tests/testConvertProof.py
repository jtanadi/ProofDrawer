from lib.utils.convertProofToPreset import removeXMLtags
import unittest

class TestRemoveXMLTags(unittest.TestCase):
    def test_base(self):
        taggedString = "<group>UC, lc, etc.</group>"
        cleanedString = removeXMLtags(taggedString, "group")
        expected = "UC, lc, etc."

        self.assertEqual(cleanedString, expected)
