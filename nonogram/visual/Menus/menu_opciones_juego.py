from idlelib.configdialog import font_sample_text

import pygame
import pygame_menu
from pygame_menu.examples.other.image_background import background_image


class MenuOpcionesJuego:
    def __init__(self, screen: pygame.display, menu_partida, main):

        custom_theme = pygame_menu.Theme(background_color= (17, 84, 143), title_font= pygame_menu.font.FONT_FRANCHISE, title_font_size=100,
                                         title_background_color=(13, 62, 105),
                                         widget_font=pygame_menu.font.FONT_FRANCHISE,
                                         widget_font_color=(255,255,255),
                                         widget_font_size=70,
                                         widget_background_color=(13, 62, 105),
                                         selection_color=(25, 122, 207),
                                         widget_padding=(10, 15),
                                         )




        self.pantalla = screen
        self.num_botones = 3
        self.main_juego = main
        self.menu_partida = menu_partida
        self.menu_opciones_juego = pygame_menu.Menu(title="Seteo del nivel", width=1000, height=700, theme=custom_theme)



    def mostrar_menu_opciones_juego(self):
        self.menu_opciones_juego.clear()
        self.menu_opciones_juego.add.label(f'Cantidad de botones')
        self.menu_opciones_juego.add.range_slider('Botones', default=3, range_values=(3,20), increment=1, onchange=self.selecionar_cant_botones)
        self.menu_opciones_juego.add.button("Jugar", action=self.main_juego.main)
        self.menu_opciones_juego.add.button("Volver", action=self.menu_partida.mostrar_menu_partida)

        self.menu_opciones_juego.mainloop(self.pantalla)

    def selecionar_cant_botones(self, cant):
        self.main_juego.select_cant_botones(cant)
