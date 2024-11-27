import os
from backend.utils.file_io import FileIO as fio

class OutputSchemaWriter:
    #def __init__(self):
    
    def write_schema(data, folder_path, name):
        file_path = os.path.join(folder_path, f"{name}.output.schema")
        fio.write_json(data, file_path)