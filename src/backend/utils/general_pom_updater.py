import re
from pathlib import Path
from typing import Optional


class GeneralPomUpdater:
    """
    This class is responsible for updating the content inside <module></module> tags
    in an XML file named 'pom.xml' (general pom). It replaces the existing content with the value
    provided in the 'uuaa' parameter.
    """

    def __init__(self, folder_path: str, uuaa: str) -> None:
        """
        Initialize the ModuleUpdater with the base folder path and the uuaa value.

        :param folder_path: The base folder path where 'pom.xml' is located.
        :param uuaa: The value to insert inside the <module></module> tags.
        :raises ValueError: If the folder_path or uuaa is empty.
        """
        if not folder_path:
            raise ValueError("folder_path cannot be empty.")
        if not uuaa:
            raise ValueError("ua cannot be empty.")

        self.folder_path: Path = Path(folder_path)
        self.uuaa: str = uuaa
        self.file_name: str = "pom.xml"
        self.pattern: re.Pattern = re.compile(r"(<module>)(.*?)(</module>)", flags=re.DOTALL)

    def update_module_content(self) -> bool:
        """
        Update the <module></module> content in the 'pom.xml' file with the uuaa value.

        :return: True if the content was updated successfully, False otherwise.
        """
        file_path = self.folder_path / self.file_name

        if not file_path.is_file():
            # Logically, we might raise an exception or just return False.
            # Here we return False to indicate failure gracefully.
            return False

        original_content: Optional[str] = self._read_file(file_path)
        if original_content is None:
            return False

        updated_content: str = self._replace_module_content(original_content, self.uuaa)

        if updated_content != original_content:
            return self._write_file(file_path, updated_content)

        return True

    def _read_file(self, file_path: Path) -> Optional[str]:
        """
        Read the content of the file.

        :param file_path: Path to the file to be read.
        :return: The file content as a string, or None if an error occurs.
        """
        try:
            with file_path.open('r', encoding='utf-8') as file:
                return file.read()
        except (OSError, UnicodeDecodeError):
            # In a real-world scenario, we might log this error.
            return None

    def _write_file(self, file_path: Path, content: str) -> bool:
        """
        Write content to the specified file.

        :param file_path: Path to the file to be written.
        :param content: The content to write.
        :return: True if the file was written successfully, False otherwise.
        """
        try:
            with file_path.open('w', encoding='utf-8') as file:
                file.write(content)
            return True
        except OSError:
            # In a real-world scenario, we might log this error.
            return False

    def _replace_module_content(self, original_content: str, uuaa_value: str) -> str:
        """
        Replace the content inside <module></module> tags with the UA value.

        :param original_content: The original XML content.
        :param ua_value: The new UA value to be inserted.
        :return: The updated content.
        """
        # Using a backreference approach where:
        # \1 corresponds to <module>
        # \3 corresponds to </module>
        # We replace the inner text with ua_value
        return self.pattern.sub(rf"\1{uuaa_value}\3", original_content)
