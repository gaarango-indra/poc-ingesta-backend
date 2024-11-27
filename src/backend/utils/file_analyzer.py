import csv
from pathlib import Path
from typing import Optional, Tuple
import re

class FileAnalyzer:
    """
    Class responsible for analyzing a CSV or TXT file to determine if it has a header and identify the delimiter.
    """

    def __init__(self, file_path: str):
        self._file_path = Path(file_path)
        self._delimiters = [',', ';', '\t', '|', ' ']

    def analyze_file(self) -> Optional[Tuple[bool, Optional[str]]]:
        """
        Analyzes the file to determine if it has a header and its delimiter.

        Returns:
            Optional[Tuple[bool, Optional[str]]]: Tuple containing a boolean indicating if the file has a header and
                                                  the delimiter used. Returns None if the file is invalid.
        """
        if not self._is_valid_file():
            return None
        delimiter = self._detect_delimiter()
        if not delimiter:
            return None
        has_header = self._has_header(delimiter)
        return has_header, delimiter

    def _is_valid_file(self) -> bool:
        """
        Checks if the provided file path is valid and the file is a CSV or TXT file.

        Returns:
            bool: True if the file path is valid, False otherwise.
        """
        return self._file_path.exists() and self._file_path.is_file() and self._file_path.suffix in ['.csv', '.txt']

    def _detect_delimiter(self) -> Optional[str]:
        """
        Detects the delimiter used in the file by analyzing the first line.

        Returns:
            Optional[str]: The detected delimiter or None if no suitable delimiter is found.
        """
        with self._file_path.open('r', encoding='utf-8') as file:
            sample = file.readline()
            for delimiter in self._delimiters:
                if sample.count(delimiter) > 0:
                    return delimiter
        return None

    def _has_header(self, delimiter: str) -> bool:
        """
        Determines if the file has a header by analyzing the data types and patterns
        in the first two rows of the file, allowing flexible data types in the second row.

        Args:
            delimiter (str): The delimiter used in the file.

        Returns:
            bool: True if the file likely has a header, False otherwise.
        """
        # Define the pattern to detect header keywords
        header_keywords = re.compile(r'(id|date|year)', re.IGNORECASE)
        # Define a pattern to detect date-like values
        date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{4}/\d{2}/\d{2})$')

        with self._file_path.open('r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=delimiter)
            try:
                first_row = next(reader)
                second_row = next(reader, None)

                # If second row exists, analyze the rows
                if second_row:
                    # Check if the first row contains header-like patterns
                    first_row_is_header = any(
                        not item.replace('.', '', 1).isdigit()  # Allow decimal numbers
                        and not item.isnumeric()  # Handle numeric-like values
                        and not item.strip() == ''  # Ignore empty values
                        and (header_keywords.search(item) is not None  # Match header keywords
                            or not item.strip().islower())  # Check if it's not purely lowercase (e.g., names)
                        for item in first_row
                    )

                    # Check if the second row contains a mix of valid data types
                    second_row_is_data = all(
                        item.strip() == ''  # Allow empty values
                        or item.replace('.', '', 1).isdigit()  # Allow integers and decimals
                        or re.match(r'^-?\d+(\.\d+)?$', item.strip())  # Match decimal values
                        or date_pattern.match(item.strip())  # Match date-like values
                        or item.isalpha()  # Allow pure string values
                        or item.isalnum()  # Allow alphanumeric strings
                        for item in second_row
                    )
                    return first_row_is_header and second_row_is_data
                return False  # No second row to compare, assume no header
            except StopIteration:
                # If file is empty or doesn't have enough rows, assume no header
                return False