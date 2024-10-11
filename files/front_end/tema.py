import flet as ft

def meu_tema():
    return ft.Theme(
        color_scheme_seed=ft.colors.YELLOW_700, # Amarelo-ouro como base
        color_scheme=ft.ColorScheme(
            primary=ft.colors.YELLOW_700,
            on_primary=ft.colors.WHITE,
            secondary=ft.colors.BLUE_GREY_900,
            on_secondary=ft.colors.WHITE,
            surface=ft.colors.WHITE,
            on_surface=ft.colors.BLACK87,
            background=ft.colors.GREY_100,
        ),
        text_theme=ft.TextTheme(
            headline_medium=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY_900),
            title_medium=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
            body_medium=ft.TextStyle(size=14, color=ft.colors.BLACK87),
            body_small=ft.TextStyle(size=12, color=ft.colors.BLACK54),
        ),
        font_family="Roboto",
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.FADE_UPWARDS,
        ),
        tabs_theme=ft.TabsTheme(
            overlay_color= {
                ft.ControlState.FOCUSED: ft.colors.GREY_200,
                ft.ControlState.HOVERED: ft.colors.GREY_300,
                ft.ControlState.PRESSED: ft.colors.GREY_400,
            },
            indicator_color=ft.colors.YELLOW_700,
        ),
    )