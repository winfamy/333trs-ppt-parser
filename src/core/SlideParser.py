from pathlib import Path
from lxml import etree


"""
Currently does nothing, here for future code organization
"""


class SlideParser:
    def __init__(self, slide_filepath: Path):
        self.slide_filepath = slide_filepath
        self.etree = etree.parse(slide_filepath)

    def parse(self, features: bool = False):
        pass

    def extract_features(self):
        pass
