from simple_term_menu import TerminalMenu
from controllers import exit_controller, parse_controller, validate_controller

MENU_MESSAGES = {
    "parse": "[p] parse pptx",
    "validate": "[v] validate pptx",
    "exit": "[e] exit"
}

def main_menu():
    options = [MENU_MESSAGES[x] for x in MENU_MESSAGES.keys()]
    terminal_menu = TerminalMenu(options)
    selected_index = terminal_menu.show()

    if options[selected_index] == MENU_MESSAGES["parse"]:
        input_path = input("Path where PPTX and CTS document are located: ")
        parse_controller.parse_controller(input_path)

    elif options[selected_index] == MENU_MESSAGES["validate"]:
        validate_controller.validate_controller()

    elif options[selected_index] == MENU_MESSAGES["exit"]:
        exit_controller.exit_controller()