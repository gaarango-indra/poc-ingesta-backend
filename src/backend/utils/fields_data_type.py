from typing import Optional, List, Dict
from pydantic import BaseModel

class FieldSchema(BaseModel):
    """
    Data model for schema fields based on the provided JSON structure.
    """
    name: str
    type: str
    legacy_name: str
    logical_format: str
    format: Optional[str] = None
    deleted: bool
    metadata: bool
    locale: str
    default: str


class FieldsDataType:
    """
    Class to load schema and group fields by their data type automatically.
    """
    def __init__(self, schema: dict):
        self.field_schemas = self._load_fields(schema)
        self.grouped_fields = self._group_fields_by_type()

    @staticmethod
    def _load_fields(schema: dict) -> List[FieldSchema]:
        """
        Loads fields from schema and validates their structure.
        """
        data = schema.get("fields", [])
        return [FieldSchema(**item) for item in data]

    def _group_fields_by_type(self) -> Dict[str, List[FieldSchema]]:
        """
        Groups fields by their data type.
        """
        grouped = {}
        for field in self.field_schemas:
            field_type = field.type
            if field_type not in grouped:
                grouped[field_type] = []
            grouped[field_type].append(field)
        return grouped

    def get_all_grouped_fields(self) -> Dict[str, List[FieldSchema]]:
        """
        Returns all fields grouped by their data type.
        """
        return self.grouped_fields
