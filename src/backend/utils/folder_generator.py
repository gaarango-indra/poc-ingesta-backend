import os
import json

class FolderGenerator:
    def __init__(self, schema, base_output_path):
        self.schema = schema
        self.base_output_path = base_output_path

    def create_folders(self, structure):

        """
        Create the folder structure based on the JSON data.
        """

        self.data = structure
        self.uuaa = self.data.get('namespace', '').lower()
        self.name = self.data.get('name')
        self.database = self.data.get('database')
        self.partitions = self.data.get('partitions')
        self.output_path = self.data.get('physicalPath')

        if not self.uuaa or not self.name:
            print("JSON is missing 'uuaa' or 'name'.")
            return

        structure = [
            self.base_output_path,
            self.uuaa,
            "src",
            "main",
            "resources",
            "kirby",
            self.uuaa,
            self.name,
            self.database
        ]

        complete_path = os.path.join(*structure)

        if not os.path.exists(complete_path):
            os.makedirs(complete_path)
            print(f"Folder structure created: {complete_path}")
        else:
            print(f"Folder structure already exists: {complete_path}")
        return ({"complete_path": complete_path,
                 "uuaa": self.uuaa,
                 "name": self.name,
                 "database": self.database,
                 "partitions": self.partitions,
                 "output_path": self.output_path
                 })
        '''
        for key, value in structure.items():
            folder_path = os.path.join(base_path, key)
            os.makedirs(folder_path, exist_ok=True)
            if isinstance(value, dict):
                self.create_folders(folder_path, value)
        '''
    
    def generate(self):
        complete_path = self.create_folders(self.schema)
        return complete_path

# Usage
# generator = FolderGenerator('path/to/initial_schema.schema')
# generator.generate()
