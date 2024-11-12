import pygame_menu
import pygame


class MenuConfiguracion:
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

        self.pantalla = screen
        self.main_juego = main
        self.menu_inicio = menu_inicial
        self.menu_configuracion = pygame_menu.Menu(title="Ajustes", width=1000, height=700, theme=custom_theme)

    def mostrar_menu_configuracion(self):
        self.menu_configuracion.clear()
        self.menu_configuracion.add.label(f'Volumen de la musica: ')
        self.menu_configuracion.add.range_slider('Volumen', default=0.05, range_values=(0, 1), increment=1,
                                                  onchange=self.main_juego.cambiar_volumen_musica)
        self.menu_configuracion.add.button(title="Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_configuracion.mainloop(self.pantalla)