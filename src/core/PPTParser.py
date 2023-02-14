from zipfile import ZipFile
from pathlib import Path
from lxml import etree
import csv


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
        return list(self.unpack_dir.glob("ppt/slides/*.xml"))

    # returns a dictionary of the text in a {title: [content]} format from the given filepath of a slide XML file
    def extract_text_slide_filepath(self, slide_filepath: Path) -> dict | None:
        # remove "slide" from slide12 to isolated the slide's number
        slide_num = slide_filepath.stem.replace("slide", "")

        # lxml api allows parsing from python Path objects directly
        tree = etree.parse(slide_filepath)
        root = tree.getroot()
        p_tags = root.findall(".//a:p", namespaces=root.nsmap)
        text_entries = []

        # for each p-tag, discover internal p tags to rebuild the "full"/displayed string
        for p_tag in p_tags:
            combined_text = ""
            t_tags = p_tag.findall(".//a:t", namespaces=root.nsmap)
            for t_tag in t_tags:
                combined_text += t_tag.text

            text_entries.append(combined_text.strip())

        if len(text_entries) > 0:
            return {slide_num: text_entries}

    def extract_text(self) -> None:
        extracted_text = {}
        slide_paths = self.get_slide_filepaths()
        for path in slide_paths:
            slide_dict = self.extract_text_slide_filepath(path)
            if (slide_dict is not None):
                extracted_text.update(slide_dict)

        self.write_extracted_text_to_csv(extracted_text)

    def write_extracted_text_to_csv(self, extracted_text: dict) -> None:
        csv_filepath = str(self.unpack_dir) + ".csv"
        with open(csv_filepath, "w") as csvfile:
            csv_writer = csv.writer(
                csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
            sorted_keys = sorted(extracted_text.keys(), key=lambda x: int(x))
            for slide_num in sorted_keys:
                for text_entry in extracted_text[slide_num]:
                    # exclude any entries that are empty
                    if (len(text_entry) == 0):
                        continue

                    # exclude any entries that are just the slide number
                    if (text_entry == slide_num):
                        continue

                    csv_writer.writerow([slide_num, text_entry])
