import os.path
from tkinter.ttk import Treeview

import pygame
import pygame_menu
from .menu_inicio import MenuInicio
from nonogram.visual.popup import Popup


class MenuGuardarPartida:
    def __init__(self, screen: pygame.display, menu_inicio: MenuInicio, tablero):

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
        self.tablero = tablero
        self.nombre_guardado = None
        self.menu_inicio = menu_inicio
        self.menu_guardar_partida = pygame_menu.Menu("Opciones de guardado", width=1000, height=700, theme=custom_theme)

        self.popup = Popup(400, 50, "¡Se guardó correctamente!")

    def mostrar_menu_guardado(self):
        self.menu_guardar_partida.clear()
        self.menu_guardar_partida.add.text_input(title="Nombre archivo: ", default="",onchange=self.set_nombre_archivo)
        self.menu_guardar_partida.add.button("Volver al Juego", action=self.apagar_menu_guardado)
        self.boton_guardar = self.menu_guardar_partida.add.button("Guardar",action=self.guardar_partida)
        self.boton_guardar._visible = False
        self.menu_guardar_partida.add.button("Salir", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_guardar_partida.mainloop(self.pantalla)

    def activar_menu_guardado(self):
        self.menu_guardar_partida.clear()
        self.menu_guardar_partida.enable()

    def apagar_menu_guardado(self):
        self.menu_guardar_partida.disable()

    def actualizar_popup(self, eventos, menu):
        if self.popup.active:
            for evento in eventos:
                self.popup.handle_event(evento)

    def imprimir_popup(self, screen):
        if self.popup.active:
            self.popup.imprimir(screen)

    def guardar_partida(self):
        if not os.path.exists("nonogram/partidas_guardadas"):
            os.mkdir("nonogram/partidas_guardadas")
        ruta = "nonogram/partidas_guardadas/" + self.nombre_guardado + ".bin"
        self.tablero.guardar_estado(ruta)

        self.popup.mostrar()

    def set_nombre_archivo(self, nombre_archivo):
        self.nombre_guardado = nombre_archivo
        print("Nombre de archivo guardado: " + self.nombre_guardado)
        if self.nombre_guardado != "":
            self.boton_guardar._visible = True
