from zipfile import ZipFile
from pathlib import Path

class PPTParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def unpack_file(self):
        with ZipFile(self.filepath) as zFile:
            zFile.extractall(path=(self.filepath.parent / self.filepath.stem))
