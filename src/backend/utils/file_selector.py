import tkinter as tk
from tkinter import filedialog

class FileSelector:
    def __init__(self):
        pass

    def select_file(self, filetypes):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        print(f"file_selector.py: {file_path}")
        root.destroy()
        return file_path