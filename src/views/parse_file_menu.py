from simple_term_menu import TerminalMenu

# TODO this file returns logic in parse_controller since we need to access the return statement from this menu. this should be changed globally to either allow views to handle this or not, just to keep it consistent
def parse_file_menu(files):
    terminal_menu = TerminalMenu(
        files,
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_empty_ok=True
    )

    menu_entry_indices = terminal_menu.show()
    return terminal_menu.chosen_menu_entries