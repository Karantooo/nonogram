import pygame
import pygame_menu

class Colores:
    BLANCO = (255, 255, 255)
    AZUL = (0, 0, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    VERDE = (0, 255, 0)
    AMARILLO = (255, 255, 0)

class Popup:
    def __init__(self, width: int, height: int, mensaje: str, font_size=20, alpha=230, bg_color=(30, 30, 30), text_color=Colores.BLANCO, padding=20):
        """
        Clase para manejar popups en Pygame.

        :param width: Ancho del popup.
        :param height: Altura del popup.
        :param mensaje: Mensaje que se mostrará en el popup.
        :param font_size: Tamaño de la fuente del mensaje.
        :param alpha: Nivel de transparencia (0-255).
        :param bg_color: Color de fondo del popup.
        :param text_color: Color del texto.
        :param padding: Espacio entre el texto y los bordes del popup.
        """
        self.width = width
        self.height = height
        self.font_size = font_size
        self.alpha = alpha
        self.bg_color = bg_color
        self.text_color = text_color
        self.padding = padding
        self.active = False
        self.mensaje = mensaje

        # Crear la superficie del popup
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_alpha(self.alpha)
        self.surface.fill(self.bg_color)

        # Fuente para el texto
        self.font = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS, self.font_size)
        self.text_lines = self._split_text_into_lines(mensaje)

    def _split_text_into_lines(self, texto: str) -> list[str]:
        """
        Divide el texto en líneas que se ajusten al ancho del popup.

        :param texto: Texto completo.
        :return: Lista de líneas de texto.
        """
        words = texto.split()  # Separar el texto por palabras
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_width, _ = self.font.size(test_line)

            if text_width + self.padding * 2 <= self.width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        # Agregar la última línea si no está vacía
        if current_line:
            lines.append(current_line)

        return lines

    def mostrar(self):
        self.active = True

    def ocultar(self):
        self.active = False

    def imprimir(self, screen):
        if self.active:
            screen_rect = screen.get_rect()
            popup_x = (screen_rect.width - self.width) // 2
            popup_y = (screen_rect.height - self.height) // 2
            self.surface.fill(self.bg_color)  # Rellenar el fondo del popup

            # Dibujar texto centrado en múltiples líneas
            y_offset = self.padding
            for line in self.text_lines:
                text_surface = self.font.render(line, True, self.text_color)
                text_rect = text_surface.get_rect(center=(self.width // 2, y_offset + self.font_size // 2))
                self.surface.blit(text_surface, text_rect)
                y_offset += self.font_size + 5  # Espaciado entre líneas

            screen.blit(self.surface, (popup_x, popup_y))

    def handle_event(self, event):
        """Maneja eventos para cerrar el popup."""
        if self.active and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
            self.ocultar()


# Función principal
def main():
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Popup con texto multilínea")
    clock = pygame.time.Clock()

    # Crear menú principal
    menu = pygame_menu.Menu("Ejemplo de Popup", 600, 400, theme=pygame_menu.themes.THEME_DARK)
    popup = Popup(
        400, 200,
        "Este es un mensaje de ejemplo que es muy largo y debe ser dividido en varias líneas dentro del popup. "
        "asdasd adadaaaaa aaaaaaaaa aaaaaaaaaaa aaaaaaaaaaa aaaaaaaaaaa aaaaaaaaaaa aaaaaaaaaaaa aaaaaaaaa aaaaaaa aaaaa "
        "aaaaaaa aaaaaaaaa aaaaaaaaaa aaaaaaaaaaa aaaaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaaa aaaaaaaa fin"
    )

    menu.add.button("Mostrar Popup", popup.mostrar)
    menu.add.button("Salir", pygame_menu.events.EXIT)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # Manejar eventos del popup
            popup.handle_event(event)

        # Dibujar menú o popup
        screen.fill((50, 50, 50))

        if popup.active:
            popup.imprimir(screen)
        else:
            menu.update(events)
            menu.draw(screen)


        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# Ejecutar
if __name__ == "__main__":
    pygame.init()
    main()
