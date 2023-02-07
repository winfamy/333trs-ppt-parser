from core.PPTParser import PPTParser
from pathlib import Path
from views import parse_file_menu, main_menu

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
    parser.unpack_file()