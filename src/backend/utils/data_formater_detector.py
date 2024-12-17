from datetime import datetime
from typing import List, Optional

class DateFormatDetector:
    """
    A class to detect the format of a given date string based on a predefined list of formats.
    """

    def __init__(self, date_formats: Optional[List[dict]] = None):
        """
        Initialize the DateFormatDetector with a list of date formats.
        If no formats are provided, a default list is used.
        """
        self._date_formats = date_formats or [
            {"pattern": "%d/%m/%Y", "human_readable": "dd/MM/yyyy"},
            {"pattern": "%Y-%m-%d", "human_readable": "yyyy-MM-dd"},
            {"pattern": "%m/%d/%Y", "human_readable": "MM/dd/yyyy"},
            {"pattern": "%d-%m-%Y", "human_readable": "dd-MM-yyyy"},
            {"pattern": "%Y/%m/%d", "human_readable": "yyyy/MM/dd"},
            {"pattern": "%B %d, %Y", "human_readable": "Month day, Year"},
            {"pattern": "%d %B %Y", "human_readable": "day Month Year"},
            {"pattern": "%Y.%m.%d", "human_readable": "yyyy.MM.dd"},
            {"pattern": "%d.%m.%Y", "human_readable": "dd.MM.yyyy"},
        ]

    def detect_format(self, date_string: str) -> Optional[str]:
        """
        Detect the format of a given date string.

        :param date_string: The date string to analyze.
        :return: The human-readable format string if a match is found, otherwise None.
        """
        for date_format in self._date_formats:
            if self._is_valid_format(date_string, date_format["pattern"]):
                return date_format["human_readable"]
        return None

    def _is_valid_format(self, date_string: str, date_format: str) -> bool:
        """
        Check if the given date string matches the provided format.

        :param date_string: The date string to validate.
        :param date_format: The format to test against.
        :return: True if the date matches the format, False otherwise.
        """
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    def add_format(self, new_format: str, human_readable: str) -> None:
        """
        Add a new date format to the list of formats.

        :param new_format: The format pattern to add (e.g., "%d/%m/%Y").
        :param human_readable: The human-readable equivalent (e.g., "dd/MM/yyyy").
        """
        if not any(fmt["pattern"] == new_format for fmt in self._date_formats):
            self._date_formats.append({"pattern": new_format, "human_readable": human_readable})

    def get_formats(self) -> List[dict]:
        """
        Retrieve the current list of date formats.

        :return: A list of dictionaries with format patterns and their human-readable equivalents.
        """
        return self._date_formats
