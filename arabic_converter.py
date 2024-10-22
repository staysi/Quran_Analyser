import re
import xml.etree.ElementTree as ET
import os

class ArabicConverter:
    def __init__(self):
        # Initialize dictionaries for Arabic letters and diacritical marks
        self.arabic_letter_map = {
            'ا': 1, 'ب': 2, 'ت': 3, 'ث': 4, 'ج': 5, 'ح': 6, 'خ': 7, 'د': 8, 'ذ': 9, 'ر': 10,
            'ز': 11, 'س': 12, 'ش': 13, 'ص': 14, 'ض': 15, 'ط': 16, 'ظ': 17, 'ع': 18, 'غ': 19, 'ف': 20,
            'ق': 21, 'ك': 22, 'ل': 23, 'م': 24, 'ن': 25, 'ه': 26, 'و': 27, 'ي': 28, 'ء': 29, 'ى': 30,
            'آ': 31, 'ة': 32, 'ؤ': 33, 'ئ': 34
        }
        self.diacritical_mark_map = {
            '\u064B': 1, '\u064C': 2, '\u064D': 3, '\u064E': 4, '\u064F': 5,
            '\u0650': 6, '\u0651': 7, '\u0652': 8
        }

    def convert_arabic_to_numbers(self, input_text):
        """
        Convert Arabic text to numbers based on the predefined mappings.
        """
        result = []
        current_word = []
        current_letter = ""
        current_diacritics = []

        for char in input_text:
            if char in self.arabic_letter_map:
                if current_letter:
                    current_word.append(self.format_letter_with_diacritics(current_letter, current_diacritics))
                current_letter = str(self.arabic_letter_map[char])
                current_diacritics = []
            elif char in self.diacritical_mark_map:
                current_diacritics.append(str(self.diacritical_mark_map[char]))
            elif char.isspace():
                if current_letter:
                    current_word.append(self.format_letter_with_diacritics(current_letter, current_diacritics))
                if current_word:
                    result.append(f"[{' - '.join(current_word)}]")
                result.append(' ')
                current_word = []
                current_letter = ""
                current_diacritics = []

        if current_letter:
            current_word.append(self.format_letter_with_diacritics(current_letter, current_diacritics))
        if current_word:
            result.append(f"[{' - '.join(current_word)}]")

        return ''.join(result).strip()

    def format_letter_with_diacritics(self, letter, diacritics):
        if diacritics:
            return f"{letter}({','.join(diacritics)})"
        return letter

    def filter_quran(self, quran_xml, filter_string):
        """
        Filter the Quran XML based on the provided filter string.
        """
        try:
            root = ET.fromstring(quran_xml)
        except ET.ParseError as e:
            print(f"Error parsing Quran XML: {e}")
            return []

        result = []

        # Process each part of the filter string (separated by semicolons)
        for filter_part in filter_string.split(';'):
            surah_filters = filter_part.strip().split(',')
            for surah_filter in surah_filters:
                if surah_filter:  # Only process non-empty filters
                    if ':' in surah_filter:
                        # Handle verse or word-level filtering
                        parts = surah_filter.split(':')
                        surah_num = int(parts[0])
                        if len(parts) > 2:
                            # Word-level filtering
                            verse_num = int(parts[1])
                            word_range = self.parse_range(parts[2])
                            result.extend(self.get_words(root, surah_num, verse_num, word_range))
                        elif len(parts) == 2:
                            # Verse-level filtering
                            verse_range = self.parse_range(parts[1])
                            result.extend(self.get_verses(root, surah_num, verse_range))
                    else:
                        # Surah-level filtering
                        surah_range = self.parse_range(surah_filter)
                        for i in surah_range:
                            surah = self.get_surah(root, i)
                            if surah:
                                result.append(surah)

        return result

    def parse_range(self, range_string):
        """
        Parse a range string (e.g., "1-3" or "5") into a list of integers.
        """
        range_string = range_string.strip()
        if not range_string:
            return []
        if '-' in range_string:
            start, end = map(int, range_string.split('-'))
            return range(start, end + 1)
        return [int(range_string)]

    def get_surah(self, root, surah_num):
        """
        Retrieve an entire surah from the XML.
        """
        surah = root.find(f".//sura[@index='{surah_num}']")
        if surah is not None:
            return {
                'type': 'surah',
                'number': int(surah_num),
                'content': [{'type': 'verse', 'number': int(aya.get('index')), 'text': aya.get('text', '')} for aya in surah.findall('aya')]
            }
        print(f"Surah {surah_num} not found")
        return None

    def get_verses(self, root, surah_num, verse_range):
        """
        Retrieve specific verses from a surah.
        """
        surah = root.find(f".//sura[@index='{surah_num}']")
        if surah is not None:
            verses = surah.findall('aya')
            return [{
                'type': 'verse',
                'surah': surah_num,
                'number': i,
                'text': verses[i-1].get('text', '')
            } for i in verse_range if i <= len(verses)]
        return []

    def get_words(self, root, surah_num, verse_num, word_range):
        """
        Retrieve specific words from a verse.
        """
        surah = root.find(f".//sura[@index='{surah_num}']")
        if surah is not None:
            verse = surah.find(f"aya[@index='{verse_num}']")
            if verse is not None:
                words = verse.get('text', '').split()
                return [{
                    'type': 'word',
                    'surah': surah_num,
                    'verse': verse_num,
                    'text': ' '.join([words[i-1] for i in word_range if i <= len(words)])
                }]
        return []

def read_file(file_path):
    full_path = os.path.join('Resources', file_path)
    print(f"Attempting to read file: {full_path}")
    
    if not os.path.exists(full_path):
        print(f"Error: File not found at {full_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Contents of Resources directory: {os.listdir('Resources')}")
        return ""
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"Successfully read {len(content)} characters from the file.")
        
        # Print the first 100 characters of the file content
        print(f"First 100 characters of {file_path}:")
        print(content[:100])
        
        # Remove any potential Byte Order Mark (BOM) and leading/trailing whitespace
        content = content.strip('\ufeff').strip()
        
        # Check if the content already has an XML declaration
        if not content.startswith('<?xml'):
            content = '<?xml version="1.0" encoding="utf-8"?>\n' + content
        
        # Check if the content is already wrapped in a <quran> tag
        if not content.strip().endswith('</quran>'):
            content = content.rstrip() + '\n</quran>'
        
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def format_specific_search(surah, verse='', word=''):
    """Format the specific search inputs into a search string."""
    parts = [surah]
    if verse:
        parts.append(verse)
        if word:
            parts.append(word)
    return ':'.join(parts)

if __name__ == "__main__":
    import sys

    input_file = 'quran-simple-plain.xml'
    file_content = read_file(input_file)

    if not file_content:
        print("Error reading file or file is empty.")
        sys.exit(1)

    converter = ArabicConverter()
    converted_text = converter.convert_arabic_to_numbers(file_content)
    print("First 500 characters of converted text:")
    print(converted_text[:500])
