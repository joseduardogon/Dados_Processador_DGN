import flet as ft
from loading import loading_window

def login_window(page: ft.Page):
    page.title = "Login"
    page.window.width = 400
    page.window.height = 300
    page.bgcolor = ft.colors.LIGHT_BLUE

    def on_login_click(e):
        # Limpa os elementos da página de login
        page.clean()
        loading_window(page)  # Chama a página de loading

    page.add(ft.Text("Tela de Login", size=24))
    page.add(ft.TextField(label="Usuário"))
    page.add(ft.TextField(label="Senha", password=True))
    page.add(ft.ElevatedButton("Login", on_click=on_login_click))

if __name__ == "__main__":
    ft.app(target=login_window)
