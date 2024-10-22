# Quran Digitization and Search Tool

This project is a Python-based application that allows users to search, digitize, and view the Quran in Arabic, with English translations and numerical representations of the Arabic text. In future, the aim is to include deep linguistic as well as numerical Analysis tools to the project to make use of the original Arabic text as well as the digitised data.

## Features

- Search the Quran by surah, verse, or specific words
- View Arabic text, English translations, and digitized representations side by side
- Toggle diacritical marks in the digitized output
- User-friendly GUI built with PyQt5

## Requirements

- Python 3.6+
- PyQt5
- xml.etree.ElementTree

## Installation

1. Clone this repository:   ```
   git clone https://github.com/staysi/Quran_Digitizer.git   ```

2. Navigate to the project directory:   ```
   cd Quran_Digitizer   ```

3. Install the required packages:   ```
   pip install PyQt5   ```

4. Ensure you have the necessary Quran XML files in the `Resources` folder:
   - quran-simple-clean.xml
   - quran-simple-plain.xml
   - en_itani.xml

## Usage

Run the main application:

# Quran Digitization and Search Tool - User Manual

## Getting Started

1. Launch the application by running `python quran_gui.py` in your terminal.
2. The main window will appear with four sections: search inputs (left), digitized results (middle-left), Arabic text (middle-right), and English translation (right).

## Basic Search

1. In the "Search" field at the bottom of the left panel, enter your search query.
2. Click the "Search" button or press Enter to perform the search.
3. Results will appear in the three right panels.

## Specific Search

1. Use the "Surah," "Verse," and "Word" fields in the top-left for more precise searches.
2. Enter the Surah number in the "Surah" field (required).
3. Optionally, enter a verse number in the "Verse" field.
4. Optionally, enter a word or range of words in the "Word" field.
5. Click "Add Item(s)" to add this specific search to the main search field.
6. Repeat steps 1-5 to add multiple items to your search.
7. Click "Search" or press Enter in the main search field to execute the search.

## Search Syntax

- To search for an entire Surah: Enter the Surah number (e.g., "1" for Al-Fatihah).
- To search for specific verses: Use the format "Surah:Verse" (e.g., "2:255" for Ayat Al-Kursi).
- To search for a range of verses: Use "Surah:StartVerse-EndVerse" (e.g., "2:1-5" for the first five verses of Al-Baqarah).
- To search for specific words: Use "Surah:Verse:WordRange" (e.g., "2:255:1-3" for the first three words of Ayat Al-Kursi).
- Combine multiple searches with semicolons (e.g., "1;2:255;3:1-3").

## Additional Features

- Toggle "Include Diacritical Marks" to show or hide diacritical marks in the digitized output.
- Use "Clear All Fields" to reset all input fields.
- Use "Clear Search Results" to clear all result panels.

## Understanding the Results

- Left panel: Displays the digitized representation of the Arabic text.
- Middle panel: Shows the original Arabic text.
- Right panel: Presents the English translation.

## Legend

Refer to the legend at the bottom-left of the application for understanding the digitized representation:
- Numbers represent Arabic letters (e.g., 1=ا, 2=ب).
- Diacritical marks are shown in parentheses (e.g., (4)=Fatha, (7)=Shadda).
- Words are enclosed in square brackets [].

## Tips

- For complex searches, build your query using the specific search fields and "Add Item(s)" button.
- Use the Enter key in any input field to quickly perform a search.
- Explore different combinations of Surahs, verses, and words to refine your search.
