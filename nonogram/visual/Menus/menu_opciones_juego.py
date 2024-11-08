import pygame
import pygame_menu


class MenuOpcionesJuego:
    def __init__(self, screen: pygame.display, menu_inicio, main):
        self.pantalla = screen
        self.num_botones = 3
        self.main_juego = main
        self.menu_inicio = menu_inicio
        self.menu_opciones_juego = pygame_menu.Menu(title="Seteo del nivel", width=700, height=500, theme=pygame_menu.themes.THEME_DARK)



    def mostrar_menu_opciones_juego(self):
        self.menu_opciones_juego.clear()
        self.menu_opciones_juego.add.label(f'Cantidad de botones: {self.main_juego.cantidad_de_botones}')
        self.menu_opciones_juego.add.range_slider('Botones', default=3, range_values=(3,20), increment=1, onchange=self.selecionar_cant_botones)
        self.menu_opciones_juego.add.button("Jugar", action=self.main_juego.main)
        self.menu_opciones_juego.add.button("Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_opciones_juego.mainloop(self.pantalla)

    def selecionar_cant_botones(self, cant):
        self.main_juego.select_cant_botones(cant)
