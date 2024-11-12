import pygame_menu
import pygame
from .menu_opciones_juego import MenuOpcionesJuego


class MenuNiveles:
    def __init__(self, screen: pygame.display, menu_partida, main):
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
        self.main_juego = main
        self.menu_partida = menu_partida
        self.menu_niveles = pygame_menu.Menu(title="Niveles", width=1000, height=700, theme=custom_theme)

    def mostrar_menu_niveles(self):
        self.menu_niveles.clear()
        self.menu_niveles.add.button(title="Nivel 1")
        self.menu_niveles.add.button(title="Nivel 2")
        self.menu_niveles.add.button(title="Nivel 3")
        self.menu_niveles.add.button(title="Nivel 4")
        self.menu_niveles.add.button(title="Nivel 5")
        self.menu_niveles.add.button(title="Nivel 6")
        self.menu_niveles.add.button(title="Volver", action=self.menu_partida.mostrar_menu_partida)

        self.menu_niveles.mainloop(self.pantalla)

    def activar_menu_opciones_juego(self):
        menu_opciones_juego = MenuOpcionesJuego(self.pantalla, self, self.main_juego)
        menu_opciones_juego.mostrar_menu_opciones_juego()
