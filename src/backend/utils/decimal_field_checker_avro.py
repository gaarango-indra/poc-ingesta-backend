import fastavro


class DecimalFieldChecker:
    """
    A class to check for the presence of commas (',') and dots ('.')
    in fields of type 'decimal' in an AVRO file.
    """

    def __init__(self, avro_file_path: str, data_type_fields: dict):
        """
        Initialize the DecimalFieldChecker with the AVRO file path and a dictionary of data types and fields.

        Args:
            avro_file_path (str): The path to the AVRO file.
            data_type_fields (dict): A dictionary where keys are data types (e.g., "decimal(10,2)")
                                     and values are tuples of field names of that type.
        """
        self.avro_file_path = avro_file_path
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
            with open(self.avro_file_path, 'rb') as avro_file:
                reader = fastavro.reader(avro_file)

                for record in reader:
                    for field in decimal_fields:
                        # Validate if the field exists and is a string
                        if field in record and isinstance(record[field], str):
                            value = record[field]
                            if ',' in value:
                                found_comma = True
                            if '.' in value:
                                found_dot = True

                            # Exit early if both are found
                            if found_comma and found_dot:
                                return True, True

            return found_comma, found_dot
        except FileNotFoundError:
            print(f"Error: File '{self.avro_file_path}' not found.")
        except fastavro.reader.ReaderError:
            print(f"Error: File '{self.avro_file_path}' is not a valid AVRO file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        # Return default values if an error occurred
        return False, False
