import os
from typing import Any, Dict
from backend.utils.file_extension_extractor import FileExtensionExtractor
from backend.utils.file_analyzer import FileAnalyzer
from backend.utils.folder_generator import FolderGenerator
from backend.utils.schema_reader import SchemaReader as sr
from backend.utils.file_io import FileIO as fio
from backend.utils.type_to_name_mapper import TypeToNameMapper
from backend.utils.output_schema_writer import OutputSchemaWriter as osw
from backend.utils.general_pom_updater import GeneralPomUpdater
from backend.utils.module_pom_generator2 import ModulePomGenerator
from backend.utils.rep_json_writer import RepJsonWriter as rjw
from backend.openai_langchain.ai_conf_generator import AIConfGenerator
from backend.utils.conf_writer import ConfWriter as cw
from backend.utils.decimal_field_checker_csv import DecimalFieldCheckerCSV as csvdecimalchecker
from backend.utils.csv_decimal_validator import CSVDecimalValidator
from backend.utils.csv_date_field_extractor import CsvDateFieldExtractor
from backend.utils.data_formater_detector import DateFormatDetector
from backend.utils.schema_date_field_extractor import SchemaDateFieldExtractor

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
    
    def _read_schema_file(self):
        """Reads the .schema file."""
        schema_reader = sr(self.parameters["schema_file_path"])
        return schema_reader.read()
    
    def _get_file_extension(self):
        """Extracts the file extension."""
        extension_extractor = FileExtensionExtractor(self.parameters["data_sample_file_path"])
        return extension_extractor.get_extension().lower()

    def _analyze_file(self):
        """Analyzes the file to extract header and delimiter."""
        file_analyzer = FileAnalyzer(self.parameters["data_sample_file_path"])
        return file_analyzer.analyze_file()

    def _generate_folders(self, schema):
        """Generates the folder structure based on the schema."""
        print("Generating folder structure...")
        folder_generator = FolderGenerator(schema, self.parameters["folder_path"])
        return folder_generator.generate()
    
    def _update_general_pom(self, folder_path, uuaa):
        """Update general pom file"""
        general_pom_updater = GeneralPomUpdater(folder_path, uuaa)
        status_general_pom_updater = general_pom_updater.update_module_content()
    
    def _generate_module_pom(self, folder_path, uuaa):
        "Generate module pom file"
        module_pom_generator = ModulePomGenerator(folder_path, uuaa)
        module_pom_generator.generate_xml()
    
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
        
        processor = AIConfGenerator(api_key=self.api_key)
        
        try:
            if self.ingest_type == "raw":
                filled_template = processor.fill_template(self.ingest_type, template_conf, self.parameters, rules_conf, example_conf)
                #config_content = self._extract_config_from_template(str(filled_template))
                #cw.write_conf(config_content, folder_info['complete_path'], folder_info['name'])
                print(f"Plantilla Diligenciada")
            elif self.ingest_type == "master":
                print(f"date_format_dict")
                print(self.date_format_dict)
                filled_template = processor.fill_template(self.ingest_type, template_conf, self.parameters, rules_conf, example_conf, self.date_format_dict, self.grouped_fields)
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
        rules_raw_conf_path = os.path.join(base_dir, 'resources', 'rules', 'raw_conf_rules.txt')
        example_raw_conf_path = os.path.join(base_dir, 'resources', 'examples', 'raw_config.conf')

        raw_content = self._generate_configuration(folder_info, conf_raw_template_path, rules_raw_conf_path, example_raw_conf_path)
        return raw_content
    
    def _generate_master_configuration(self, folder_info):
        print("Ingresó a _generate_master_configuration")
        """Generates the configuration file based on templates and parameters."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        conf_master_template_path = os.path.join(base_dir, 'resources', 'templates', 'master_config_template.conf')
        rules_raw_conf_path = os.path.join(base_dir, 'resources', 'rules', 'master_conf_rules.txt')
        example_master_conf_path = os.path.join(base_dir, 'resources', 'examples', 'master_config.conf')

        master_content = self._generate_configuration(folder_info, conf_master_template_path, rules_raw_conf_path, example_master_conf_path)
        return master_content

    def _extract_config_from_template(self, raw_content):
        """Extracts the configuration content from the filled template."""
        initial_position = raw_content.find("'```")
        final_position = raw_content.rfind("```'")
        return raw_content[initial_position + 11: final_position - 2].replace(r'\n', '\n').replace(r"\'", "'")
    
    def _process_ingest(self):
        """Processes 'Ingesta RAW' type files."""
        #self.schema = self._read_schema_file()
        self.database = self.schema["database"]
        print(f"self.database de _process_ingest: {self.database}")

        header, delimiter = self._analyze_file()

        if self.database == "raw":
            file_extension = self._get_file_extension()
            self.parameters["input_format"] = file_extension
            print(f"Sample Data Extension: {file_extension}")

            if file_extension in ["csv", "txt"]:
                #header, delimiter = self._analyze_file()
                self.parameters["delimiter"] = delimiter
                self.parameters["header"] = header
                print(f"Header: {header}, Delimiter: {delimiter}")
        
        if self.database == "master":
            mapper = TypeToNameMapper(self.schema)
            self.grouped_fields = mapper.map_types_to_names()
            print(f"Parameters Processor self.grouped_fields: {self.grouped_fields}")
            csv_path = self.parameters["data_sample_file_path"]
            print(f"Parameters Processor csv_path: {csv_path}")

            if 'date' in self.grouped_fields:
                print("La llave 'date' existe en el diccionario.")
                data_type_date_extractor = CsvDateFieldExtractor(csv_path, self.grouped_fields, delimiter)
                value_input_date = data_type_date_extractor.get_first_date_field_value()
                date_format_detector = DateFormatDetector()
                sample_data_date_format = date_format_detector.detect_format(value_input_date)
                schema_date_field_extractor = SchemaDateFieldExtractor(self.schema)
                date_formats = schema_date_field_extractor.extract_date_formats()
                schema_date_format = list(date_formats[0].values())[0]
                #if sample_data_date_format != schema_date_format:
                if "date" in self.grouped_fields:
                    print("Hay date")
                    self.date_format_dict = {"input_date_format": sample_data_date_format, "output_date_format": schema_date_format}            
            else:
                print("La llave 'date' no existe en el diccionario.")
                self.date_format_dict = {"input_date_format": "", "output_date_format": ""}
            #csv_decimal_checker = csvdecimalchecker(csv_path, self.grouped_fields)
            #found_comma, found_dot = csv_decimal_checker.check_comma_and_dot()
            csv_decimal_validator = CSVDecimalValidator(csv_path, self.grouped_fields)
            found_comma, found_dot, decimal_symbol, correct_data = csv_decimal_validator.analyze_csv()
            self.parameters["found_comma"] = found_comma
            self.parameters["found_dot"] = found_dot
            self.parameters["decimal_symbol"] = decimal_symbol
        
        print(f"parameters_processor schema: {self.schema}")
        self.parameters["uuaa"] = self.schema["namespace"].lower()
        self.parameters["database"] = self.schema["database"]
        self.parameters["tabla"] = self.schema["name"]
        self.parameters["partitions"] = self.schema["partitions"]
        self.parameters["physicalPath"] = self.schema["physicalPath"]
        folder_info = self._generate_folders(self.schema)
        self._update_general_pom(self.parameters["folder_path"] ,self.parameters["uuaa"])
        self._generate_module_pom(self.parameters["folder_path"] ,self.parameters["uuaa"])
        self._create_json_and_schema_files(self.schema, folder_info)
        print(f"Tipo de Ingesta: {self.ingest_type}")
        if (self.ingest_type == "raw"):
            config_content = self._generate_raw_configuration(folder_info)
            print("\nRaw Config File Ok:")
            #print(config_content)
        elif (self.ingest_type == "master"):
            config_content = self._generate_master_configuration(folder_info)
            print("\nMaster Config File Ok:")
        print(f"Config content: {config_content}")

    async def process_parameters(self):
        """Asynchronously processes the received parameters."""
        # Log sample file path for debugging
        #print(f"Sample Path: {self.parameters['data_sample_file_path']}")
        
        self.schema = self._read_schema_file()
        print(f"Información de self.schema {self.schema}")
        print(f"Tipo de self.schema: {type(self.schema)}")

        # Process types
        process_type = self.parameters["process_type"]
        self.ingest_type = self.schema["database"]

        if process_type == "ingest":# and 
            #if ingest_type == "Ingesta RAW":
            self._process_ingest()