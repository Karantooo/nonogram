# import pygame
# import pygame_menu
#
# # Inicializar pygame
# pygame.init()
# screen = pygame.display.set_mode((1000, 700))
# pygame.display.set_caption("Menú con pygame-menu")
#
# # Variables del juego
# dificultad = 1
# jugador_pos = [300, 200]
# velocidad = 5
#
# # Función para cambiar la dificultad
# def set_dificultad(selected, value):
#     global dificultad, velocidad
#     dificultad = value
#     velocidad = 5 + (value - 1) * 3
#     print(f"Dificultad seleccionada: {['Difícil', 'Fácil'][value-1]}")
#
# # Función para iniciar el juego
# def start_the_game():
#     global jugador_pos, velocidad
#     jugador_pos = [300, 200]  # Posición inicial del jugador
#     jugando = True
#
#     while jugando:
#         screen.fill((0, 0, 0))  # Fondo negro
#
#         # Dibuja el jugador
#         pygame.draw.rect(screen, (255, 0, 0), (*jugador_pos, 50, 50))
#
#         # Manejo de eventos
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 jugando = False
#
#         # Movimiento del jugador con teclas
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT]:
#             jugador_pos[0] -= velocidad
#         if keys[pygame.K_RIGHT]:
#             jugador_pos[0] += velocidad
#         if keys[pygame.K_UP]:
#             jugador_pos[1] -= velocidad
#         if keys[pygame.K_DOWN]:
#             jugador_pos[1] += velocidad
#
#         pygame.display.flip()
#
# # Funciones para cambiar entre menús
# def abrir_menu2():
#     menu2.enable()  # Habilitar el segundo menú
#     menu.disable()  # Deshabilitar el menú principal
#
# def volver_menu1():
#     menu.enable()  # Habilitar el menú principal
#     menu2.disable()  # Deshabilitar el segundo menú
#
# # Crear tema para el menú
# mi_tema = pygame_menu.Theme(
#     background_color=(40, 0, 40),  # Fondo morado oscuro
#     title_background_color=(255, 0, 0),  # Fondo del título rojo
#     title_font_shadow=True,  # Sombra en el texto del título
#     widget_font=pygame_menu.font.FONT_BEBAS,  # Fuente Bebas
#     widget_font_color=(255, 255, 255),  # Color de fuente blanco
#     widget_background_color=(50, 50, 50),  # Fondo de los widgets gris
#     widget_padding=20  # Espaciado alrededor de cada widget
# )
#
# # Crear menús
# menu = pygame_menu.Menu('', 400, 300, theme=mi_tema)
# menu2 = pygame_menu.Menu("Opciones", 400, 300, theme=mi_tema)
#
# # Agregar elementos al menú principal
# menu.add.text_input('Nombre :', default='John Doe')
# menu.add.selector('Dificultad :', [('Dificil', 1), ('Fácil', 2)], onchange=set_dificultad)
# menu.add.button('Jugar', abrir_menu2)  # Aquí se pasa la referencia a la función
# menu.add.button('Salir', pygame_menu.events.EXIT)
#
# # Agregar elementos al menú de opciones
# menu2.add.button("Jugar", start_the_game)  # Aquí se pasa la referencia a la función
# menu2.add.button("Volver", volver_menu1)  # Aquí se pasa la referencia a la función
#
# # Habilita el menú principal al inicio
# menu.enable()
# menu2.disable()
# # Bucle principal
# while True:
#     screen.fill((0, 0, 0))
#
#     # Captura eventos de pygame
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.QUIT:
#             exit()
#
#     # Actualiza y dibuja el menú en la pantalla
#     if menu.is_enabled():
#         menu.draw(screen)
#         menu.update(events)
#     if menu2.is_enabled():
#         menu2.draw(screen)
#         menu2.update(events)
#     pygame.display.flip()
