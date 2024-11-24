import pygame_menu
import pygame
import pickle
import threading
import os
import tkinter as tk
from tkinter import filedialog
from nonogram.logica.sistema_guardado import SistemaGuardado
from .menu_niveles import MenuNiveles
from .menu_opciones_juego import MenuOpcionesJuego
from .menu_partida_perso import MenuPartidaPerso
class MenuPartida:
    def __init__(self, screen: pygame.display, menu_inicial, main):
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
        self.menu_inicio = menu_inicial
        self.menu_partida = pygame_menu.Menu(title="Seleccione partida", width=1000, height=700, theme=custom_theme)

    def mostrar_menu_partida(self):
        self.menu_partida.clear()
        if os.path.exists(r"nonogram/partidas_guardadas") and len(os.listdir(r"nonogram/partidas_guardadas")) > 0:
            self.menu_partida.add.button(title="Partida Guardada", action=self.cargar_partida)
        self.menu_partida.add.button(title="Nueva Partida", action=self.activar_menu_opciones_juego)
        self.menu_partida.add.button(title="Partida personalizada", action=self.activar_menu_partida_perso)
        self.menu_partida.add.button(title="Niveles", action=self.activar_menu_niveles)
        self.menu_partida.add.button(title="Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_partida.mainloop(self.pantalla)

    def activar_menu_opciones_juego(self):
        menu_opciones_juego = MenuOpcionesJuego(self.pantalla, self, self.main_juego)
        menu_opciones_juego.mostrar_menu_opciones_juego()

    def activar_menu_niveles(self):
        menu_niveles = MenuNiveles(self.pantalla, self, self.main_juego)
        menu_niveles.mostrar_menu_niveles()

    def activar_menu_partida_perso(self):
        menu_partida_perso = MenuPartidaPerso(self.pantalla, self, self.main_juego)
        menu_partida_perso.mostrar_menu_partida_perso()

    def cargar_partida(self):
        hilo = threading.Thread(target=self.seleccionar_archivo)
        hilo.start()
        while self.ruta is None:
            pass
        partida = self.cargar_estado(ruta = self.ruta)
        self.main_juego.main(partida_guardada=partida)

    @staticmethod
    def cargar_estado(ruta: str = r"C:/Users/pablo/PycharmProjects/nonogram/nonogram/partidas_guardadas/partidaG.bin") -> SistemaGuardado:
        with open(ruta, "rb") as archivo:
            casillas = pickle.load(archivo)
        return casillas

    def seleccionar_archivo(self):
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal de Tkinter
        ruta_partidas_guardadas = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../partidas_guardada"))
        archivo_seleccionado = None
        while not archivo_seleccionado:  # Sigue preguntando hasta que se seleccione un archivo
            archivo_seleccionado = filedialog.askopenfilename(
                title="Selecciona un archivo",
                initialdir=ruta_partidas_guardadas,
            )
        root.destroy()
        self.ruta = archivo_seleccionado
