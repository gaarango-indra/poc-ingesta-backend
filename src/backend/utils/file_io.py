import json
import os

class FileIO:
    @staticmethod
    def write_json(data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def read_txt(filepath):
        # Abre el archivo en modo de lectura ('r')
        with open(filepath, "r") as file:
            content = file.read()
            return content
        
    @staticmethod
    def write_txt(data, file_path):
        with open(file_path, "w") as file:
            file.write(data)

    @staticmethod
    def write_schema_file(data, folder_path, name):
        file_path = os.path.join(folder_path, f"{name}.output.schema")
        FileIO.write_json(data, file_path)

    @staticmethod
    def write_json_file(data, folder_path, name):
        file_path = os.path.join(folder_path, f"{name}.rep.json")
        FileIO.write_json(data, file_path)

    @staticmethod
    def write_conf_file(data, folder_path, name):
        file_path = os.path.join(folder_path, f"{name}.rep.conf")
        FileIO.write_json(data, file_path)