import unittest
from Extractor.extractor import extract_names


class TestExtractNames(unittest.TestCase):
    def test_text_single_name(self):
        texts = ["ABBAY(ST.BATHANS)", "ABBEY-GREEN", "ABB'S (ST. HEAD", "ABERNETHY & KINCARDINE"]
        for index, text in enumerate(texts):
            name, alters = extract_names(text)
            expected_name = text
            expected_alters = []
            self.assertEqual(expected_name, name)
            self.assertEqual(expected_alters, alters)

    def test_text_with_or_simple(self):
        texts = ["BAMFF, OR BANFF", "ARDMEANACH, OR BLACK ISLE", "BERVIE BROW, OR CRAIG DAVID", "INVERARAY, OR INVERARY IN GAELIC, ION-AR-AO-REIDH",
                 "LONG, OR LOUNG (LOCH)", "JOHN'S (ST., OR ST. JOHN'S CLAUCHAN"]
        expected_results = [
            {"name": "BAMFF", "alters": ["BANFF"]},
            {"name": "ARDMEANACH", "alters": ["BLACK ISLE"]},
            {"name": "BERVIE BROW", "alters": ["CRAIG DAVID"]},
            {"name": "INVERARAY", "alters": ["INVERARY IN GAELIC, ION-AR-AO-REIDH"]},
            {"name": "LONG", "alters": ["LOUNG (LOCH)"]},
            {"name": "JOHN'S (ST.", "alters": ["ST. JOHN'S CLAUCHAN"]},
        ]
        for index, text in enumerate(texts):
            name, alters = extract_names(text)
            expected_name = expected_results[index]["name"]
            expected_alters = expected_results[index]["alters"]
            self.assertEqual(expected_name, name)
            self.assertEqual(expected_alters, alters)

    def test_text_with_or_multiple_names(self):
        texts = ["CAMBRAY, CUMBRAY, OR CIMBRAES", "HEBRIDES, HEBUD7E, 2EBU DI E, OR THE WESTERN ISLES", "ILA, ILAY, ISLA, OR ISLAY"]
        expected_results = [
            {"name": "CAMBRAY", "alters": ["CUMBRAY", "CIMBRAES"]},
            {"name": "HEBRIDES", "alters": ["HEBUD7E", "2EBU DI E", "THE WESTERN ISLES"]},
            {"name": "ILA", "alters": ["ILAY", "ISLA", "ISLAY"]},]
        for index, text in enumerate(texts):
            name, alters = extract_names(text)
            expected_name = expected_results[index]["name"]
            expected_alters = expected_results[index]["alters"]
            self.assertEqual(expected_name, name)
            self.assertEqual(expected_alters, alters)

    def test_text_with_post_or_extra(self):
        texts = ["I R O N G R AY, OR MORE PROPERLY KIRKPATRICK-IRONGRAY"]
        expected_results = [
            {"name": "I R O N G R AY", "alters": ["KIRKPATRICK-IRONGRAY"]}]
        for index, text in enumerate(texts):
            name, alters = extract_names(text)
            expected_name = expected_results[index]["name"]
            expected_alters = expected_results[index]["alters"]
            self.assertEqual(expected_name, name)
            self.assertEqual(expected_alters, alters)


    def test_text_with_or_embedded_parentheses(self):
        texts = ["KILPATRICK ( OLD, OR WEST)", "KINTYRE (MAOIL, OR MULL OF)", "CAMBRAY (LITTLE OR LESSER)"]
        expected_results = [
            {"name": "KILPATRICK OLD", "alters": ["KILPATRICK WEST"]},
            {"name": "KINTYRE MAOIL", "alters": ["KINTYRE MULL OF"]},
            {"name": "CAMBRAY LITTLE", "alters": ["CAMBRAY LESSER"]}]
        for index, text in enumerate(texts):
            name, alters = extract_names(text)
            expected_name = expected_results[index]["name"]
            expected_alters = expected_results[index]["alters"]
            self.assertEqual(expected_name, name)
            self.assertEqual(expected_alters, alters)


    def test_text_with_other_indicators(self):
        texts = ["MILNATHORT, VULGARLY CALLED MILLS OF FORTH", "STRATHNAIRN, OTHERWISE THE COUNTY OF NAIRN", "AVENDALE, OTHERWISE CALLED STRATHAVEN",
                 "MONANCE (ST., FORMERLY NAMED ABERCROMBIE", "TRAQUA1R (PORE PROPERLY STRATHQUAIR)"]
        expected_results = [
            {"name": "MILNATHORT", "alters": ["MILLS OF FORTH"]},
            {"name": "STRATHNAIRN", "alters": ["THE COUNTY OF NAIRN"]},
            {"name": "AVENDALE", "alters": ["STRATHAVEN"]},
            {"name": "MONANCE (ST.", "alters": ["ABERCROMBIE"]},
            {"name": "TRAQUA1R", "alters": ["STRATHQUAIR"]},]
        for index, text in enumerate(texts):
            name, alters = extract_names(text)
            expected_name = expected_results[index]["name"]
            expected_alters = expected_results[index]["alters"]
            self.assertEqual(expected_name, name)
            self.assertEqual(expected_alters, alters)








