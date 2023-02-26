from core.PPTParser import PPTParser
from core.NotesParser import SlideNotesParser
from core.WebScraper import WebScraper
from pathlib import Path
from views import parse_file_menu, main_menu, parse_slide_feature_menu, parse_slide_notes_menu, scrape_web_references_menu
import csv
import json


def parse_controller(in_path='.'):
    dir_path = Path(in_path)
    files = list(dir_path.glob("*.pptx"))
    files_as_filenames = [x.name for x in files]

    files_to_parse = parse_file_menu.parse_file_menu(files_as_filenames)
    if files_to_parse == None:
        print("No files selected to parse. Returning to main menu.")
        main_menu.main_menu()

    files_to_parse = [dir_path / x for x in files_to_parse]

    parser = PPTParser(filepath=files_to_parse[0])
    unpack_dir = parser.unpack_file()

    file_action_to_take = parse_slide_feature_menu.parse_slide_feature_menu()

    # these string literals are defined in parse_slide_feature_menu.py
    if file_action_to_take == "text":
        parser.extract_text()
    elif file_action_to_take == "features":
        parser.extract_features()
    else:
        exit()

    out_file = str(unpack_dir) + \
        (".csv" if file_action_to_take == "text" else ".json")
    should_parse_notes = parse_slide_notes_menu.parse_slide_notes_menu() == "yes"
    all_note_content = {}
    if should_parse_notes:
        files_to_parse = unpack_dir.glob("ppt/notesSlides/*.xml")
        for filepath in files_to_parse:
            np = SlideNotesParser(filepath)
            content = np.parse()
            all_note_content.update({content["slide"] + "-notes": content})

        if file_action_to_take == "text":
            # we're writing to CSV, prep that
            # this is basically copy-pasted from PPTParser.py:write_extracted_text_to_csv
            # this can certainly be cleaned up
            csv_filepath = str(unpack_dir) + ".csv"
            with open(csv_filepath, "a") as csvfile:
                csv_writer = csv.writer(
                    csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)

                # include the raw information from the slide's notes
                for slide in all_note_content.keys():
                    if (len(all_note_content[slide]["content"]["information"]) > 0):
                        csv_writer.writerow(
                            [slide, all_note_content[slide]["content"]["information"]])

        if file_action_to_take == "features":
            json_filepath = str(unpack_dir) + ".json"
            with open(json_filepath, "r+") as jsonfile:
                prev_content = jsonfile.read()
                json_out = json.loads(prev_content)
                json_out.update({"notes": all_note_content})
                jsonfile.seek(0)
                jsonfile.write(json.dumps(json_out))
                jsonfile.truncate()
    else:
        print(f"Output written to {out_file}")
        exit()

    should_scrape_references = scrape_web_references_menu.scrape_web_references_menu() == "yes"
    all_references = {}
    if should_scrape_references:
        for slide in all_note_content.keys():
            slide_links = all_note_content[slide]["content"]["links"]
            for reference_idx in range(0, len(slide_links)):
                try:
                    scraper = WebScraper(slide_links[reference_idx])
                    html = scraper.fetch_html()
                    all_text = scraper.get_readable_text_from_html(html)
                    all_references.update(
                        {f"{slide}-reference{reference_idx}": all_text})
                except:
                    print("Problem scraping link: " +
                          slide_links[reference_idx])

        if file_action_to_take == "text":
            # we're writing to CSV, prep that
            # this is basically copy-pasted from PPTParser.py:write_extracted_text_to_csv
            # this can certainly be cleaned up
            csv_filepath = str(unpack_dir) + ".csv"
            with open(csv_filepath, "a") as csvfile:
                csv_writer = csv.writer(
                    csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)

                for slide in all_references.keys():
                    csv_writer.writerow(
                        [slide, all_references[slide]])

        if file_action_to_take == "features":
            json_filepath = str(unpack_dir) + ".json"
            with open(json_filepath, "r+") as jsonfile:
                prev_content = jsonfile.read()
                json_out = json.loads(prev_content)
                json_out.update({"references": all_references})
                jsonfile.seek(0)
                jsonfile.write(json.dumps(json_out))
                jsonfile.truncate()

    else:
        print(f"Output written to {out_file}")
        exit()

    print(f"Output written to {out_file}")
