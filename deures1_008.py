import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils

# Definir colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (100, 200, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)  

pygame.init()
clock = pygame.time.Clock()

# Definir la finestra
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('deures008')

font = pygame.font.SysFont("Arial", 14)

mouse_pos = {"x": -1, "y": -1, "pressed": False, "action": False}
buttons = [
    {"value": "up", "x": 25, "y": 25, "width": 25, "height": 25, "pressed": False},
    {"value": "down", "x": 25, "y": 25, "width": 25, "height": 25, "pressed": False}
]
direction = "up"
position_y = 250
radius = 25

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
                mouse_pos["y"] = -1
                mouse_pos["x"] = -1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos["pressed"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos["pressed"] = False
            mouse_pos["action"] = True
        

    return True

# Fer càlculs
def app_run():
    global buttons, direction, position_y, radius

    for button in buttons:
        if utils.is_point_in_rect(mouse_pos, button):
            if mouse_pos["pressed"] == True:
                button["pressed"] = True
            elif mouse_pos["action"] == True:
                button["pressed"] = False
                direction = button["value"]
        else:
            button["pressed"] = False
    mouse_pos["action"] = False

    delta_time = clock.get_time() / 1000.0
    speed = 50

    if direction == "up":
        position_y = position_y - speed * delta_time
    else:
        position_y = position_y + speed * delta_time

    min_y = radius  
    max_y = screen.get_height() - radius

    if position_y < min_y:
        position_y = min_y
    elif position_y > max_y:
        position_y = max_y

# Dibuixar
def app_draw():
    global  position_y
    screen.fill(WHITE)
    utils.draw_grid(pygame, screen, 50)

    for button in buttons:
        draw_button(button)
        
    center = (500, position_y)
    pygame.draw.circle(screen, BLUE, center, radius)
    
    if mouse_pos["pressed"] == True:
        text = font.render("Mouse Pressed", True, BLACK)
        screen.blit(text, (60,30))

    pygame.display.update()

def draw_button(button):
    color = WHITE

    if button["pressed"] == True:
        color = ORANGE
    elif direction == button["value"]:
        color = BLUE

    rect = (button["x"], button["y"], button["width"], button["height"])
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
if __name__ == "__main__":
    main()