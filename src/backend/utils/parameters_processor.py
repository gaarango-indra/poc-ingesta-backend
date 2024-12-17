import os
from typing import Any, Dict
from backend.utils.file_extension_extractor import FileExtensionExtractor
from backend.utils.file_analyzer import FileAnalyzer
from backend.utils.folder_generator import FolderGenerator
from backend.utils.schema_reader import SchemaReader as sr
from backend.utils.file_io import FileIO as fio
#from backend.utils.fields_data_type import FieldsDataType
from backend.utils.type_to_name_mapper import TypeToNameMapper
from backend.utils.output_schema_writer import OutputSchemaWriter as osw
from backend.utils.rep_json_writer import RepJsonWriter as rjw
from backend.openai_langchain.ai_conf_generator import AIConfGenerator
from backend.utils.conf_writer import ConfWriter as cw
from backend.utils.decimal_field_checker_csv import DecimalFieldCheckerCSV as csvdecimalchecker

class ParameterProcessor:
    """Asynchronous processor for handling parameters related to data ingestion."""

    def __init__(self, parameters: dict, api_key: str):
        """
        Initialize the ParameterProcessor with parameters and API key.
        
        :param parameters: Dictionary containing processing parameters.
        :param api_key: API key for OpenAI processor.
        """
        self.parameters = parameters
        self.api_key = api_key

    async def process_parameters(self):
        """Asynchronously processes the received parameters."""
        # Log sample file path for debugging
        #print(f"Sample Path: {self.parameters['data_sample_file_path']}")

<<<<<<< HEAD
        
        self.schema = self._read_schema_file()

=======
>>>>>>> 2e362e34245e2329e768318ea0d40dab0fb234c6
        # Process types
        process_type = self.parameters["process_type"]
        ingest_type = self.parameters["ingest_type"]
        self.ingest_type = ingest_type

        if process_type == "ingest":# and 
            #if ingest_type == "Ingesta RAW":
            self._process_ingest_raw()

    def _process_ingest_raw(self):
        """Processes 'Ingesta RAW' type files."""
<<<<<<< HEAD
        #self.schema = self._read_schema_file()
=======
        self.schema = self._read_schema_file()
