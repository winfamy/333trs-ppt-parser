from simple_term_menu import TerminalMenu


def parse_slide_feature_menu():
    MENU_MESSAGES = {
        "text": "[t] extract text only",
        "features": "[v] extract semantic features",
        "exit": "[e] exit"
    }

    keys = list(MENU_MESSAGES.keys())
    options = [MENU_MESSAGES[x] for x in keys]
    terminal_menu = TerminalMenu(options)

    selected_index = terminal_menu.show()
    return keys[selected_index]
