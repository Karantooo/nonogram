import pygame_menu
import pygame
from menu_inicio import MenuInicio


class MenuConfiguracion:
    def __init__(self, screen: pygame.display, menu_inicial: MenuInicio):
        self.pantalla = screen
        self.menu_inicio = menu_inicial
        self.menu_configuracion = pygame_menu.Menu(title="Ajustes", width=700, height=500, theme=pygame_menu.themes.THEME_DARK)

    def mostrar_menu_configuracion(self):
        self.menu_configuracion.clear()
        self.menu_configuracion.add.button(title="Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_configuracion.mainloop(self.pantalla)