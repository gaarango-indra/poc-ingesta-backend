import os
from backend.utils.file_io import FileIO as fio

class ConfWriter:
    #def __init__(self):
    
    def write_conf(data, folder_path, name):
        file_path = os.path.join(folder_path, f"{name}.rep.conf")
        fio.write_txt(data, file_path)