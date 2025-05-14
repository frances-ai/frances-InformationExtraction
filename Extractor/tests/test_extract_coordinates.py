import unittest
from Extractor.extractor import extract_coordinates


class TestExtractCoordinates(unittest.TestCase):
    def test_text_simple(self):
        texts = [".... are also made. Long. 10.31. 25. E. Lat. 47. 53.10. N.",
                 "... of Scanderoon. Lat. 36° 56' N.; Long. 36° 25' E.",
                 "other goods. Long. 104. 5. E. Lat. 1. 40. N.",
                 "and 5690 inhabitants. Lat. 51° 25\\\' 6\", and Long. 7° 35\\\' 22\" E."
                 ]
        expected = [
            (47.88611111111111, 10.523611111111112),
            (36.93333333333333, 36.416666666666664),
            (1.6666666666666665, 104.08333333333333),
        ]
        for text, expected in zip(texts, expected):
            self.assertAlmostEqual(expected[0], extract_coordinates(text)[0])
            self.assertAlmostEqual(expected[1], extract_coordinates(text)[1])

