

import flet as ft
from time import sleep


def main(page: ft.Page):
        pass
        page.window.width = 250
        page.window.height = 100
        page.bgcolor = ft.colors.WHITE
        page.window.border_radius = 7
        page.window.frameless = True
        page.window.always_on_top = True
        page.window.shadow = True
        page.window.center()
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        progress_bar = ft.ProgressBar(width=200, color="yellow")
        texto_progresso = ft.Text(value="0%", size=16, color="black")

        layout = ft.Column(
                controls=[
                    ft.Text("Carregando...", size=20, weight=ft.FontWeight.BOLD, color="black"), # texto "Carregando"
                    progress_bar, # Barra de progresso
                    texto_progresso, # Texto do progresso
                ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page.add(layout)

        for i in range(0, 101):
            progress_bar.value = i * 0.01
            loading_value = int(progress_bar.value * 100)
            texto_progresso.value = f"{loading_value}%"
            sleep(0.1)
            page.update()

ft.app(target=main)