import pygame
import sys
import random
import math

# Inicializar pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 900, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🎂 ¡Feliz Cumpleaños, Diego! 🎉")

# Cargar imágenes
pastel = pygame.image.load("pastel.png").convert_alpha()
fuegos = pygame.image.load("fuegos.gif").convert_alpha()

# Escalar imágenes (pastel más grande, fuegos más grandes)
pastel = pygame.transform.scale(pastel, (300, 300))
fuegos = pygame.transform.scale(fuegos, (160, 160))

# Cargar música
try:
    pygame.mixer.music.load("musica.mp3")
    pygame.mixer.music.play(-1)  # Reproducir en bucle
except:
    print("⚠️ No se pudo cargar la música, pero el juego funcionará igual.")

# Colores y fondo
COLORES_FONDO = [
    (255, 182, 193),  # rosa
    (173, 216, 230),  # celeste
    (255, 255, 153),  # amarillo suave
    (144, 238, 144),  # verde claro
    (221, 160, 221)   # violeta claro
]

# Fuente
fuente = pygame.font.Font(None, 80)
fuente_peque = pygame.font.Font(None, 40)

# Posición del pastel
pastel_x = ANCHO // 2 - 150
pastel_y = ALTO - 320

# Sistema de partículas (fuegos artificiales)
class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radio = random.randint(3, 7)
        self.color = color
        self.vel_x = random.uniform(-4, 4)
        self.vel_y = random.uniform(-5, -1)
        self.tiempo_vida = random.randint(40, 70)

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.1  # gravedad
        self.tiempo_vida -= 1

    def dibujar(self, pantalla):
        if self.tiempo_vida > 0:
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)

# Lista de partículas activas
fuegos_lista = []

# Reloj
clock = pygame.time.Clock()

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fondo cambiante
    tiempo = pygame.time.get_ticks()
    color_idx = (tiempo // 800) % len(COLORES_FONDO)
    pantalla.fill(COLORES_FONDO[color_idx])

    # Dibujar pastel
    pantalla.blit(pastel, (pastel_x, pastel_y))

    # Texto principal
    texto = fuente.render("🎉 ¡Feliz cumpleaños, Diego! 🎂", True, (0, 0, 0))
    texto_rect = texto.get_rect(center=(ANCHO // 2, 100))
    pantalla.blit(texto, texto_rect)

    # Texto pequeño
    subtexto = fuente_peque.render("Toca o haz clic para lanzar fuegos artificiales ✨", True, (0, 0, 0))
    subtexto_rect = subtexto.get_rect(center=(ANCHO // 2, ALTO - 40))
    pantalla.blit(subtexto, subtexto_rect)

    # Detectar clic/tacto
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        color_random = random.choice([
            (255, 99, 71), (135, 206, 250), (255, 215, 0),
            (255, 105, 180), (144, 238, 144), (186, 85, 211)
        ])
        for _ in range(25):  # más partículas = más fuegos
            fuegos_lista.append(Particula(x, y, color_random))

    # Actualizar y dibujar partículas
    for f in fuegos_lista[:]:
        f.mover()
        f.dibujar(pantalla)
        if f.tiempo_vida <= 0:
            fuegos_lista.remove(f)

    pygame.display.flip()
    clock.tick(60)

