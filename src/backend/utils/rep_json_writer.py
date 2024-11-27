import os
import json
#from string import Template

class RepJsonWriter:
    """Clase para crear y escribir archivos JSON de configuración a partir de una plantilla."""

    def __init__(self, template_path: str):
        """
        Inicializa la clase con la ruta de la plantilla JSON.

        :param template_path: Ruta al archivo de plantilla JSON.
        :raises FileNotFoundError: Si la plantilla no se encuentra.
        :raises ValueError: Si el archivo de plantilla no es un JSON válido.
        """
        if not os.path.isfile(template_path):
            raise FileNotFoundError(f"The template file '{template_path}' does not exist.")
        self.template_path = template_path
        self.template_data = self._load_template()

    def _load_template(self) -> dict:
        """
        Carga la plantilla JSON desde el archivo especificado.

        :return: La estructura de datos JSON de la plantilla.
        :raises ValueError: Si el archivo de plantilla no es un JSON válido.
        """
        try:
            with open(self.template_path, 'r') as template_file:
                return json.load(template_file)
        except json.JSONDecodeError as e:
            raise ValueError(f"The template file '{self.template_path}' is not a valid JSON: {e}")

    def _validate_parameters(self, folder_path: str, name: str, uuaa: str, code_schema: str, database: str, size_value: str):
        """
        Valida los parámetros de entrada para asegurarse de que son del tipo correcto.

        :param folder_path: Ruta de la carpeta.
        :param name: Nombre base.
        :param uuaa: Identificador UUAA.
        :param code_schema: Código del esquema.
        :param database: Nombre de la base de datos.
        :param size_value: Valor de tamaño.
        :raises ValueError: Si algún parámetro no es de tipo str.
        :raises FileNotFoundError: Si el folder_path no existe.
        """
        if not all(isinstance(param, str) for param in [folder_path, name, uuaa, code_schema, database, size_value]):
            raise ValueError("All parameters must be of type str.")
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

    def _generate_job_id(self, name: str, uuaa: str, code_schema: str, database: str) -> str:
        """
        Genera un ID único de trabajo (job_id) basado en los parámetros proporcionados.

        :param name: Nombre base.
        :param uuaa: Identificador UUAA.
        :param code_schema: Código del esquema.
        :param database: Nombre de la base de datos.
        :return: El ID de trabajo generado.
        """
        second_underscore_index = name.find('_', name.find('_') + 1)
        project_name = name[second_underscore_index + 1:].replace('_', '')
        letter_ingest = database[0]
        return f"{uuaa}-{code_schema}-krb-in{letter_ingest}-{project_name}r-01"

    def write_to_json(self, folder_path: str, name: str, uuaa: str, code_schema: str, database: str, size_value: str):
        """
        Escribe el archivo JSON basado en la plantilla y parámetros específicos.
        
        :param folder_path: Ruta de la carpeta para almacenar el JSON.
        :param name: Nombre base para el archivo JSON.
        :param uuaa: Identificador UUAA.
        :param code_schema: Código del esquema.
        :param database: Nombre de la base de datos.
        :param size_value: Valor de tamaño.
        :raises ValueError: Si los parámetros no son válidos.
        :raises FileNotFoundError: Si la carpeta especificada no existe.
        """
        # Validar parámetros
        self._validate_parameters(folder_path, name, uuaa, code_schema, database, size_value)
        
        # Generar job_id
        job_id = self._generate_job_id(name, uuaa, code_schema, database)
        
        # Diccionario de valores a reemplazar en el JSON
        replacements = {
            "_id": job_id,
            "description": f"Job {job_id} created with App.",
            "size": size_value,
            "params.configUrl": (
                f"${{repository.endpoint.vdc}}/${{repository.repo.schemas}}/kirby/{code_schema}/{uuaa}/{database}/{name}/${{version}}/{name}.rep.conf"
            )
        }
        
        # Reemplazar valores en el JSON
        for key, value in replacements.items():
            # Navega por el JSON para ajustar claves anidadas (como "params.configUrl")
            keys = key.split(".")
            temp_data = self.template_data
            for k in keys[:-1]:
                temp_data = temp_data.setdefault(k, {})  # Crea subdiccionarios si no existen
            temp_data[keys[-1]] = value  # Asigna el valor final

        # Definir la ruta del archivo de salida
        file_path = os.path.join(folder_path, f"{name}.rep.json")

        # Guardar en archivo JSON con manejo de errores
        try:
            with open(file_path, 'w') as file:
                json.dump(self.template_data, file, indent=4)
            print(f"JSON content written to: {file_path}")
        except (OSError, json.JSONEncodeError) as e:
            print(f"Failed to write JSON to {file_path}: {e}")
