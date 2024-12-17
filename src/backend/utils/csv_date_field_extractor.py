import pandas as pd
from typing import Dict, List

class CsvDateFieldExtractor:
    """
    Class responsible for extracting values from CSV files based on grouped fields.
    """
    def __init__(self, csv_path: str, grouped_fields: Dict[str, List[str]], delimiter: str):
        """
        Initializes the CsvFieldExtractor.

        Args:
            csv_path (str): Path to the CSV file.
            grouped_fields (Dict[str, List[str]]): Dictionary containing field types as keys and
                                                 a list of field names as values.
        """
        self._csv_path = csv_path
        self._grouped_fields = grouped_fields
        self.delimiter = delimiter
        self._dataframe = None
        self._load_csv()

    def _load_csv(self) -> None:
        """
        Loads the CSV file into a pandas DataFrame securely.

        Raises:
            FileNotFoundError: If the file is not found at the given path.
            ValueError: If an error occurs while reading the CSV file.
        """
        try:
            self._dataframe = pd.read_csv(self._csv_path, sep=self.delimiter)
        except FileNotFoundError as file_error:
            raise FileNotFoundError(f"File not found: '{self._csv_path}'.") from file_error
        except pd.errors.EmptyDataError:
            raise ValueError("The CSV file is empty or corrupted.")
        except Exception as error:
            raise ValueError(f"Error loading the CSV file: {error}.")

    def get_first_date_field_value(self) -> str:
        """
        Retrieves the first value of a field with the 'date' type from the CSV file.

        Returns:
            str: The first value of a 'date' type field.

        Raises:
            ValueError: If no 'date' fields are found or none exist in the CSV file.
        """
        date_fields = self._grouped_fields.get('date', [])
        if not date_fields:
            raise ValueError("No fields of type 'date' found in grouped_fields.")
        
        print(f"Campos de tipo Date gropued_fields: {date_fields}")
        print(f"Campos de la Sample Data CSV: {self._dataframe.columns}")

        for field in date_fields:
            if field in self._dataframe.columns:
                # Return the first non-null value for the field
                first_value = self._dataframe[field].dropna().iloc[0]
                return str(first_value)
            print(f"Warning: Field '{field}' does not exist in the CSV file.")

        raise ValueError("None of the 'date' fields exist in the CSV file.")
