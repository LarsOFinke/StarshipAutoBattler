from .utils.console_helpers import clear_console
from .models.menus.auth_menu import AuthMenu
from .models.menus.main_menu import MainMenu


def run_authentication() -> bool:
    auth_menu = AuthMenu()
    auth_menu.run()
    if auth_menu.auth_client.is_authenticated():
        return True
    return False


def run_main_menu():
    main_menu = MainMenu()
    main_menu.run()


def main():
    authenticated = run_authentication()
    if authenticated:
        run_main_menu()
    input("Goodbye! \n(Press Enter)")
    clear_console()


if __name__ == "__main__":
    main()
