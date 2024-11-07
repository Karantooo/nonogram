import pygame_menu
import pygame
from menu_configuracion import MenuConfiguracion
from menu_opciones_juego import MenuOpcionesJuego



class MenuInicio:
    def __init__(self, screen: pygame.display):
        self.pantalla = screen
        self.menu_inicio = pygame_menu.Menu(title="Nonogram", width=700, height=500, theme=pygame_menu.themes.THEME_DARK)

    def mostrar_menu_inicio(self):
        self.menu_inicio.clear()
        self.menu_inicio.add.button('Jugar', self.activar_menu_opciones_juego)
        self.menu_inicio.add.button('Configuración', self.activar_menu_configuracion)
        self.menu_inicio.add.button('Salir', pygame_menu.events.EXIT)

        self.menu_inicio.mainloop(self.pantalla)

    def activar_menu_configuracion(self):
        menu_configuracion = MenuConfiguracion(self.pantalla, self)
        menu_configuracion.mostrar_menu_configuracion()

    def activar_menu_opciones_juego(self):
        menu_opciones_juego = MenuOpcionesJuego(self.pantalla, self)
        menu_opciones_juego.mostrar_menu_opciones_juego()