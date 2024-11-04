import pygame
import pygame_menu
import sys

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Juego:
    def __init__(self, screen, menu_principal, color_cuadrado):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.counter = 0
        self.menu_principal = menu_principal
        self.color_cuadrado = color_cuadrado  # Color seleccionado para el cuadrado
        self.menu_ajustes = MenuAjustes(screen, menu_principal)  # Crear el menú de ajustes

        # Definir los rectángulos de los botones
        self.pause_button_rect = pygame.Rect(50, 100, 100, 50)  # Botón para pausar
        self.counter_button_rect = pygame.Rect(250, 100, 100, 50)  # Botón para aumentar el contador
        self.settings_button_rect = pygame.Rect(50, 200, 100, 50)  # Botón para ajustes

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)

            # Dibuja los botones
            pygame.draw.rect(self.screen, BLUE, self.pause_button_rect)  # Botón de pausa
            pygame.draw.rect(self.screen, self.color_cuadrado, self.counter_button_rect)  # Botón de contador

            # Renderiza y muestra el contador
            counter_text = self.font.render(f"Contador: {self.counter}", True, (0, 0, 0))
            self.screen.blit(counter_text, (150, 50))

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button_rect.collidepoint(event.pos):
                        # Abre el menú de pausa
                        self.menu_ajustes.activar_menu_ajustes()
                        self.menu_ajustes.mostrar_menu_ajustes()
                    elif self.counter_button_rect.collidepoint(event.pos):
                        # Aumenta el contador
                        self.counter += 1

            pygame.display.flip()

        pygame.quit()
        sys.exit()

class MenuInicio:
    def __init__(self, screen):
        self.pantalla = screen
        self.menu_inicio = pygame_menu.Menu(title="Nonogram", width=700, height=500, theme=pygame_menu.themes.THEME_DARK)

    def mostrar_menu_inicio(self):
        self.menu_inicio.clear()
        self.menu_inicio.add.button('Jugar', self.activar_menu_opciones_juego)
        self.menu_inicio.add.button('Configuración', self.activar_menu_configuracion)
        self.menu_inicio.add.button('Salir', pygame_menu.events.EXIT)

        self.menu_inicio.mainloop(self.pantalla)

    def activar_menu_configuracion(self):
        menu_configuracion = MenuConfiguracion(self.pantalla, self)
        menu_configuracion.mostrar_menu_configuracion()

    def activar_menu_opciones_juego(self):
        menu_opciones_juego = MenuOpcionesJuego(self.pantalla, self)
        menu_opciones_juego.mostrar_menu_opciones_juego()

class MenuConfiguracion:
    def __init__(self, screen, menu_inicial):
        self.pantalla = screen
        self.menu_inicio = menu_inicial
        self.menu_configuracion = pygame_menu.Menu(title="Ajustes", width=700, height=500, theme=pygame_menu.themes.THEME_DARK)

    def mostrar_menu_configuracion(self):
        self.menu_configuracion.clear()
        self.menu_configuracion.add.button(title="Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_configuracion.mainloop(self.pantalla)

class MenuOpcionesJuego:
    def __init__(self, screen, menu_inicio):
        self.pantalla = screen
        self.menu_inicio = menu_inicio
        self.menu_opciones_juego = pygame_menu.Menu(title="Seteo del nivel", width=700, height=500, theme=pygame_menu.themes.THEME_DARK)
        self.color_cuadrado = BLUE

    def set_color(self, color):
        self.color_cuadrado = color

    def iniciar_juego(self):
        juego = Juego(self.pantalla, self.menu_inicio, self.color_cuadrado)
        juego.run()

    def mostrar_menu_opciones_juego(self):
        self.menu_opciones_juego.clear()
        self.menu_opciones_juego.add.selector('Color: ', [('Azul', BLUE), ('Rojo', RED), ('Verde', GREEN)], onchange=lambda _, color: self.set_color(color))
        self.menu_opciones_juego.add.button("Jugar", action=self.iniciar_juego)
        self.menu_opciones_juego.add.button("Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_opciones_juego.mainloop(self.pantalla)

class MenuAjustes:
    def __init__(self, screen, menu_inicio):
        self.pantalla = screen
        self.menu_inicio = menu_inicio
        self.menu_ajustes = pygame_menu.Menu("Opciones de juego", 600, 400, theme=pygame_menu.themes.THEME_DARK)

    def mostrar_menu_ajustes(self):
        self.menu_ajustes.clear()
        self.menu_ajustes.add.button("Continuar", action=self.apagar_menu_ajustes)
        self.menu_ajustes.add.button("Salir", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_ajustes.mainloop(self.pantalla)

    def activar_menu_ajustes(self):
        self.menu_ajustes.clear()
        self.menu_ajustes.enable()

    def apagar_menu_ajustes(self):
        self.menu_ajustes.disable()

# Código principal
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Juego con Menús y Contador")

if __name__ == "__main__":
    menu_inicio = MenuInicio(screen)
    menu_inicio.mostrar_menu_inicio()
