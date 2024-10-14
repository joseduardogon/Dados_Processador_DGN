import flet as ft
import asyncio

def loading_window(page: ft.Page):
    page.title = "Loading"
    page.window.width = 300
    page.window.height = 200
    page.bgcolor = ft.colors.LIGHT_GREEN

    page.add(ft.Text("Carregando...", size=24))
    page.update()  # Atualiza a página para refletir as mudanças

    async def simulate_loading():
        await asyncio.sleep(2)  # Simula um delay de 2 segundos
        page.clean()  # Limpa a página de loading
        from main import main_page  # Importa a página principal
        main_page(page)  # Chama a página principal

    asyncio.run(simulate_loading())  # Executa a função assíncrona

