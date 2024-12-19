import csv
import re
from typing import Dict, List, Tuple, Any

class CSVDecimalValidator:
    """
    A class to validate CSV files for correct decimal formats and delimiters.

    Attributes:
        csv_path (str): Path to the CSV file to be validated.
        grouped_fields (Dict[str, Tuple[str]]): Mapping of data types to fields in the CSV.
        delimiter (str): The delimiter used in the CSV file.
    """

    def __init__(self, csv_path: str, grouped_fields: Dict[str, Tuple[str]]) -> None:
        """
        Initialize the CSVDecimalValidator.

        Args:
            csv_path (str): Path to the CSV file.
            grouped_fields (Dict[str, Tuple[str]]): Dictionary of data types mapped to fields.
        """
        self.csv_path = csv_path
        self.grouped_fields = grouped_fields
        self.delimiter = self._detect_delimiter()

    def _detect_delimiter(self) -> str:
        """
        Detect the delimiter of the CSV file dynamically.

        Returns:
            str: The detected delimiter or a default comma (',') if detection fails.
        """
        with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
            sample = file.read(1024)  # Read a sample of the file
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
                return dialect.delimiter
            except csv.Error:
                return ','  # Default to comma if detection fails

    def analyze_csv(self) -> Dict[str, Any]:
        """
        Analyze the CSV file for decimal format compliance and delimiter usage.

        Returns:
            Dict[str, Any]: A dictionary with analysis results including:
                - comma (bool): Whether commas are present in the values.
                - dot (bool): Whether dots are present in the values.
                - decimal_symbol (str): The detected decimal symbol (',' or '.').
                - correct_data (bool): Whether the data complies with the decimal format.
        """
        comma = False
        dot = False
        decimal_symbol = None
        correct_data = False  # Default to False

        # Extract decimal field specifications
        decimal_fields = {
            data_type: (fields, int(re.search(r"\((\d+),(\d+)\)", data_type).group(2)))
            for data_type, fields in self.grouped_fields.items()
            if data_type.startswith("decimal") and re.search(r"\((\d+),(\d+)\)", data_type)
        }

        # Read the CSV file
        with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=self.delimiter)
            headers = reader.fieldnames

            # Ensure fieldnames are present in the CSV header
            missing_fields = []
            for decimal_type, (fields, _) in decimal_fields.items():
                for field in fields:
                    if field not in headers:
                        missing_fields.append(field)

            if missing_fields:
                print(f"Warning: The following fields are missing in the CSV file: {missing_fields}")

            for row in reader:
                for decimal_type, (fields, decimal_places) in decimal_fields.items():
                    for field in fields:
                        if field not in headers:
                            continue  # Skip missing fields

                        value = row[field].strip()

                        # Check for presence of comma and dot
                        if "," in value:
                            comma = True
                        if "." in value:
                            dot = True

                        # Determine decimal symbol
                        if "," in value and "." in value:
                            decimal_symbol = "," if value.rfind(",") > value.rfind(".") else "."
                        elif "," in value:
                            decimal_symbol = ","
                        elif "." in value:
                            decimal_symbol = "."

                        # Validate number of decimal places
                        if decimal_symbol:
                            parts = value.rsplit(decimal_symbol, 1)
                            if len(parts) == 2 and len(parts[1]) == decimal_places:
                                correct_data = True  # Set to True only if validation passes
                            else:
                                correct_data = False

        return {
            "comma": comma,
            "dot": dot,
            "decimal_symbol": decimal_symbol,
            "correct_data": correct_data
        }
