import pygame_menu
import pygame


class MenuAjustes():
    menu_inicio : pygame_menu
    pantalla : pygame.display
    def __init__(self, menu_inicial : pygame_menu, screen : pygame.display, juego):
        self.pantalla = screen
        self.menu_inicio = menu_inicial
        self.menu_ajustes = pygame_menu.Menu("Opciones de juego", 600,400, theme=pygame_menu.themes.THEME_DARK)

    def mostrar_menu_ajustes(self):
        self.menu_ajustes.clear()
        self.menu_ajustes.add.button("Continuar", self.menu_ajustes.disable)
        self.menu_ajustes.add.button("Salir", self.menu_ajustes.close)
