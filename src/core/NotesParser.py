from lxml import etree
from pathlib import Path


class SlideNotesParser:
    labels = {
        "links": {
            "section-label": "URL References",
            "type": list,
            "separator": "\n"
        },
        "title": {
            "section-label": "Title",
            "type": str
        },
        "cts-items": {
            "section-label": "CTS Items",
            "type": list,
            "separator": ","
        },
        "information": {
            "section-label": "Information",
            "type": str
        },
        "presenter-notes": {
            "section-label": "Presenter Notes",
            "type": str
        },
        "raw_entries": {
            "section-label": "",
            "type": list
        }
    }

    def __init__(self, note_path: Path) -> None:
        self.note_path = note_path
        self._setup_xml_tree()

    def _setup_xml_tree(self) -> None:
        self.root = etree.parse(self.note_path).getroot()

    def _get_all_text(self) -> list:
        text_entries = []

        # for each p-tag, discover internal p tags to rebuild the "full"/displayed string
        p_tags = self.root.findall(".//a:p", namespaces=self.root.nsmap)
        for p_tag in p_tags:
            # for each p-tag, discover internal p tags to rebuild the "full"/displayed string
            combined_text = ""
            t_tags = p_tag.findall(".//a:t", namespaces=self.root.nsmap)
            for t_tag in t_tags:
                # filter out auto-generated slide numbers
                parent = t_tag.getparent()
                if parent.get("type") == "slidenum":
                    continue

                combined_text += t_tag.text

            if len(combined_text) > 0:
                text_entries.append(combined_text)

        return text_entries

    def _get_slide(self) -> str:
        """
        This function gets the corresponding slide number from the notesSlideX.xml.rels files within notesSlides/_rels/ because the numbers are not directly related. In the first testing scenario notesSlide9.xml stored the notes for slide 23. Really cool!
        """

        # Constructs the path to the corresponding .xml.rels
        rels_path = self.note_path.parent / "_rels" / \
            self.note_path.with_suffix(".xml.rels").name

        rels_root = etree.parse(rels_path).getroot()
        relationships = rels_root.findall(
            "Relationship[@Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide']", namespaces=rels_root.nsmap)
        # exactly one xml element should define the slide relationship
        if len(relationships) != 1:
            raise RuntimeError(
                "Error finding the corresponding slide for notes items " + self.note_path.name)

        slide_relationship = relationships[0]
        slide_target = slide_relationship.get("Target")

        # filter ../slides/slide38.xml to slide38
        return slide_target.replace("../slides/", "").replace(".xml", "")

    def parse_content(self, text_entries):
        """Groups content into text following a label marker until the next label marker is found"""
        content_dict = {}
        label_dict = {}

        # maps a dictionary from the "section label" to the internal "key" so we can use the raw notes text to match where it should be
        for key in SlideNotesParser.labels.keys():
            label_dict[SlideNotesParser.labels[key]
                       ["section-label"]] = key
            content_dict[key] = SlideNotesParser.labels[key]["type"]()

        current_label = None
        for text_entry in text_entries:
            if text_entry.startswith("["):
                # update which section the following content gets grouped into
                current_label = text_entry.replace("[", "").replace("]", "")
            else:
                try:
                    label_key = label_dict[current_label]
                    label_meta_info = SlideNotesParser.labels[label_key]
                    text_entry_type = label_meta_info["type"]

                    # if the group's type is defined as a list, parse like that
                    if text_entry_type is list:
                        content_separator = label_meta_info["separator"]
                        line_content_as_list = text_entry.split(
                            content_separator)
                        for line_entry in line_content_as_list:
                            content_dict[label_key].append(
                                line_entry.strip())
                    elif text_entry_type is str:
                        content_dict[label_key] += text_entry + "\n"
                    else:
                        pass
                except KeyError:
                    # label not found, means slide notes are malformed
                    pass

        content_dict["raw"] = text_entries
        return content_dict

    def parse(self) -> dict:
        self._setup_xml_tree()

        notes_text_entries = self._get_all_text()

        return {
            "slide": self._get_slide(),
            "content": self.parse_content(notes_text_entries)
        }
