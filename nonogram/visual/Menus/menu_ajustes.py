import pygame
import pygame_menu
from .menu_inicio import MenuInicio


class MenuAjustes:
    def __init__(self, screen: pygame.display, menu_inicio: MenuInicio):
        self.pantalla = screen
        self.menu_inicio = menu_inicio
        self.menu_ajustes = pygame_menu.Menu("Opciones de juego", 600, 400, theme=pygame_menu.themes.THEME_DARK)

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
