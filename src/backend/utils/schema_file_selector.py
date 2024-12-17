from file_selector import FileSelector
import requests
import asyncio

class SchemaFileSelector(FileSelector):
    def __init__(self):
        super().__init__()

    def select_file(self):
        # Define el tipo de archivo permitido: .schema
        filetypes = [("Schema File", "*.schema")]
        # Llama al método select_file de la clase base con los tipos de archivo especificados
        return super().select_file(filetypes)

async def send_message(value):
    uri = "http://localhost:8000/post_parameters"
    response = requests.post(uri, json={"key": "schema_file_path", "value": value})

def main():
    selector = SchemaFileSelector()
    selected_schema_file = selector.select_file()
    print("schema_file_selector.py:", selected_schema_file)
    asyncio.run(send_message(selected_schema_file))

if __name__ == "__main__":
    main()