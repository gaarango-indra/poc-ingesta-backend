import os
import xml.etree.ElementTree as ET
import json

class ModulePomGenerator:
    """
    A class to process XML files, convert them to JSON, extract specific data, 
    and generate an XML file based on a template.
    Implements SOLID principles, clean code practices, and adheres to PEP8 standards.
    """

    def __init__(self, folder_path: str, uuaa: str):
        """
        Initialize the ModulePomGenerator with a folder path and a user agent.

        :param folder_path: Path to the folder containing the template and XML files.
        :param uuaa: A user agent string to replace placeholders in the template.
        """
        self.folder_path = folder_path
        self.uuaa = uuaa
        self.namespace = {'ns0': 'http://maven.apache.org/POM/4.0.0'}

    def read_xml(self) -> ET.Element:
        """
        Reads an XML file and returns its root element.

        :param file_name: Name of the XML file to read.
        :return: Root element of the XML file.
        """
        try:
            file_path = os.path.join(self.folder_path, 'pom.xml')
            tree = ET.parse(file_path)
            return tree.getroot()
        except Exception as e:
            raise RuntimeError(f"Error reading XML file general pom.xml: {e}")

    def xml_to_dict(self, xml_root: ET.Element) -> dict:
        """
        Converts an XML root element into a dictionary.

        :param xml_root: Root element of the XML file.
        :return: Dictionary representation of the XML file.
        """
        def element_to_dict(element):
            children = list(element)
            if not children:
                return element.text.strip() if element.text else None
            return {
                child.tag.split('}')[-1]: element_to_dict(child) for child in children
            }
        print(f"XML to Dict")
        print({xml_root.tag.split('}')[-1]: element_to_dict(xml_root)})
        return {xml_root.tag.split('}')[-1]: element_to_dict(xml_root)}

    def extract_data_from_dict(self, xml_dict: dict) -> dict:
        """
        Extracts specific data from the XML dictionary.

        :param xml_dict: Dictionary representation of the XML file.
        :return: Dictionary containing extracted data.
        """
        try:
            project = xml_dict.get("project", {})
            parent = project.get("parent", {})

            group_id = parent.get("groupId")
            artifact_id = project.get("artifactId")
            version = project.get("version")

            if not (group_id and artifact_id and version):
                raise ValueError("Missing required elements in the XML dictionary.")

            return {
                "parent_gp_groupId": group_id,
                "gp_artifactId": artifact_id,
                "gp_version": version
            }
        except Exception as e:
            raise RuntimeError(f"Error extracting data from XML dictionary: {e}")
    
    def extract_data_from_xml(self, xml_root: ET.Element) -> dict:
        """
        Extracts specific data directly from the XML using namespaces.

        :param xml_root: Root element of the XML file.
        :return: Dictionary containing extracted data.
        """
        try:
            parent = xml_root.find("ns0:parent", self.namespace)

            group_id = parent.find("ns0:groupId", self.namespace).text if parent is not None else None
            artifact_id = xml_root.find("ns0:artifactId", self.namespace).text
            version = xml_root.find("ns0:version", self.namespace).text

            if not (group_id and artifact_id and version):
                raise ValueError("Missing required elements in the XML file.")

            return {
                "parent_gp_groupId": group_id,
                "gp_artifactId": artifact_id,
                "gp_version": version
            }
        except Exception as e:
            raise RuntimeError(f"Error extracting data from XML: {e}")

    def load_template(self) -> str:
        """
        Loads the content of a template file.

        :param template_name: Name of the template file.
        :return: Content of the template file as a string.
        """
        try:
            backend_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            template_path = os.path.join(backend_folder_path, 'resources', 'templates', 'module_pom.xml')
            with open(template_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise RuntimeError(f"Error loading template module_pom.xml: {e}")

    def generate_output_xml(self, template_content: str, data: dict) -> None:
        """
        Generates an XML file by replacing placeholders in the template content.

        :param template_content: Content of the template.
        :param data: Dictionary with data to replace placeholders.
        :param output_file: Name of the output XML file.
        """
        try:
            content = template_content.replace("{parent_gp_groupId}", data["parent_gp_groupId"])
            content = content.replace("{gp_artifactId}", data["gp_artifactId"])
            content = content.replace("{gp_version}", data["gp_version"])
            content = content.replace("{uuaa}", self.uuaa)

            output_path = os.path.join(self.folder_path, self.uuaa, 'pom.xml')
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(content)

            print(f"Output XML file module pom.xml created successfully.")
        except Exception as e:
            raise RuntimeError(f"Error generating output XML file module pom.xml: {e}")

    def process_files(self) -> None:
        """
        Main method to process the XML files and generate the output XML file.

        :param input_file: Name of the input XML file.
        :param template_file: Name of the template XML file.
        :param output_file: Name of the output XML file.
        """
        try:
            xml_root = self.read_xml()
            data = self.extract_data_from_xml(xml_root)
            template_content = self.load_template()
            self.generate_output_xml(template_content, data)
        except Exception as e:
            raise RuntimeError(f"Error processing files: {e}")
    
    def generate_xml(self):
        self.process_files()
