import pygame
import pygame_menu
from menu_inicio import MenuInicio


class MenuOpcionesJuego:
    def __init__(self, screen: pygame.display, menu_inicio: MenuInicio):
        self.pantalla = screen
        self.menu_inicio = menu_inicio
        self.menu_opciones_juego = pygame_menu.Menu(title="Seteo del nivel", width=700, height=500, theme=pygame_menu.themes.THEME_DARK)


    def iniciar_juego(self):
        juego = Juego(self.pantalla, self.menu_inicio, self.color_cuadrado) ############################################
        juego.run()

    def mostrar_menu_opciones_juego(self):
        self.menu_opciones_juego.clear()
        self.menu_opciones_juego.add.button("Jugar", action=self.iniciar_juego)
        self.menu_opciones_juego.add.button("Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_opciones_juego.mainloop(self.pantalla)