>>>>>>> 2e362e34245e2329e768318ea0d40dab0fb234c6
        if self.ingest_type == "Ingesta RAW":
            file_extension = self._get_file_extension()
            print(f"Sample Data Extension: {file_extension}")

            if file_extension in ["csv", "txt"]:
                header, delimiter = self._analyze_file()
                self.parameters["delimiter"] = delimiter
                self.parameters["header"] = header
                #print(f"Header: {header}, Delimiter: {delimiter}")
        
        if self.ingest_type == "Ingesta Master":
            mapper = TypeToNameMapper(self.schema)
            self.grouped_fields = mapper.map_types_to_names()
            print(f"Parameters Processor self.grouped_fields: {self.grouped_fields}")
            csv_path = self.parameters["data_sample_file_path"]
            print(f"Parameters Processor csv_path: {csv_path}")
            csv_decimal_checker = csvdecimalchecker(csv_path, self.grouped_fields)
            found_comma, found_dot = csv_decimal_checker.check_comma_and_dot()
            self.parameters["found_comma"] = found_comma
            self.parameters["found_dot"] = found_dot
        
        print(f"parameters_processor schema: {self.schema}")
        self.parameters["uuaa"] = self.schema["namespace"].lower()
        self.parameters["database"] = self.schema["database"]
        self.parameters["tabla"] = self.schema["name"]
        self.parameters["partitions"] = self.schema["partitions"]
        self.parameters["physicalPath"] = self.schema["physicalPath"]
        folder_info = self._generate_folders(self.schema)
        self._create_json_and_schema_files(self.schema, folder_info)
        print(f"Tipo de Ingesta: {self.ingest_type}")
        if (self.ingest_type == "Ingesta RAW"):
            config_content = self._generate_raw_configuration(folder_info)
            print("\nRaw Config File Ok:")
            #print(config_content)
        elif (self.ingest_type == "Ingesta Master"):
            config_content = self._generate_master_configuration(folder_info)
            print("\nMaster Config File Ok:")
        print(f"Config content: {config_content}")

    def _get_file_extension(self):
        """Extracts the file extension."""
        extension_extractor = FileExtensionExtractor(self.parameters["data_sample_file_path"])
        return extension_extractor.get_extension().lower()

    def _analyze_file(self):
        """Analyzes the file to extract header and delimiter."""
        file_analyzer = FileAnalyzer(self.parameters["data_sample_file_path"])
        return file_analyzer.analyze_file()

    def _read_schema_file(self):
        """Reads the .schema file."""
        schema_reader = sr(self.parameters["schema_file_path"])
        return schema_reader.read()

    def _generate_folders(self, schema):
        """Generates the folder structure based on the schema."""
        print("Generating folder structure...")
        folder_generator = FolderGenerator(schema, self.parameters["folder_path"])
        return folder_generator.generate()

    def _create_json_and_schema_files(self, schema, folder_info):
        """Creates necessary JSON and schema files."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_template_path = os.path.join(base_dir, 'resources', 'templates', 'json_template.json')
        conf_raw_template_path = os.path.join(base_dir, 'resources', 'templates', 'config_raw_template.conf')

        write_output_schema_file = osw.write_schema(schema, folder_info['complete_path'], folder_info['name'])

        write_rep_json_file = rjw(json_template_path)
        write_rep_json_file.write_to_json(
            folder_info['complete_path'],
            folder_info['name'],
            folder_info['uuaa'],
            self.parameters["code_schema"],
            folder_info['database'],
            "S"
        )

    def _generate_configuration(self, folder_info, conf_template_path, rules_conf_path, example_conf_path):
        print("Ingresó a _generate_configuration")
        # Reading template and rule files
        template_conf = fio.read_txt(conf_template_path)
        rules_conf = fio.read_txt(rules_conf_path)
        example_conf = fio.read_txt(example_conf_path)
        #fdt = FieldsDataType(self.schema)
        #grouped_fields = fdt.get_all_grouped_fields()
        #mapper = TypeToNameMapper(self.schema)
        #self.grouped_fields = mapper.map_types_to_names()
        # Display the result
<<<<<<< HEAD
        #print("Type to Name Mapping:", self.grouped_fields)
        #print(f"Ingest type de _generate_configuration: {self.ingest_type}")
=======
        print("Type to Name Mapping:", self.grouped_fields)
        print(f"Ingest type de _generate_configuration: {self.ingest_type}")
>>>>>>> 2e362e34245e2329e768318ea0d40dab0fb234c6
        processor = AIConfGenerator(api_key=self.api_key)
        try:
            if self.ingest_type == "Ingesta RAW":
                filled_template = processor.fill_template(self.ingest_type, template_conf, self.parameters, rules_conf, example_conf)
                #config_content = self._extract_config_from_template(str(filled_template))
                #cw.write_conf(config_content, folder_info['complete_path'], folder_info['name'])
                print(f"Plantilla Diligenciada")
            elif self.ingest_type == "Ingesta Master":
                filled_template = processor.fill_template(self.ingest_type, template_conf, self.parameters, rules_conf, example_conf, self.grouped_fields)
                #config_content = self._extract_config_from_template(str(filled_template))
                #cw.write_conf(config_content, folder_info['complete_path'], folder_info['name'])
            print(f"Filled <template: \n{filled_template}")
            config_content = self._extract_config_from_template(str(filled_template))
            cw.write_conf(config_content, folder_info['complete_path'], folder_info['name'])
            return config_content
        except Exception as e:
            print("An error occurred while filling the template:", e)
    
    def _generate_raw_configuration(self, folder_info):
        """Generates the configuration file based on templates and parameters."""
        print("Ingresó a _generate_raw_configuration")
        base_dir = os.path.dirname(os.path.dirname(__file__))
        conf_raw_template_path = os.path.join(base_dir, 'resources', 'templates', 'config_raw_template.conf')
        rules_raw_conf_path = os.path.join(base_dir, 'resources', 'rules', 'raw_conf.txt')
        example_raw_conf_path = os.path.join(base_dir, 'resources', 'examples', 'raw_config.conf')

        raw_content = self._generate_configuration(folder_info, conf_raw_template_path, rules_raw_conf_path, example_raw_conf_path)
        return raw_content
    
    def _generate_master_configuration(self, folder_info):
        print("Ingresó a _generate_master_configuration")
        """Generates the configuration file based on templates and parameters."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        conf_master_template_path = os.path.join(base_dir, 'resources', 'templates', 'master_config_template.conf')
        rules_raw_conf_path = os.path.join(base_dir, 'resources', 'rules', 'raw_conf.txt')
        example_master_conf_path = os.path.join(base_dir, 'resources', 'examples', 'master_config.conf')

        master_content = self._generate_configuration(folder_info, conf_master_template_path, rules_raw_conf_path, example_master_conf_path)
        return master_content

    def _extract_config_from_template(self, raw_content):
        """Extracts the configuration content from the filled template."""
        initial_position = raw_content.find("'```")
        final_position = raw_content.rfind("```'")
        return raw_content[initial_position + 11: final_position - 2].replace(r'\n', '\n')
