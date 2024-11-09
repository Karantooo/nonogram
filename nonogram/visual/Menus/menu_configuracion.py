import pygame_menu
import pygame


class MenuConfiguracion:
    def __init__(self, screen: pygame.display, menu_inicial):
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
        self.menu_inicio = menu_inicial
        self.menu_configuracion = pygame_menu.Menu(title="Ajustes", width=1920, height=1080, theme=custom_theme)

    def mostrar_menu_configuracion(self):
        self.menu_configuracion.clear()
        self.menu_configuracion.add.button(title="Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_configuracion.mainloop(self.pantalla)