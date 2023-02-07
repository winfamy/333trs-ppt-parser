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
        validate_controller.validate_controller()

    elif options[selected_index] == MENU_MESSAGES["validate"]:
        parse_controller.parse_controller()
        
    elif options[selected_index] == MENU_MESSAGES["exit"]:
        exit_controller.exit_controller()