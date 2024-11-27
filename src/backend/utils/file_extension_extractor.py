import os
from pathlib import Path
from typing import Optional

class FileExtensionExtractor:
    """
    Class responsible for extracting the file extension from a given file path.
    """

    def __init__(self, file_path: str):
        self._file_path = file_path

    def get_extension(self) -> Optional[str]:
        """
        Extracts and returns the file extension if it exists, or None otherwise.

        Returns:
            Optional[str]: The file extension, or None if there is no extension.
        """
        if not self._is_valid_file_path():
            return None
        return self._extract_extension()

    def _is_valid_file_path(self) -> bool:
        """
        Checks if the provided file path is valid and exists.

        Returns:
            bool: True if the file path is valid and exists, False otherwise.
        """
        file = Path(self._file_path)
        return file.exists() and file.is_file()

    def _extract_extension(self) -> Optional[str]:
        """
        Extracts the file extension from the file path.

        Returns:
            Optional[str]: The file extension or None if the file has no extension.
        """
        _, extension = os.path.splitext(self._file_path)
        return extension[1:] if extension else None