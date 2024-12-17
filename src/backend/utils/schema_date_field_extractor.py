from typing import List, Dict, Any, Optional


class SchemaDateFieldExtractor:
    """
    A class to extract 'format' values from dictionary fields where the 'type' is 'date'.
    Implements clean code practices, adheres to SOLID principles, and follows PEP8 guidelines.
    """

    def __init__(self, source_data: Dict[str, Any]) -> None:
        """
        Initializes the DateFieldExtractor with a data dictionary.

        :param source_data: Dictionary containing the data structure.
        """
        if not isinstance(source_data, dict):
            raise ValueError("source_data must be a dictionary")
        self._source_data = source_data

    def extract_date_formats(self) -> List[Dict[str, Optional[str]]]:
        """
        Extracts the 'format' values from fields where 'type' equals 'date'.

        :return: A list of dictionaries with field names as keys and 'format' as values.
        """
        result = []
        fields = self._source_data.get("fields", [])

        if not isinstance(fields, list):
            raise ValueError("'fields' must be a list of dictionaries")

        for field in fields:
            if self._is_valid_date_field(field):
                field_name = field.get("name")
                date_format = field.get("format")
                result.append({field_name: date_format})

        return result

    @staticmethod
    def _is_valid_date_field(field: Dict[str, Any]) -> bool:
        """
        Validates if a field has 'type' set to 'date'.

        :param field: A single field dictionary.
        :return: True if 'type' equals 'date', otherwise False.
        """
        return isinstance(field, dict) and field.get("type") == "date"