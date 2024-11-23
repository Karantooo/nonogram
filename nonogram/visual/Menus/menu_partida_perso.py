import pygame_menu
import pygame

from .menu_opciones_juego import MenuOpcionesJuego
from nonogram.logica.image_to_matrix import ImageToMatrix
from nonogram.logica.excepciones_imagenes import NoExisteMatrizError, ImagenError
from nonogram.logica.casilla import Casilla
from nonogram.logica.sistema_guardado import SistemaGuardado


class MenuPartidaPerso():
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
        self.URL = ""
        self.botones = 10
        self.pantalla = screen
        self.main_juego = main
        self.menu_partida = menu_partida
        self.menu_partida_perso = pygame_menu.Menu(title="Seleccione partida", width=1000, height=700, theme=custom_theme)

    def mostrar_menu_partida_perso(self):
        self.menu_partida_perso.clear()
        self.menu_partida_perso.add.text_input(title="URL: ",onchange= self.guardar_URL)
        self.menu_partida_perso.add.text_input(title="Cantidad de botones: ", onchange= self.cant_botones, default="10")
        self.menu_partida_perso.add.button(title="Aceptar", action=self.jugar_partida_guardada)
        self.menu_partida_perso.add.button(title="Volver", action=self.menu_partida.mostrar_menu_partida)

        self.menu_partida_perso.mainloop(self.pantalla)

    def activar_menu_partida(self):
        menu_opciones_juego = MenuOpcionesJuego(self.pantalla, self, self.main_juego)
        menu_opciones_juego.mostrar_menu_opciones_juego()

    def jugar_partida_guardada(self):
        while True:
            try:
                # Verificar si la URL ha sido proporcionada
                if not self.URL:
                    raise ValueError("No se ha proporcionado una URL.")

                # Intentar cargar la imagen usando ImageToMatrix
                thresh_hold = 0.5
                image_processor = ImageToMatrix(self.URL, self.botones, thresh_hold)
                self.matrix = image_processor.show_matrix()

                # Mostrar éxito y romper el bucle
                print("Matriz generada con éxito:")
                break

            except ImagenError:
                self.menu_partida_perso.add.label(
                    "Error: No se pudo cargar la imagen. Verifica la URL.",
                    max_char=-1, align=pygame_menu.locals.ALIGN_CENTER
                )
                return self.mostrar_menu_partida_perso()

            except ValueError as ve:
                self.menu_partida_perso.add.label(
                    f"Error: {str(ve)}",
                    max_char=-1, align=pygame_menu.locals.ALIGN_CENTER
                )
                return self.mostrar_menu_partida_perso()

            except NoExisteMatrizError:
                print("Error: No se pudo generar la matriz.")
                return self.mostrar_menu_partida_perso()

            except Exception as e:
                print(f"Error inesperado: {e}")
                return self.mostrar_menu_partida_perso()

        self.main_juego.main(partida_guardada=self.matriz_a_SistemaGuardado())

    def guardar_URL(self, url):
        self.URL = url

    def cant_botones(self, cant: str):

        try:
            cant = int(cant) if cant.strip() else 10
        except ValueError:
            cant = 10

        if cant >= 20:
            self.botones = 20
        else:
            self.botones = cant

    def matriz_a_SistemaGuardado(self):
        if self.matrix is None:
            raise ValueError("No se ha generado una matriz. Ejecute jugar_partida_guardada primero.")

        casillas = [
            [Casilla(marcado=bool(valor)) for valor in fila]
            for fila in self.matrix
        ]

        partida_imagen = SistemaGuardado(
            casillas=casillas,
            vidas_restantes=3,
            tiempo=0
        )
        return partida_imagen