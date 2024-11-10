import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils

# Definir colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PINK = (255, 105, 180)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pygame.init()
clock = pygame.time.Clock()

# Definir la finestra
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('deures002')

font_ = pygame.font.SysFont("Arial", 15)

# Bucle de l'aplicació
def main():
    is_looping = True

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60) # Limitar a 60 FPS

    # Fora del bucle, tancar l'aplicació
    pygame.quit()
    sys.exit()

# Gestionar events
def app_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Botó tancar finestra
            return False
    return True

# Fer càlculs
def app_run():
    pass

# Dibuixar
def app_draw():
    screen.fill(WHITE)
    utils.draw_grid(pygame, screen, 50)
    
    pygame.draw.circle(screen, BLUE, (100,50), 5)
    draw_text("Poma", font_, 100, 50, "left", "bottom")

    pygame.draw.circle(screen, BLUE, (250,50), 5)
    draw_text("Plàtan", font_, 250, 50, "left", "top")

    pygame.draw.circle(screen, BLUE, (100,100), 5)
    draw_text("Pera", font_, 100, 100, "center", "center")

    pygame.draw.circle(screen, BLUE, (250,100), 5)
    draw_text("Prèssec", font_, 250, 100, "center", "center")

    pygame.draw.circle(screen, BLUE, (100,150), 5)
    draw_text("Raïm", font_, 100, 150, "right", "top")

    pygame.draw.circle(screen, BLUE, (250,150), 5)
    draw_text("Maduixa", font_, 250, 150, "right", "bottom")
    

    pygame.display.update()

def draw_text(text, font, x, y, align_x, align_y):
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    
    if align_x == 'center':
        text_rect.centerx = x
    elif align_x == 'left':
        text_rect.left = x
    elif align_x == 'right':
        text_rect.right = x
    
    if align_y == 'center':
        text_rect.centery = y
    elif align_y == 'top':
        text_rect.top = y
    elif align_y == 'bottom':
        text_rect.bottom = y

    screen.blit(text_surface, text_rect)
if __name__ == "__main__":
    main()