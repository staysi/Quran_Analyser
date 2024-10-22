import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTextEdit, QSplitter, QFrame, QGridLayout, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette, QFont
from arabic_converter import ArabicConverter, read_file, format_specific_search
import xml.etree.ElementTree as ET
import logging

# Set up logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuranGUI(QWidget):
    def __init__(self):
        super().__init__()
        logging.info("Initializing QuranGUI...")
        self.converter = ArabicConverter()
        self.quran_xml = {}  # Will store both versions of the Quran XML
        self.english_translation = None  # Will store the parsed English translation
        self.load_quran_xml()
        self.initUI()
        logging.info("QuranGUI initialized.")

    def load_quran_xml(self):
        """
        Load both versions of the Quran XML and the English translation.
        This method reads the XML files and stores them in memory for quick access.
        """
        logging.info("Loading Quran XML files...")
        self.quran_xml['clean'] = read_file('quran-simple-clean.xml')
        self.quran_xml['plain'] = read_file('quran-simple-plain.xml')
        english_xml = read_file('en_itani.xml')
        self.english_translation = ET.fromstring(english_xml)
        logging.info("Quran XML files loaded.")

    def initUI(self):
        """
        Initialize the user interface.
        This method sets up the main window and all the widgets within it.
        """
        self.setWindowTitle('Quran Digitization Filter')
        self.setGeometry(100, 100, 2400, 800)  # Set window size and position

        main_layout = QGridLayout()

        # Create and add the left frame for search inputs
        left_frame = self.create_left_frame()
        main_layout.addWidget(left_frame, 0, 0)

        # Create and add the legend
        legend = self.create_legend()
        main_layout.addWidget(legend, 1, 0)

        # Create the middle frame for digitized results (white text)
        self.digitized_result = self.create_result_text_edit(Qt.white, font_size_increase=1)
        main_layout.addWidget(self.digitized_result, 0, 1, 2, 1)

        # Create the right frame for original Arabic results (orange text and larger font)
        self.arabic_result = self.create_result_text_edit(QColor(255, 165, 0), font_size_increase=4)
        main_layout.addWidget(self.arabic_result, 0, 2, 2, 1)

        # Create the far-right frame for English translation results
        self.english_result = self.create_result_text_edit(Qt.white, font_size_increase=2)
        main_layout.addWidget(self.english_result, 0, 3, 2, 1)

        # Set column stretch to make result frames wider
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 2)
        main_layout.setColumnStretch(2, 2)
        main_layout.setColumnStretch(3, 2)

        self.setLayout(main_layout)

    def create_left_frame(self):
        """
        Create the left frame containing search inputs and buttons.
        This frame allows users to input search criteria and control the application.
        """
        left_frame = QFrame()
        left_frame.setFrameShape(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_frame)

        # Add specific search fields
        search_grid = QGridLayout()
        search_grid.addWidget(QLabel('Surah:'), 0, 0)
        self.surah_input = QLineEdit()
        self.surah_input.returnPressed.connect(self.handle_enter)
        search_grid.addWidget(self.surah_input, 0, 1)

        search_grid.addWidget(QLabel('Verse:'), 1, 0)
        self.verse_input = QLineEdit()
        self.verse_input.returnPressed.connect(self.handle_enter)
        search_grid.addWidget(self.verse_input, 1, 1)

        search_grid.addWidget(QLabel('Word:'), 2, 0)
        self.word_input = QLineEdit()
        self.word_input.returnPressed.connect(self.handle_enter)
        search_grid.addWidget(self.word_input, 2, 1)

        add_item_button = QPushButton('Add Item(s)')
        add_item_button.clicked.connect(self.add_specific_search)
        search_grid.addWidget(add_item_button, 3, 0, 1, 2)

        left_layout.addLayout(search_grid)

        # Add main filter input
        left_layout.addWidget(QLabel('Search:'))
        self.filter_input = QLineEdit()
        self.filter_input.returnPressed.connect(self.handle_enter)
        left_layout.addWidget(self.filter_input)
        filter_button = QPushButton('Search')
        filter_button.clicked.connect(self.apply_filter)
        left_layout.addWidget(filter_button)

        # Add diacritical marks checkbox
        self.diacritical_checkbox = QCheckBox('Include Diacritical Marks')
        left_layout.addWidget(self.diacritical_checkbox)

        # Add clear buttons
        clear_fields_button = QPushButton('Clear All Fields')
        clear_fields_button.clicked.connect(self.clear_fields)
        left_layout.addWidget(clear_fields_button)

        clear_results_button = QPushButton('Clear Search Results')
        clear_results_button.clicked.connect(self.clear_results)
        left_layout.addWidget(clear_results_button)

        left_layout.addStretch()
        return left_frame

    def handle_enter(self):
        """
        Handle Enter/Return key press in input fields.
        This method decides whether to add a specific search or apply the filter based on user input.
        """
        if self.surah_input.text() or self.verse_input.text() or self.word_input.text():
            self.add_specific_search()
        else:
            self.apply_filter()

    def create_result_text_edit(self, text_color, font_size_increase=0):
        """
        Create a QTextEdit widget for displaying results.
        This method sets up the text color, background, and font size for result display areas.
        """
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        palette = text_edit.palette()
        palette.setColor(QPalette.Base, QColor(64, 64, 64))  # Dark grey background
        palette.setColor(QPalette.Text, text_color)
        text_edit.setPalette(palette)

        # Increase font size if specified
        if font_size_increase > 0:
            font = text_edit.font()
            font.setPointSize(font.pointSize() + font_size_increase)
            text_edit.setFont(font)

        return text_edit

    def create_legend(self):
        """
        Create a legend explaining the digitized representation.
        This method provides a key for understanding the numerical representation of Arabic text.
        """
        legend_frame = QFrame()
        legend_frame.setFrameShape(QFrame.StyledPanel)
        legend_layout = QVBoxLayout(legend_frame)

        legend_title = QLabel("Legend")
        legend_title.setAlignment(Qt.AlignCenter)
        legend_title.setFont(QFont("Arial", 10, QFont.Bold))
        legend_layout.addWidget(legend_title)

        legend_text = """
• Arabic letters: numbers (ا=1, ب=2, ...)
• Letters in word: separated by " - "
• Words: enclosed in []
• Diacritics: (1)=Fathatan, (2)=Dammatan,
  (3)=Kasratan, (4)=Fatha, (5)=Damma,
  (6)=Kasra, (7)=Shadda, (8)=Sukun
Example: [1 - 23 - 25(4) - 1 - 12(7) - 32]
= "الناس" (an-naas)
"""

        legend_label = QLabel(legend_text)
        legend_label.setWordWrap(True)
        legend_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        legend_layout.addWidget(legend_label)

        return legend_frame

    def apply_filter(self):
        """
        Apply the main filter to search the Quran.
        This method processes the search string and displays the results.
        """
        filter_string = self.filter_input.text().rstrip(';')
        if not filter_string:
            return
        self.process_search(filter_string)

    def add_specific_search(self):
        """
        Add a specific search item to the main search field.
        This method formats the surah, verse, and word inputs into a search string.
        """
        surah = self.surah_input.text()
        verse = self.verse_input.text()
        word = self.word_input.text()

        if not surah:
            QMessageBox.warning(self, "Input Error", "Please enter a Surah number.")
            return
        if verse and not word:
            filter_string = format_specific_search(surah, verse)
        elif word and not verse:
            QMessageBox.warning(self, "Input Error", "Please enter a Verse number when specifying Words.")
            return
        else:
            filter_string = format_specific_search(surah, verse, word)

        current_search = self.filter_input.text()
        if current_search and not current_search.endswith(';'):
            current_search += ';'
        self.filter_input.setText(current_search + filter_string + ';')

        # Clear the specific search fields
        self.surah_input.clear()
        self.verse_input.clear()
        self.word_input.clear()

    def process_search(self, filter_string):
        """
        Process the search and display results.
        This method filters the Quran based on the search string and updates all result displays.
        """
        # Choose the appropriate XML based on checkbox state
        xml_key = 'plain' if self.diacritical_checkbox.isChecked() else 'clean'
        filtered_results = self.converter.filter_quran(self.quran_xml[xml_key], filter_string)
        
        digitized_text = self.format_results(filtered_results, True)
        arabic_text = self.format_results(filtered_results, False)
        english_text = self.format_english_results(filtered_results)
        
        self.digitized_result.setText(digitized_text)
        self.arabic_result.setText(arabic_text)
        self.english_result.setText(english_text)

    def format_results(self, results, digitize=False):
        """
        Format the search results for display.
        This method organizes the results into a readable format, optionally digitizing the text.
        """
        formatted_text = ""
        current_surah = None

        for item in results:
            if item['type'] == 'surah':
                if current_surah != item['number']:
                    formatted_text += f"\n\nSurah {item['number']}:\n"
                    current_surah = item['number']
                for verse in item['content']:
                    formatted_text += self.format_verse(verse, digitize) + "\n"
            elif item['type'] == 'verse':
                if current_surah != item['surah']:
                    formatted_text += f"\n\nSurah {item['surah']}:\n"
                    current_surah = item['surah']
                formatted_text += self.format_verse(item, digitize) + "\n"
            elif item['type'] == 'word':
                if current_surah != item['surah']:
                    formatted_text += f"\n\nSurah {item['surah']}, Verse {item['verse']}:\n"
                    current_surah = item['surah']
                formatted_text += self.format_word(item, digitize) + " "

        return formatted_text.strip()

    def format_verse(self, verse, digitize):
        """
        Format a single verse, optionally digitizing it.
        """
        text = verse['text']
        if digitize:
            text = self.converter.convert_arabic_to_numbers(text)
        return f"{verse['number']}. {text}"

    def format_word(self, word, digitize):
        """
        Format a single word, optionally digitizing it.
        """
        text = word['text']
        if digitize:
            text = self.converter.convert_arabic_to_numbers(text)
        return text

    def add_trackers(self, word):
        """
        Add trackers to a digitized word.
        This method adds indicators for special Arabic characters like Shadda, Tanween, and Ta marboota.
        """
        trackers = ""
        if '(7)' in word:  # Shadda
            trackers += 'S'
        if any(f'({i})' in word for i in [1, 2, 3]):  # Tanween
            trackers += 'T'
        if '32' in word:  # Ta marboota
            trackers += 'M'
        return f"[{word}{trackers}]" if trackers else f"[{word}]"

    def clear_fields(self):
        """
        Clear all input fields.
        """
        self.filter_input.clear()
        self.surah_input.clear()
        self.verse_input.clear()
        self.word_input.clear()

    def clear_results(self):
        """
        Clear all result display areas.
        """
        self.digitized_result.clear()
        self.arabic_result.clear()
        self.english_result.clear()

    def format_english_results(self, results):
        """
        Format the English translation results for display.
        This method organizes the English translations into a readable format.
        """
        formatted_text = ""
        current_surah = None

        for item in results:
            if item['type'] == 'surah':
                surah_num = item['number']
                formatted_text += f"\n\nSurah {surah_num}:\n"
                for verse in item['content']:
                    formatted_text += self.format_english_verse(surah_num, verse['number']) + "\n"
            elif item['type'] == 'verse':
                if current_surah != item['surah']:
                    formatted_text += f"\n\nSurah {item['surah']}:\n"
                    current_surah = item['surah']
                formatted_text += self.format_english_verse(item['surah'], item['number']) + "\n"
            elif item['type'] == 'word':
                if current_surah != item['surah']:
                    formatted_text += f"\n\nSurah {item['surah']}, Verse {item['verse']}:\n"
                    current_surah = item['surah']
                formatted_text += self.get_english_word(item['surah'], item['verse'], item['text']) + " "

        return formatted_text.strip()

    def format_english_verse(self, surah, verse_num):
        """
        Format a single English verse.
        """
        text = self.get_english_translation(surah, verse_num)
        return f"{verse_num}. {text}"

    def get_english_translation(self, surah, verse):
        """
        Get the English translation for a specific verse.
        This method retrieves the translation from the pre-loaded English XML.
        """
        try:
            verse_element = self.english_translation.find(f".//sura[@index='{surah}']/aya[@index='{verse}']")
            if verse_element is not None:
                return verse_element.get('text', '')
        except Exception as e:
            logging.error(f"Error getting English translation for Surah {surah}, Verse {verse}: {e}")
        return '[Translation not available]'

    def get_english_word(self, surah, verse, arabic_word):
        """
        Get the English translation for a specific word.
        This is a simplistic approach and may not always be accurate for individual words.
        """
        full_verse = self.get_english_translation(surah, verse)
        words = full_verse.split()
        arabic_words = self.get_arabic_verse(surah, verse).split()
        if arabic_word in arabic_words:
            index = arabic_words.index(arabic_word)
            if index < len(words):
                return words[index]
        return '[Translation not available]'

    def get_arabic_verse(self, surah, verse):
        """
        Get the Arabic text for a specific verse.
        """
        root = ET.fromstring(self.quran_xml['clean'])
        verse_element = root.find(f".//sura[@index='{surah}']/aya[@index='{verse}']")
        if verse_element is not None:
            return verse_element.get('text', '')
        return ''

    def showEvent(self, event):
        """
        Event handler for when the window is shown.
        This method sets the focus to the filter input field when the application starts.
        """
        super().showEvent(event)
        QTimer.singleShot(0, self.filter_input.setFocus)

if __name__ == '__main__':
    logging.info("Starting QuranGUI application...")
    app = QApplication(sys.argv)
    ex = QuranGUI()
    ex.show()
    sys.exit(app.exec_())
