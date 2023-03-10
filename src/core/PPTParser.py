from zipfile import ZipFile
from pathlib import Path
from lxml import etree
import csv
import json


class PPTParser:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.unpack_dir = None
        self.parse_mode = None

    # unzips the file specified in the constructor
    def unpack_file(self) -> str:
        with ZipFile(self.filepath) as zFile:
            self.unpack_dir = self.filepath.parent / self.filepath.stem
            zFile.extractall(path=self.unpack_dir)
        return self.unpack_dir

    # returns a list of the slide filepaths from the unpacked dir
    def get_slide_filepaths(self) -> list:
        return list(self.unpack_dir.glob("ppt/slides/*.xml"))

    # returns a dictionary of the text in a {title: [content]} format from the given filepath of a slide XML file
    def extract_text_slide_filepath(self, slide_filepath: Path) -> dict:
        # remove "slide" from slide12 to isolated the slide's number
        slide_num = slide_filepath.stem

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

    def rebuild_p_tag(self, p_tag, nsmap) -> list:
        # for each p-tag, discover internal p tags to rebuild the "full"/displayed string
        combined_text = ""
        t_tags = p_tag.findall(".//a:t", namespaces=nsmap)
        for t_tag in t_tags:
            combined_text += t_tag.text

        return combined_text

    def extract_text(self) -> None:
        self.parse_mode = "text"
        extracted_text = {}
        slide_paths = self.get_slide_filepaths()
        extracted_text = self._extract_text(slide_paths)

        self.write_extracted_text_to_csv(extracted_text)

    def _extract_text(self, slide_paths) -> dict:
        extracted_text = {}
        for path in slide_paths:
            slide_dict = self.extract_text_slide_filepath(path)
            if (slide_dict is not None):
                extracted_text.update(slide_dict)

        return extracted_text

    def write_extracted_text_to_csv(self, extracted_text: dict) -> None:
        csv_filepath = str(self.unpack_dir) + ".csv"
        with open(csv_filepath, "w") as csvfile:
            csv_writer = csv.writer(
                csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
            sorted_keys = sorted(extracted_text.keys(), key=lambda x: int(x.replace("slide", "")))
            for slide_num in sorted_keys:
                for text_entry in extracted_text[slide_num]:
                    # exclude any entries that are empty
                    if (len(text_entry) == 0):
                        continue

                    # exclude any entries that are just the slide number
                    if (text_entry == slide_num):
                        continue

                    csv_writer.writerow([slide_num, text_entry])

    def write_feature_dict_to_json(self, feature_dict) -> None:
        for slide_num in feature_dict["text"].keys():
            text_entries = feature_dict["text"][slide_num]
            for text_entry in text_entries:
                if (text_entry == ""):
                    text_entries.remove(text_entry)
                if (text_entry == slide_num):
                    text_entries.remove(text_entry)

        json_filepath = str(self.unpack_dir) + ".json"
        with open(json_filepath, "w") as jsonfile:
            jsonfile.write(json.dumps(feature_dict))

    def extract_table_features(self, slide_paths) -> dict:
        all_extracted_tables = {}
        for slide_path in slide_paths:
            extracted_tables = self.extract_table_slide_filepath(slide_path)
            if extracted_tables is not None:
                all_extracted_tables.update(extracted_tables)

        return all_extracted_tables

    def extract_table_slide_filepath(self, slide_filepath):
        # remove "slide" from slide12 to isolated the slide's number
        slide_num = slide_filepath.stem

        # lxml api allows parsing from python Path objects directly
        tree = etree.parse(slide_filepath)
        root = tree.getroot()
        xml_tables = root.findall(".//a:tbl", namespaces=root.nsmap)

        extracted_tables = []
        for xml_table in xml_tables:
            table_contents = []
            xml_rows = xml_table.findall(".//a:tr", namespaces=root.nsmap)
            for xml_row in xml_rows:
                row_contents = []
                xml_cells = xml_row.findall(".//a:tc", namespaces=root.nsmap)
                for xml_cell in xml_cells:
                    cell_text = ""
                    cell_p_tags = xml_cell.findall(
                        ".//a:p", namespaces=root.nsmap)
                    for p_tag in cell_p_tags:
                        cell_text += self.rebuild_p_tag(p_tag,
                                                        nsmap=root.nsmap)
                    row_contents.append(cell_text)
                table_contents.append(row_contents)
            extracted_tables.append(table_contents)

        if (len(extracted_tables) > 0):
            return {slide_num: extracted_tables}

    def extract_bullet_features(self, slide_paths: list[Path]) -> dict:
        all_extracted_bullets = {}
        for slide_path in slide_paths:
            extracted_bullets = self.extract_bullet_slide_filepath(slide_path)
            if extracted_bullets is not None:
                all_extracted_bullets.update(extracted_bullets)

        return all_extracted_bullets

    def extract_bullet_slide_filepath(self, slide_filepath):
        # remove "slide" from slide12 to isolated the slide's number
        slide_num = slide_filepath.stem

        # lxml api allows parsing from python Path objects directly
        tree = etree.parse(slide_filepath)
        root = tree.getroot()

        extracted_bullets = []
        paragraphs = root.findall(".//a:p", namespaces=root.nsmap)

        if (len(extracted_bullets) > 0):
            return {slide_num: extracted_bullets}

    def extract_features(self) -> None:
        self.parse_mode = "features"

        # 1. pull text
        slide_paths = self.get_slide_filepaths()
        extracted_text = self._extract_text(slide_paths)

        # 2. pull defined features
        extracted_tables = self.extract_table_features(slide_paths)
        extracted_bullets = self.extract_bullet_features(slide_paths)

        # 3. build json document
        feature_dict = {"text": extracted_text, "tables": extracted_tables}

        # 4. write json document to file
        self.write_feature_dict_to_json(feature_dict)
