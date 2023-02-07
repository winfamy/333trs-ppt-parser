from zipfile import ZipFile
from pathlib import Path

class PPTParser:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.unpack_dir = None

    # unzips the file specified in the constructor
    def unpack_file(self) -> None:
        with ZipFile(self.filepath) as zFile:
            self.unpack_dir = self.filepath.parent / self.filepath.stem
            zFile.extractall(path=self.unpack_dir)

    # returns a list of the slide filepaths from the unpacked dir
    def get_slide_filepaths(self) -> list:
        pass

    # returns a dictionary of the text in a {title: [content]} format from the given filepath of a slide XML file
    def parse_text_from_slide_filepath(self, slide_filepath: Path) -> dict:
        pass



