# front_end/main.py
import flet as ft
from front_end.gui_login import login_window

def main(page: ft.Page):
    login_window(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

