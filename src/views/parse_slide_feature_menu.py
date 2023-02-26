from simple_term_menu import TerminalMenu


def parse_slide_feature_menu():
    MENU_MESSAGES = {
        "text": "[t] extract slide text only (outputs to csv)",
        "features": "[v] extract semantic features (outputs to json)",
        "exit": "[e] exit"
    }

    keys = list(MENU_MESSAGES.keys())
    options = [MENU_MESSAGES[x] for x in keys]
    terminal_menu = TerminalMenu(options, title="Which data to parse:")

    selected_index = terminal_menu.show()
    return keys[selected_index]
