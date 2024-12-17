import xml.etree.ElementTree as ET
import os


class ModulePomGenerator:
    """
    A class to process XML files by extracting specific values from an input XML file,
    replacing placeholders in a template XML, and generating an output XML file.

    Attributes:
        folder_path (str): The folder path where input XML and template XML are located.
        uuaa (str): The user agent value to replace in the template.
        input_xml (str): The path to the input XML file (general pom.xml).
        template_xml (str): The path to the template XML file (module_pom.xml).
        output_xml (str): The path where the output XML file (module pom.xml) will be saved.
    """

    def __init__(self, folder_path: str, uuaa: str):
        """
        Initializes the ModulePomGenerator with the folder path and user agent.

        Args:
            folder_path (str): The folder path containing XML files.
            uuaa (str): The user agent string to be used in the template replacement.
        """
        self.folder_path = folder_path
        self.uuaa = uuaa
        self.input_xml = os.path.join(folder_path, 'pom.xml')
        backend_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(f"module_pom_generator Script Folder: {backend_folder_path}")
        print(f"Ruta del directorio del script ModulePomGenerator: {backend_folder_path}")
        self.template_xml = os.path.join(backend_folder_path, 'resources', 'templates', 'module_pom.xml')
        self.output_xml = os.path.join(folder_path, uuaa, 'pom.xml')

    def _get_values_from_input_xml(self) -> tuple:
        """
        Extracts the necessary values from the input XML file (p1.xml).

        Returns:
            tuple: A tuple containing groupId, artifactId, and version from the input XML.

        Raises:
            ValueError: If required elements are missing or if XML parsing fails.
        """
        try:
            tree = ET.parse(self.input_xml)
            root = tree.getroot()

            # Define the namespace dictionary
            namespaces = {'ns0': 'http://maven.apache.org/POM/4.0.0'}

            # Debugging: print the XML to verify its structure
            print(ET.tostring(root, encoding="unicode"))

            # Find groupId inside parent and project
            group_id_element = root.find('.//ns0:parent/ns0:groupId', namespaces)
            print(f"group_id_element: {group_id_element.text}")
            artifact_id_elements = root.findall('.//ns0:artifactId', namespaces)
            print(f"artifact_id_element: {artifact_id_elements[1].text}")
            version_elements = root.findall('.//ns0:version', namespaces)
            print(f"version_element: {version_elements[1].text}")

            # Check if any of the elements are missing
            if group_id_element is None:
                raise ValueError("Missing 'groupId' in the input XML.")
            if artifact_id_elements is None:
                raise ValueError("Missing 'artifactId' in the input XML.")
            if version_elements is None:
                raise ValueError("Missing 'version' in the input XML.")

            group_id = group_id_element.text
            artifact_id = artifact_id_elements[1].text
            version = version_elements[1].text

            return group_id, artifact_id, version

        except (ET.ParseError, ValueError) as e:
            raise ValueError(f"Error parsing input XML: {e}")

    def _load_template(self) -> str:
        """
        Loads the template XML file.

        Returns:
            str: The content of the template XML file.
        """
        try:
            with open(self.template_xml, 'r') as file:
                template_content = file.read()
            return template_content
        except FileNotFoundError:
            raise FileNotFoundError(f"Template XML file {self.template_xml} not found.")

    def _replace_placeholders(self, template_content: str, group_id: str, artifact_id: str, version: str) -> str:
        """
        Replaces the placeholders in the template content with the provided values.

        Args:
            template_content (str): The template XML content.
            group_id (str): The groupId value to replace the placeholder.
            artifact_id (str): The artifactId value to replace the placeholder.
            version (str): The version value to replace the placeholder.

        Returns:
            str: The modified XML content with placeholders replaced.
        """
        template_content = template_content.replace("{parent_gp_groupId}", group_id)
        template_content = template_content.replace("{gp_artifactId}", artifact_id)
        template_content = template_content.replace("{gp_version}", version)
        template_content = template_content.replace("{uuaa}", self.uuaa)

        return template_content

    def _write_output_xml(self, modified_content: str) -> None:
        """
        Writes the modified XML content to the output XML file (p2.xml).

        Args:
            modified_content (str): The final XML content to be written to the output file.
        """
        try:
            with open(self.output_xml, 'w') as file:
                file.write(modified_content)
        except IOError as e:
            raise IOError(f"Error writing to output XML file: {e}")

    def generate_xml(self) -> None:
        """
        Coordinates the extraction of values, loading the template, replacing placeholders,
        and generating the output XML file.

        Raises:
            ValueError: If there is an error in parsing the input XML.
            FileNotFoundError: If the template XML file is not found.
            IOError: If there is an error writing the output XML file.
        """
        group_id, artifact_id, version = self._get_values_from_input_xml()
        template_content = self._load_template()
        modified_content = self._replace_placeholders(template_content, group_id, artifact_id, version)
        self._write_output_xml(modified_content)
        print(f"File {self.output_xml} has been successfully generated.")