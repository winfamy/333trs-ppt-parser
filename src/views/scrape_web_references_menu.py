from simple_term_menu import TerminalMenu


def scrape_web_references_menu():
    MENU_MESSAGES = {
        "yes": "[y] yes",
        "no": "[n] no"
    }

    keys = list(MENU_MESSAGES.keys())
    options = [MENU_MESSAGES[x] for x in keys]
    terminal_menu = TerminalMenu(options, title="Scrape web references?")

    selected_index = terminal_menu.show()
    return keys[selected_index]
