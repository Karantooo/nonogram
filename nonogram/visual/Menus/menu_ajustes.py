import pygame
import pygame_menu
from .menu_inicio import MenuInicio


class MenuAjustes:
    def __init__(self, screen: pygame.display, menu_inicio: MenuInicio):

        custom_theme = pygame_menu.Theme(background_color=(17, 84, 143), title_font=pygame_menu.font.FONT_FRANCHISE,
                                         title_font_size=100,
                                         title_background_color=(13, 62, 105),
                                         widget_font=pygame_menu.font.FONT_FRANCHISE,
                                         widget_font_color=(255, 255, 255),
                                         widget_font_size=70,
                                         widget_background_color=(13, 62, 105),
                                         selection_color=(25, 122, 207),
                                         widget_padding=(10, 15),
                                         )

        self.pantalla = screen
        self.menu_inicio = menu_inicio
        self.menu_ajustes = pygame_menu.Menu("Opciones de juego", 1920, 1080, theme=custom_theme)

    def mostrar_menu_ajustes(self):
        self.menu_ajustes.clear()
        self.menu_ajustes.add.button("Continuar", action=self.apagar_menu_ajustes)
        self.menu_ajustes.add.button("Salir", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_ajustes.mainloop(self.pantalla)

    def activar_menu_ajustes(self):
        self.menu_ajustes.clear()
        self.menu_ajustes.enable()

    def apagar_menu_ajustes(self):
        self.menu_ajustes.disable()
