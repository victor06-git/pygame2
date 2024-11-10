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
YELLOW = (255, 255, 0)

pygame.init()
clock = pygame.time.Clock()

# Definir la finestra
screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
pygame.display.set_caption('deures003')

window_size = { 
    "width": 0, 
    "height": 0, 
    "center": {
        "x": 0,
        "y": 0
    } 
}
mouse_pos = { "x": -1, "y": -1 }
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
    global mouse_pos
    mouse_inside = pygame.mouse.get_focused()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Botó tancar finestra
            return False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_inside:
                mouse_pos["x"] = event.pos[0]
                mouse_pos["y"] = event.pos[1]
            else:
                mouse_pos["x"] = -1
                mouse_pos["y"] = -1
    return True

# Fer càlculs
def app_run():
    global window_size

    window_size["width"] = screen.get_width()
    window_size["height"] = screen.get_height()
    window_size["center"]["x"] = int(screen.get_width() / 2)
    window_size["center"]["y"] = int(screen.get_height() / 2)

# Dibuixar
def app_draw():
    screen.fill(WHITE)
    utils.draw_grid(pygame, screen, 50)
    
    #Rectangle exterior
    rect_ample = window_size["width"] - 100 
    rect_altura = window_size["height"] - 100
    pygame.draw.rect(screen, BLACK, (50, 50, rect_ample, rect_altura), 4)

    #Linea vertical i horitzontal
    pygame.draw.line(screen, BLACK, (window_size["center"]["x"], 0),(window_size["center"]["x"], window_size["height"]), 4)
    pygame.draw.line(screen, BLACK, (0, window_size["center"]["y"]),(window_size["width"], window_size["center"]["y"]), 4)
    
    x1 = mouse_pos["x"] - 20
    y1 = mouse_pos["y"] - 20
    color = get_color(x1, y1, 50, 50, rect_ample, rect_altura)

    #Definir quadre que es mou
    pygame.draw.rect(screen, color, (x1, y1, 40, 40))
    pygame.draw.rect(screen, BLACK, (x1, y1, 40, 40), 2)

    pygame.display.update()

def get_color(x2, y2, x3, y3, rect_ample, rect_altura):
    color= BLACK

    if x2 < x3 or x2 > (x3 + rect_ample) or y2 < y3 or y2 > (y3 + rect_altura):
        return color
    
    if x2 < window_size["center"]["x"]:
        if y2 < window_size["center"]["y"]:
            return RED
        else:
            return GREEN 
    else:
        if y2 < window_size["center"]["x"]:
            return BLUE
        else:
            return YELLOW   

if __name__ == "__main__":
    main()