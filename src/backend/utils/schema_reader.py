import json

class SchemaReader:
    def __init__(self, schema_path):
        self.schema_path = schema_path

    def read(self):
        with open(self.schema_path, 'r') as file:
            schema = json.load(file)
        return schema
