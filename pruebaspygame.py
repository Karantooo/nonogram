import pygame
import numpy as np
import random

def get_num_arriba(a):
    val = []
    for i in range(a.shape[1]):
        val2 = []
        cant = 0
        bot = False
        for j in range(a.shape[0]):
            x = a[j][i]
            if a[j][i] == 1:
                if not bot:
                    bot = True
                    cant += 1
                else:
                    cant += 1
            else:
                if bot:
                    bot = False
                    val2.insert(0, cant)
                    cant = 0
        if cant != 0:
            val2.insert(0, cant)
        val.append(val2)
    return val

def get_num_lado(a):
    val = []
    for i in range(a.shape[0]):
        val2 = []
        cant = 0
        bot = False
        for j in range(a.shape[1]):
            x = a[i][j]
            if a[i][j] == 1:
                if not bot:
                    bot = True
                    cant += 1
                else:
                    cant += 1
            else:
                if bot:
                    bot = False
                    val2.insert(0, cant)
                    cant = 0
        if cant != 0:
            val2.insert(0, cant)
        val.append(val2)
    return val
def pcc_array_a_matriz(a):
    fila = a // 4
    columna = a % 4
    return (fila, columna)


# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Mi primer juego en Pygame")

# Definir colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Tamaño de los botones
ancho_boton = 100
alto_boton = 50
espacio = 10

# Crear una fuente para los números
fuente = pygame.font.SysFont('Arial', 24)

# Crear una lista para almacenar los rectángulos de los botones
botones = []
valores = np.random.randint(0, 2, size=16)
matriz = valores.reshape(4, 4)
num_up = get_num_arriba(matriz)
num_side = get_num_lado(matriz)
mpunos = np.zeros((4,4))
puntos = [0] * 16
vidas = 3

# Crear los botones en una cuadrícula 4x4
for fila in range(4):
    for columna in range(4):
        boton_rect = pygame.Rect(
            300 + columna * (ancho_boton + espacio),  # X: posición horizontal con espacio
            200 + fila * (alto_boton + espacio),     # Y: posición vertical con espacio
            ancho_boton,                             # Ancho del botón
            alto_boton                               # Alto del botón
        )
        botones.append(boton_rect)

# Bucle principal del juego
print(valores)
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # Obtener la posición del ratón al hacer clic
            for boton_rect in botones:
                if boton_rect.collidepoint(mouse_pos):
                    indice = botones.index(boton_rect)
                    print(f"Botón en {boton_rect.topleft} clicado")
                    if valores[indice] == 1:
                        print(f"Botón {indice} activado correctamente")
                        puntos[indice] = 1
                        aux = pcc_array_a_matriz(indice)
                        mpunos[aux[0]][aux[1]] = 1
                    else:
                        print(f"Botón {indice} activado incorrectamente")
                        vidas -= 1
                        puntos[indice] = 2
                    print(f"{valores}\n")
                    print(f"{puntos}\n")
    if vidas == 0:
        corriendo = False
    if np.array_equal(mpunos, matriz):
        corriendo = False
        print("gg")
    
    # Llenar la pantalla de blanco
    screen.fill(BLANCO)

    # Dibujar los botones con fila y columna
    for i, boton_rect in enumerate(botones):
        if puntos[i] == 0:
            pygame.draw.rect(screen, AZUL, boton_rect)
        elif puntos[i] == 1:
            pygame.draw.rect(screen, VERDE, boton_rect)
        elif puntos[i] == 2:
            pygame.draw.rect(screen, ROJO, boton_rect)

        pygame.draw.rect(screen, NEGRO, boton_rect, 2)  # Borde negro del botón

        # Renderizar el texto como "fila, columna"
        texto = fuente.render(f'{i}', True, NEGRO)
        texto_rect = texto.get_rect(center=boton_rect.center)

        # Dibujar el texto en el centro del botón
        screen.blit(texto, texto_rect)

    # Dibujar los números arriba (num_up) en el centro de la ventana
    for i, nums in enumerate(num_up):
        for j, num in enumerate(nums):
            texto = fuente.render(str(num), True, NEGRO)
            texto_rect = texto.get_rect(center=(350 + i * (ancho_boton + espacio), 150 - j * 30))
            screen.blit(texto, texto_rect)

    # Dibujar los números a los lados (num_side) en el centro de la ventana
    for i, nums in enumerate(num_side):
        for j, num in enumerate(nums):
            texto = fuente.render(str(num), True, NEGRO)
            texto_rect = texto.get_rect(center=(250 - j * 30, 225 + i * (alto_boton + espacio)))
            screen.blit(texto, texto_rect)

    # Dibujar el contador de vidas en la esquina superior derecha
    texto_vidas = fuente.render(f'Vidas: {vidas}', True, NEGRO)
    screen.blit(texto_vidas, (screen.get_width() - texto_vidas.get_width() - 20, 20))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar los FPS
    pygame.time.Clock().tick(60)


# Salir de Pygame
pygame.quit()
print(matriz, num_up, num_side)
