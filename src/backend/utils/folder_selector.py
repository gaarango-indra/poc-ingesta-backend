import tkinter as tk
from tkinter import filedialog
import os
from typing import Optional
import requests
import asyncio

import json

class FolderSelector:
    """Clase para seleccionar y obtener la ruta de una carpeta."""

    _instance = None

    def __new__(cls):
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super(FolderSelector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Constructor de la clase que inicializa los componentes de la UI."""
        self.root = None

    def open_folder_dialog(self) -> Optional[str]:
        """Abre un cuadro de diálogo para seleccionar una carpeta.

        Returns:
            str | None: Ruta de la carpeta seleccionada, o None si no se selecciona ninguna.
        """
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta la ventana principal
        folder_path = filedialog.askdirectory()  # Abre el diálogo para seleccionar la carpeta
        self.root.destroy()

        if not folder_path or not os.path.isdir(folder_path):
            print("No se ha seleccionado una carpeta válida.")
            return None

        return folder_path

    def get_folder_path(self) -> Optional[str]:
        """Obtiene la ruta de la carpeta seleccionada, garantizando que es válida.

        Returns:
            str | None: Ruta de la carpeta seleccionada, o None si no se selecciona una ruta válida.
        """
        folder_path = self.open_folder_dialog()
        if folder_path:
            print(f"Carpeta seleccionada: {folder_path}")
            print(f"Tipo de dato: {type(folder_path)}")
            return folder_path
        return None

async def send_message(value):
    uri = "http://localhost:8000/post_parameters"
    response = requests.post(uri, json={"key": "folder_path", "value": value})

def main():
    selector = FolderSelector()
    selected_folder = selector.get_folder_path()
    print(f"Main folder path type: {type(selected_folder)}")
    asyncio.run(send_message(selected_folder))

if __name__ == "__main__":
    main()