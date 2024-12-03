import pygame_menu
import pygame
import pickle
from .menu_opciones_juego import MenuOpcionesJuego


class MenuNiveles:
    def __init__(self, screen: pygame.display, menu_partida, main):
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
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
        self.ruta = None
        self.pantalla = screen
        self.main_juego = main
        self.menu_partida = menu_partida
        self.menu_niveles = pygame_menu.Menu(title="Niveles", width=screen_width, height=screen_height, theme=custom_theme)

    def mostrar_menu_niveles(self):
        self.menu_niveles.clear()
        self.menu_niveles.add.button(title="Nivel 1", action=self.cargar_nivel1)
        self.menu_niveles.add.button(title="Nivel 2", action=self.cargar_nivel2)
        self.menu_niveles.add.button(title="Nivel 3", action=self.cargar_nivel3)
        self.menu_niveles.add.button(title="Nivel 4", action=self.cargar_nivel4)
        self.menu_niveles.add.button(title="Nivel 5", action=self.cargar_nivel5)
        self.menu_niveles.add.button(title="Nivel 6", action=self.cargar_nivel6)
        self.menu_niveles.add.button(title="Volver", action=self.menu_partida.mostrar_menu_partida)

        self.menu_niveles.mainloop(self.pantalla)

    def activar_menu_opciones_juego(self):
        menu_opciones_juego = MenuOpcionesJuego(self.pantalla, self, self.main_juego)
        menu_opciones_juego.mostrar_menu_opciones_juego()

    def cargar_nivel1(self):
        partida = self.cargar_estado(ruta = r"nonogram/Niveles/Nivel1.bin")
        self.main_juego.main(partida_guardada=partida)

    def cargar_nivel2(self):
        partida = self.cargar_estado(ruta = r"nonogram/Niveles/Nivel2.bin")
        self.main_juego.main(partida_guardada=partida)

    def cargar_nivel3(self):
        partida = self.cargar_estado(ruta = r"nonogram/Niveles/Nivel3.bin")
        self.main_juego.main(partida_guardada=partida)

    def cargar_nivel4(self):
        partida = self.cargar_estado(ruta = r"nonogram/Niveles/Nivel4.bin")
        self.main_juego.main(partida_guardada=partida)

    def cargar_nivel5(self):
        partida = self.cargar_estado(ruta = r"nonogram/Niveles/Nivel5.bin")
        self.main_juego.main(partida_guardada=partida)

    def cargar_nivel6(self):
        partida = self.cargar_estado(ruta = r"nonogram/Niveles/Nivel6.bin")
        self.main_juego.main(partida_guardada=partida)

    @staticmethod
    def cargar_estado(ruta: str = r"../../Niveles/partidaG.bin"):
        with open(ruta, "rb") as archivo:
            casillas = pickle.load(archivo)
        return casillas