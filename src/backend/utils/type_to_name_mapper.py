from typing import Dict, Tuple, List


class TypeToNameMapper:
    """
    A class to process a JSON schema and map types to names.
    Adheres to SOLID principles and ensures modular, reusable code.
    """

    def __init__(self, schema: Dict):
        """
        Initialize the mapper with the given schema.

        Args:
            schema (Dict): The JSON schema containing the fields.
        """
        self.schema = schema

    def map_types_to_names(self) -> Dict[str, Tuple[str]]:
        """
        Maps field types to their corresponding names in the schema.

        Returns:
            Dict[str, Tuple[str]]: A dictionary where the key is the type
            and the value is a tuple of field names.
        """
        type_to_name_mapping: Dict[str, List[str]] = {}

        # Process each field in the schema
        for field in self.schema.get("fields", []):
            field_type = field.get("type")
            field_name = field.get("name")
            if field_type and field_name:
                # Add the name to the corresponding type key
                type_to_name_mapping.setdefault(field_type, []).append(field_name)

        # Convert lists to tuples for immutability
        return {key: tuple(names) for key, names in type_to_name_mapping.items()}
