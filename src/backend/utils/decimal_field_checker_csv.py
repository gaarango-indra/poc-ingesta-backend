import csv
import logging

logging.basicConfig(level=logging.ERROR)

class DecimalFieldCheckerCSV:
    """
    A class to check for the presence of commas (',') and dots ('.')
    in fields of type 'decimal' in a CSV file.
    """

    def __init__(self, csv_file_path: str, data_type_fields: dict):
        """
        Initialize the DecimalFieldCheckerCSV with the CSV file path and a dictionary of data types and fields.

        Args:
            csv_file_path (str): The path to the CSV file.
            data_type_fields (dict): A dictionary where keys are data types (e.g., "decimal(10,2)")
                                     and values are tuples of field names of that type.
        """
        self.csv_file_path = csv_file_path
        self.data_type_fields = data_type_fields

    def _get_decimal_fields(self) -> list:
        """
        Extracts the list of fields associated with 'decimal' data types.

        Returns:
            list: A list of field names with data types starting with 'decimal'.
        """
        return [
            field for data_type, fields in self.data_type_fields.items()
            if data_type.lower().startswith("decimal") for field in fields
        ]

    def check_comma_and_dot(self) -> tuple:
        """
        Checks for the presence of commas (',') and dots ('.') in the specified decimal fields.

        Returns:
            tuple: A tuple (found_comma, found_dot) indicating whether commas and dots were found.
        """
        decimal_fields = self._get_decimal_fields()
        found_comma = False
        found_dot = False

        try:
            with open(self.csv_file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    for field in decimal_fields:
                        # Validate if the field exists in the row
                        if field in row and isinstance(row[field], str):
                            value = row[field]
                            if ',' in value:
                                found_comma = True
                            if '.' in value:
                                found_dot = True

                            # Exit early if both are found
                            if found_comma and found_dot:
                                return True, True

            return found_comma, found_dot
        except FileNotFoundError:
            logging.error(f"Error: File '{self.csv_file_path}' not found.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        
        # Return default values if an error occurred
        return False, False