import pygame_menu
import pygame
from .menu_configuracion import MenuConfiguracion
from .menu_opciones_juego import MenuOpcionesJuego



class MenuInicio:
    def __init__(self, screen: pygame.display, main):
        custom_theme = pygame_menu.Theme(background_color=(17, 84, 143), title_font=pygame_menu.font.FONT_FRANCHISE,
                                         title_font_size=50,
                                         title_background_color=(13, 62, 105),
                                         widget_font=pygame_menu.font.FONT_FRANCHISE,
                                         widget_font_color=(255, 255, 255),
                                         widget_font_size=35,
                                         widget_background_color=(13, 62, 105),
                                         selection_color=(25, 122, 207),
                                         widget_padding=(10, 15),
                                         )

        self.pantalla = screen
        self.main = main
        self.menu_inicio = pygame_menu.Menu(title="Nonogram", width=1920, height=1080, theme=custom_theme)

    def mostrar_menu_inicio(self):
        self.menu_inicio.clear()
        self.menu_inicio.add.button('Jugar', self.activar_menu_opciones_juego)
        self.menu_inicio.add.button('Configuracion', self.activar_menu_configuracion)
        self.menu_inicio.add.button('Salir', pygame_menu.events.EXIT)

        self.menu_inicio.mainloop(self.pantalla)

    def activar_menu_configuracion(self):
        menu_configuracion = MenuConfiguracion(self.pantalla, self)
        menu_configuracion.mostrar_menu_configuracion()

    def activar_menu_opciones_juego(self):
        menu_opciones_juego = MenuOpcionesJuego(self.pantalla, self, self.main)
        menu_opciones_juego.mostrar_menu_opciones_juego()