import pygame
from nonogram.visual.colores import Colores
from nonogram.logica.casilla import Casilla


class Boton:
    """
    Esta clase representa un botón en el tablero del juego.
    """

    alto: int                   # Altura del botón
    ancho: int                  # Anchura del botón
    espacio: int                # Espacio entre botones
    identificador: int          # Identificador único del botón
    fuente: pygame.font.Font    # Fuente utilizada para renderizar texto
    boton_visual: pygame.Rect   # Rectángulo que define la posición y tamaño del botón
    dimensiones: tuple          # Dimensiones de la ventana
    bandera_image: pygame.Surface   # Imagen de una bandera
    posicion_bandera: tuple     # Reprecenta las coordenadas de la posicion en que se colocara la bandera

    sonido_correcto: pygame.mixer.Sound         # Clase que representa un objeto de sonido
    sonido_incorrecto: pygame.mixer.Sound       # Clase que representa un objeto de sonido
    sonido_bandera_colocar: pygame.mixer.Sound  # Clase que representa un objeto de sonido
    sonido_bandera_sacar: pygame.mixer.Sound    # Clase que representa un objeto de sonido

    def __init__(
                self,
                fila: int, columna: int,
                alto: int, ancho: int,
                espacio: int, marcado: bool,
                identificador: int, fuente: pygame.font,
                dimensiones: tuple = (1000, 700),
                casilla: Casilla = None
    ) -> None:

        self.alto = alto
        self.ancho = ancho
        self.espacio = espacio
        self.dimensiones = dimensiones

        # Creacion del boton en pygame
        self.boton_visual = pygame.Rect(
                int(self.dimensiones[0] * 0.2) + columna * (self.ancho + self.espacio),  # X: posición horizontal con espacio
                int(self.dimensiones[1] * 0.2) + fila * (self.alto + self.espacio),  # Y: posición vertical con espacio
                self.ancho,  # Ancho del botón
                self.alto  # Alto del botón
        )

        # Inicializacion de variables internas
        self.identificador = identificador
        self.fuente = fuente

        if casilla is None:
            self.casilla = Casilla(marcado=marcado, visibilidad=False, bandera=False)
        else:
            self.casilla = casilla

        # Inicializacion de la imagen de la bandera
        self.bandera_image = pygame.image.load("assets/bandera.png")
        dimension_menor = min(self.alto, self.ancho)
        self.bandera_image = pygame.transform.scale(self.bandera_image, [dimension_menor, dimension_menor])

        # Inicializacion de la posicion de la bandera
        self.posicion_bandera = (self.boton_visual.x + dimension_menor/2,self.boton_visual.y )

        # Carga de archivos de sonido
        self.sonido_correcto = pygame.mixer.Sound('assets/sonidos/casilla_correcta.wav')
        self.sonido_incorrecto = pygame.mixer.Sound('assets/sonidos/casilla_incorrecta.wav')
        self.sonido_bandera_colocar = pygame.mixer.Sound('assets/sonidos/bandera_colocar.wav')
        self.sonido_bandera_sacar = pygame.mixer.Sound('assets/sonidos/bandera_sacar.wav')

        # Ajuste del volumen de sonidos [0,1]
        self.sonido_correcto.set_volume(0.5)
        self.sonido_incorrecto.set_volume(1)
        self.sonido_bandera_colocar.set_volume(1)
        self.sonido_bandera_sacar.set_volume(0.3)

    def get_marcado(self) -> bool:
        return self.casilla.marcado

    def get_visibilidad(self) -> bool:
        return self.casilla.visibilidad

    def imprimir(self, screen: pygame.Surface) -> None:
        if self.casilla.visibilidad:
            if self.casilla.marcado:
                pygame.draw.rect(screen, Colores.NEGRO, self.boton_visual)
            else:
                pygame.draw.rect(screen, Colores.ROJO, self.boton_visual)
        else:
            if self.casilla.bandera:
                pygame.draw.rect(screen, Colores.AZUL, self.boton_visual)
                screen.blit(self.bandera_image, self.posicion_bandera)
            else:
                pygame.draw.rect(screen, Colores.BLANCO, self.boton_visual)

        pygame.draw.rect(screen, Colores.NEGRO, self.boton_visual, 2)  # Borde negro del botón

        # Renderizar el texto como "fila, columna"
        # texto = self.fuente.render(f'{self.identificador}', True, Colores.NEGRO)
        # texto_rect = texto.get_rect(center=self.boton_visual.center)

        # Dibujar el texto en el centro del botón
        # screen.blit(texto, texto_rect)

    def validar_click(self,mouse_pos: tuple[int,int]) -> int: # 0: Incorrecto, 1: Correcto, 2: No se marco este
        if self.boton_visual.collidepoint(mouse_pos) and self.casilla.visibilidad == False:
            self.casilla.visibilidad = True
            self.casilla.bandera = False
            if self.casilla.marcado:
                self.sonido_correcto.play()
                return 1
            else:
                self.sonido_incorrecto.play()
                return 0
        return 2

    def alterar_estado_bandera(self) -> None:
        if not self.casilla.visibilidad:    # Si no se esta mostrando el contenido del boton
            if self.casilla.bandera:
                self.sonido_bandera_sacar.play()
                self.casilla.bandera = False
            else:
                self.sonido_bandera_colocar.play()
                self.casilla.bandera = True
