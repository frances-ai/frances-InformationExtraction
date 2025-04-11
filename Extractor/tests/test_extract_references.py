import unittest
from Extractor.extractor import extract_see_references


class TestExtractReferences(unittest.TestCase):
    def test_text_simple(self):
        texts = ["COPINSHAY. See CUPINSHAY.", "a village in the stew. artrv of Kirkcudbright. See Castle Doug I las.' CARLINWARK (LOCH)",
                 "a district in Dumfri«i. shire, in the parish of Langholm. Vide LANGHOLM.", "a royal burgh in Haddingtonlhire. Vide Berwick (North)."]
        expected = [
            ["CUPINSHAY"],
            [],
            ["LANGHOLM"],
            ["Berwick (North)"]
        ]
        for text, expected in zip(texts, expected):
            self.assertEqual(expected, extract_see_references(text))

    def test_text_multiple_refs(self):
        texts = ["LOGIE WESTER. Vide URQUHART and LOGIE WESTER.", "Papastour, and Fowla. See WALLS and SANDNESS."]
        expected = [
            ["URQUHART", "LOGIE WESTER"],
            ["WALLS", "SANDNESS"],
        ]
        for text, expected in zip(texts, expected):
            self.assertEqual(expected, extract_see_references(text))
