import pygame
import pygame_menu
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Juego con Menús y Contador")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clase del juego



# Clase para el menú principal
class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        self.menu = pygame_menu.Menu("Bienvenido", 400, 300, theme=pygame_menu.themes.THEME_BLUE)

    def iniciar_menu_transicion(self):
        # Iniciar el menú de transición al hacer clic en "Jugar"
        menu_transicion = MenuTransicion(self.screen, self)  # Crear el menú de transición
        menu_transicion.mostrar_menu()

    def mostrar_menu(self):
        # Añadir un botón al menú
        self.menu.clear()  # Limpia opciones previas para evitar duplicados al regresar
        self.menu.add.button("Jugar", self.iniciar_menu_transicion)
        self.menu.add.button("Salir", pygame_menu.events.EXIT)

        # Mostrar el menú hasta que se seleccione una opción
        self.menu.mainloop(self.screen)


# Clase para el menú de pausa
class MenuPausa:
    def __init__(self, screen, juego, menu_principal):
        self.screen = screen
        self.juego = juego
        self.menu_principal = menu_principal
        self.menu = pygame_menu.Menu("Pausa", 400, 300, theme=pygame_menu.themes.THEME_DARK)

    def mostrar_menu_pausa(self):
        # Añadir botones para continuar o ir al menú principal
        self.menu.clear()
        self.menu.add.button("Continuar", self.continuar_juego)
        self.menu.add.button("Volver al Menú Principal", self.menu_principal.mostrar_menu)

        # Pausar el juego y mostrar el menú de pausa
        self.menu.mainloop(self.screen)

    def activar_menu(self):
        self.menu.clear()
        self.menu.enable()

    def continuar_juego(self):
        # Cerrar el menú de pausa y continuar el juego
        self.menu.disable()  # Desactiva el menú de pausa para reanudar el juego


# Clase para el menú de transición
class MenuTransicion:
    def __init__(self, screen, menu_principal):
        self.screen = screen
        self.menu_principal = menu_principal
        self.color_seleccionado = GREEN  # Color por defecto
        self.menu = pygame_menu.Menu("Selecciona el Color", 400, 300, theme=pygame_menu.themes.THEME_BLUE)

    def set_color(self, color, _):
        # Actualizar el color seleccionado
        self.color_seleccionado = color

    def iniciar_juego(self):
        # Iniciar el juego con el color seleccionado
        juego = Juego(self.screen, self.menu_principal, self.color_seleccionado)
        juego.run()

    def mostrar_menu(self):
        # Añadir opciones de selección de color y botones para iniciar el juego o volver al menú principal
        self.menu.clear()
        self.menu.add.selector("Color:", [("Verde", GREEN), ("Rojo", RED), ("Azul", BLUE)], onchange=self.set_color)
        self.menu.add.button("Iniciar Juego", self.iniciar_juego)
        self.menu.add.button("Volver al Menú Principal", self.menu_principal.mostrar_menu)

        # Mostrar el menú de transición
        self.menu.mainloop(self.screen)


# Código principal
if __name__ == "__main__":
    menu_principal = MenuPrincipal(screen)
    menu_principal.mostrar_menu()
