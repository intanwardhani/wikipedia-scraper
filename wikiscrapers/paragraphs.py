# UTF-8 Python 3.13.5
# Utility functions for paragraph classes
# Author: Intan K. Wardhani

import re
import requests
from bs4 import BeautifulSoup

class Paragraph:
        
    """
    A class for extracting and cleaning the first paragraph from a Wikipedia page.

    This class handles different languages and attempts light defensive parsing to 
    account for malformed HTML. It also cleans common formatting issues in the text,
    such as missing spaces, references, and glued words.

    Attributes
    ----------
    session : None
        A session from requests.Session() that is shared by Leader class to avoid
        calling multiple HTTP sessions.

    Methods
    -------
    _sanitize_paragraph(text: str) -> str
        Cleans raw text extracted from a Wikipedia page by removing reference notes,
        adding missing spaces between words/numbers, handling glued abbreviations, 
        and normalising whitespace.

    get_first_paragraph(wiki_response: requests.models.Response) -> tuple
        Extracts the first meaningful paragraph from a Wikipedia page response 
        and detects the page's language.
        Parameters:
            wiki_response (requests.models.Response): The HTTP response object from a Wikipedia page.
        Returns:
            tuple: 
                - str: The language code from the <html lang=""> attribute, or "unknown".
                - str: The cleaned first paragraph text, or an empty string if unavailable.
    """

    def __init__(self, session=None):
        self.session = session  # optional shared session
        
    def _sanitize_paragraph(self, text: str) -> str:
        
        """Clean raw text extracted from a wiki page."""

        # Remove reference-style notes like [a], [1], [note 2]
        text = re.sub(r'\[[^\]]*\]', ' ', text)

        # Add missing spaces between lowercase-uppercase and number-word boundaries
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)

        # Add missing space after punctuation if missing
        text = re.sub(r'([a-z\)])([A-Z])', r'\1 \2', text)  # e.g. ")i" -> ") i"
        text = re.sub(r'\.([A-Z])', r'. \1', text)  # e.g. "2004.He" -> "2004. He"

        # Handle glued abbreviations like “aU.S.” → “a U.S.”
        text = re.sub(r'([a-z])([A-Z]\.)', r'\1 \2', text)

        # Normalise whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def get_first_paragraph(self, wiki_response: requests.models.Response) -> tuple:
        
        """Extract the first clean paragraph and detect page language, with light error handling."""

        try:
            # Try to parse the HTML content safely
            soup = BeautifulSoup(wiki_response.text, 'html.parser')
        except Exception as e:
            # Handle cases where HTML parsing itself fails
            print(f"Failed to parse HTML for {getattr(wiki_response, 'url', 'unknown URL')}: {e}")
            return "unknown", ""

        try:
            # Safely get language (some malformed HTMLs might lack <html> tag)
            lang = soup.html.get("lang") if soup.html else "unknown"

            content_div = soup.find("div", class_="mw-parser-output")
            if not content_div:
                print(f"No main content div found for {getattr(wiki_response, 'url', 'unknown URL')}")
                return lang, ""

            first_paragraph = ""

            # Iterate through direct child <p> tags for reliability
            for p in soup.select("div.mw-parser-output p"):
                text = p.get_text(strip=True)
                if not text:
                    continue  # skip empty text
                if 'redirected from' in text.lower():
                    continue  # skip redirect messages
                if p.find_parent('table') or p.find_parent('div', class_='hatnote'):
                    continue  # skip infoboxes, hatnotes, etc.
                first_paragraph = text
                break  # stop after first valid paragraph

            clean_paragraph = self._sanitize_paragraph(first_paragraph)
            return lang, clean_paragraph

        except Exception as e:
            # Handle any other local parsing/cleaning issues
            print(f"Error while extracting first paragraph from {getattr(wiki_response, 'url', 'unknown URL')}: {e}")
            return "unknown", ""

