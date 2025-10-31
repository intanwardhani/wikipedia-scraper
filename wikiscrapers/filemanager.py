# UTF-8 Python 3.13.5
# Utility functions for file-exporting-related classes
# Author: Intan K. Wardhani

import json
import csv

class Save:
    
    """
    A class for exporting and importing data to and from JSON files (for now).

    This class provides simple utility methods to save Python dictionaries
    as JSON files and to load JSON files back into Python dictionaries.
    It preserves non-English characters by default using UTF-8 encoding.

    Attributes
    ----------
    None

    Methods
    -------
    export_json(filename: str, dict_data: dict, ensure_ascii: bool = False) -> None
        Exports a dictionary to a JSON file with human-readable indentation.
        Parameters:
            filename (str): The desired name of the output JSON file (without extension).
            dict_data (dict): The dictionary data to be written to the file.
            ensure_ascii (bool): Whether to escape non-ASCII characters. 
                                 Defaults to False to preserve readable text (e.g., Arabic, Cyrillic).

    import_json(filename: str) -> dict
        Imports data from a JSON file and returns it as a Python dictionary.
        Parameters:
            filename (str): The name of the JSON file (without extension) to be read.
        Returns:
            dict: The data loaded from the JSON file.
    """

    def export_json(self, filename: str, dict_data: dict, ensure_ascii: bool = False) -> None:
        
        """Export dictionary data to a JSON file.
        
        Non-English characters are preserved by default (ensure_ascii=False).
        """
        
        with open(f"{filename}.json", "w", encoding="utf-8") as f:
            json.dump(dict_data, f, ensure_ascii=ensure_ascii, indent=4)

    def import_json(self, filename: str) -> dict:
        
        """Import JSON file and return as dictionary."""
        
        with open(f"{filename}.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def export_csv(self, filename: str, data: list[dict]) -> None:
        
        """Export a list of dictionaries to a CSV file."""
        
        if not data:
            print("No data to export.")
            return

        with open(f"{filename}.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)