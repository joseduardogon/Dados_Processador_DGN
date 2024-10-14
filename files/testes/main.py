import flet as ft

def main_page(page: ft.Page):
    page.title = "Página Principal"
    page.window.width = 600
    page.window.height = 400
    page.bgcolor = ft.colors.WHITE

    page.add(ft.Text("Bem-vindo à Página Principal!", size=24))
    page.add(ft.Text("Esta página é exibida após o carregamento."))

if __name__ == "__main__":
    ft.app(target=main_page)
