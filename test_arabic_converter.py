import unittest
from arabic_converter import ArabicConverter, read_file
import tempfile
import os

class TestArabicConverter(unittest.TestCase):
    def setUp(self):
        self.converter = ArabicConverter()

    def test_convert_simple_word(self):
        input_text = "بسم"
        expected = "2 12 24"
        result = self.converter.convert_arabic_to_numbers(input_text)
        self.assertEqual(expected, result.strip())

    def test_convert_word_with_diacritics(self):
        input_text = "بِسْمِ"
        expected = "2(6)12(8)24(6)"
        result = self.converter.convert_arabic_to_numbers(input_text)
        self.assertEqual(expected, result.strip())

    def test_convert_multiple_lines(self):
        input_text = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ\nالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"
        expected = "2(6)12(8)24(6) 1 23(7)23 26(6) 1 23 10(7)6(8)24 25(6) 1 23 10(7)6(6)28 24(6)\n1 23(8)6 24(8)8(5) 23(6)23(7)26(6) 10 2(7) 1 23(8)18 1 23 24(6)28 25(6)"
        result = self.converter.convert_arabic_to_numbers(input_text)
        self.assertEqual(expected, result.strip())

    def test_read_txt_file(self):
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp:
            temp.write("بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ")
            temp_name = temp.name
        
        content = read_file(temp_name)
        self.assertEqual("بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", content)
        
        os.unlink(temp_name)

    # Add more tests for XML and SQL files...

if __name__ == '__main__':
    unittest.main()
