# UTF-8 Python 3.13.5
# Utility functions for paragraph classes
# Author: Intan K. Wardhani

import re
import requests
from bs4 import BeautifulSoup

class Text:
    
    def __init__(self):
        pass
    
    def sanitise_paragraph(self, texts: str) -> str:
    
        """A function that cleans the texts extracted from a wiki page."""
        
        # remove reference-style notes like [a], [1], [note 2]
        self.text = re.sub(r'\[[^\]]*\]', ' ', texts)

        # ensure a space after closing parentheses or punctuation if missing
        self.text = re.sub(r'([a-z\)])([A-Z])', r'\1 \2', self.text)  # e.g., ")i" -> ") i"

        # add missing spaces between words stuck together (lowercase + uppercase)
        self.text = re.sub(r'([a-z])([A-Z])', r'\1 \2', self.text)

        # fix glued numbers/words: 44thpresident → 44th president
        # text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
        self.text = re.sub(r'(\d[a-z][a-z])([a-z])', r'\1 \2', self.text)

        # add missing space after known words when glued
        # e.g., "theDemocratic" → "the Democratic"
        self.text = re.sub(r'([a-z])([A-Z])', r'\1 \2', self.text)

        # fix cases like "Statesfrom" → "States from"
        self.text = re.sub(r'([a-z])([A-Z])', r'\1 \2', self.text)

        # add space after periods if missing (e.g. "2004.He" → "2004. He")
        self.text = re.sub(r'\.([A-Z])', r'. \1', self.text)

        # handle “aU.S.” → “a U.S.”
        self.text = re.sub(r'([a-z])([A-Z]\.)', r'\1 \2', self.text)

        # normalise whitespace (collapse multiple spaces)
        self.text = re.sub(r'\s+', ' ', self.text).strip()
        
        return self.text
    
    def get_first_paragraph(self, wiki_url: requests.models.Response) -> tuple:
    
        """A function to get only the first paragraph from a wiki page."""
        
        soup = BeautifulSoup(wiki_url.text, 'html.parser')
        lang = soup.html.get("lang") if soup.html else "unknown" # i wanna know the language
        first_paragraph = ""
        for p in soup.select("div.mw-parser-output p"):
            text = p.get_text(strip=True)
            if not text:
                continue # skip empty text
            if 'redirected from' in text.lower():
                continue # skip redirect messages
            if p.find_parent('table') or p.find_parent('div', class_='hatnote'):
                continue # skip infoboxes, notices, etc.
            first_paragraph = text
            break # stop after first paragraph
        
        clean_paragraph = self.sanitise_paragraph(first_paragraph)
        
        return lang, clean_paragraph