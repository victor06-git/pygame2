import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils
import random

# Definir colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
clock = pygame.time.Clock()

# Definir la finestra
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('deures010')


font_1 = pygame.font.SysFont("Arial", 14)
font_2 = pygame.font.SysFont("Arial", 12)

window_size = { 
    "width": 0, 
    "height": 0, 
    "center": {
        "x": 0,
        "y": 0
    } 
}


level = 1
mouse_pos = {"x": 325, "y": 200}

snake = {
    "queue": [],
    "speed": 50,
    "radius": 7,
    "status": "follow_mouse", # "follow_mouse" or "orbit_mouse"
    "direction_angle": 0
}

piece = { # (manzana)
    "x": -1, 
    "y": -1, 
    "value": 0,
    "radius": 7
}  

# Bucle de l'aplicació
def main():
    is_looping = True

    init_game()

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
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Botó tancar finestra
            return False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos["x"], mouse_pos["y"] = event.pos

    return True

# Fer càlculs
def app_run():
    set_window_size()
    delta_time = clock.get_time() / 1000.0

    move_snake(delta_time)

# Dibuixar
def app_draw():
    screen.fill(WHITE)
    
    draw_board()
    draw_piece()
    draw_snake()
    pygame.display.update()

def set_window_size():
    global window_size

    window_size["width"] = screen.get_width()
    window_size["height"] = screen.get_height()
    window_size["center"]["x"] = int(screen.get_width() / 2)
    window_size["center"]["y"] = int(screen.get_height() / 2)

def init_game():
    global snake
# Inicia el joc creant la primera peça si no existeix i col·locant la serp al centre de la pantalla.
    set_window_size() #Mida de la finestra
    
    if piece["x"] == -1: #Si no existeix poma, creala
        generate_piece()

    #Es defineix la llista points de la snake amb la primera posició al centre de la pantalla.
    snake["points"] = []
    snake["queue"].append({'x': window_size["center"]["x"], 'y': window_size["center"]["y"]})
    for cnt in range(4): #Afegeix cercles per aumentar la mida fins a 5
        extend_snake()

def generate_piece():
    #Genera les coordenades de la poma amb el seu valor
    piece["x"] = random.randint(100, window_size["width"] - 100) 
    piece["y"] = random.randint(100, window_size["height"] - 100)
    piece["value"] = random.randint(1, 4)
# Genera una nova peça amb una posició i un valor aleatori dins dels límits de la finestra.

def extend_snake():
    ultim = len(snake["queue"]) - 1 #A partir de la longitud de la llista de queue li resta 1 unitat perquè dona els valors des de 0
    #Afegeix un nou cercle a la llista de queue amb les coordenades de l'últim
    snake["queue"].append({
        "x": snake["queue"][ultim]["x"],
        "y": snake["queue"][ultim]["y"]
    })
# Afegeix un segment addicional a la cua de la serp copiant l'última posició de la cua actual.

def move_snake(delta_time):
    global  level

    if not snake["queue"]:
        print("Error: Snake queue is empty!")
        return

    xoc = utils.is_point_in_circle(snake["queue"][0], piece, piece["radius"])
    if xoc:
        level += 1
        snake["speed"] = snake["speed"] * 1.05 #Augmentar la velocitat de la serp
        if snake["speed"] > 200:
            snake["speed"] = 200 #Limitar la velocitat de la serp
        for _ in range(piece['value']):
            extend_snake()
        generate_piece()

    next_pos = get_next_snake_pos(delta_time)

    snake["queue"].insert(0, next_pos)

    snake["queue"].pop()
# Detecta si la serp ha xocat amb la peça, augmenta la velocitat i la longitud de la serp segons el valor de la peça, i genera una nova peça si cal. Calcula i actualitza la nova posició del cap de la serp i elimina l'últim segment per mantenir la longitud constant.
def get_next_snake_pos(delta_time):
    global snake

    # Calcula la diferència en les coordenades entre el cap de la serp i el ratolí
    delta_x = mouse_pos['x'] - snake["queue"][0]['x']
    delta_y = mouse_pos['y'] - snake["queue"][0]['y']
   
    # Calcula la distància entre el cap de la serp i la posició del ratolí
    distancia = math.hypot(delta_x, delta_y)

    # Determina l'estat de la serp segons la distància al ratolí
    if distancia < 5:
        snake["status"] = 'orbit_mouse'  # Estat per orbitar prop del ratolí
    if distancia > 50:
        snake["status"] = 'follow_mouse'  # Estat per seguir el ratolí

    # Si la serp està en estat d'òrbita, 
    # augmenta l'angle de direcció per fer-la girar
    if snake["status"] == 'orbit_mouse':
        snake["direction_angle"] += distancia * math.pi / 1000
    else:
        # Calcula el pendent per obtenir l'angle; 
        # si delta_x és 0, s'estableix a infinit per evitar divisió per zero
        if delta_x != 0:
            pendent = delta_y / delta_x
        else:
            pendent = float('inf')

        # Calcula l'angle de direcció de la serp per seguir el ratolí
        if delta_x == 0 and mouse_pos['y'] < snake["queue"][0]['y']:
            # Angle per anar amunt (270 graus)
            snake["direction_angle"] = (3 * math.pi) / 2
        elif delta_x == 0 and mouse_pos['y'] >= snake["queue"][0]['y']:
            # Angle per anar avall (90 graus)
            snake["direction_angle"] = math.pi / 2
        elif mouse_pos['x'] > snake["queue"][0]['x']:
            # Angle per anar cap a la dreta 
            snake["direction_angle"] = math.atan(pendent)
        else:
            # Angle per anar cap a l'esquerra (180 graus)
            snake["direction_angle"] = math.atan(pendent) + math.pi

    return {
        "x": snake["queue"][0]['x'] + snake["speed"] * delta_time * math.cos(snake["direction_angle"]), 
        "y": snake["queue"][0]['y'] + snake["speed"] * delta_time * math.sin(snake["direction_angle"])
    }

def draw_board():
    level_txt = font_1.render(f'Level: {level}', True, BLACK)
    length_txt = font_1.render(f'Length: {len(snake["queue"])}', True, BLACK)
    speed_txt = font_1.render(f'Speed: {snake["speed"]:.2f}', True, BLACK)
    screen.blit(level_txt, (15, 15))
    screen.blit(length_txt, (15, 35))
    screen.blit(speed_txt, (15, 55))
# Mostra el nivell, la longitud de la serp, i la velocitat actual a la pantalla.

def draw_snake():
    for cnt in reversed(range(len(snake["queue"]))):
        circle = snake["queue"][cnt]
        if len(snake["queue"]) > 1:
            lightness = int((cnt * 225) / (len(snake["queue"]) - 1))
        else:
            lightness = 0
        color = (lightness, lightness, lightness)
        pygame.draw.circle(screen, color, (int(circle["x"]), int(circle["y"])), snake["radius"])
# Dibuixa la serp segment per segment, aplicant un efecte de lluminositat que varia segons la posició del segment dins la cua.

def draw_piece():
    color = RED
    circle_coord = (int(piece["x"]), int(piece["y"]))
    pygame.draw.circle(screen, color, circle_coord, piece["radius"])

    text = font_2.render(str(piece["value"]), True, BLACK)
    text_rect = text.get_rect(center=circle_coord)
    screen.blit(text, text_rect)
# Dibuixa la peça actual a la pantalla en color vermell, incloent-hi el seu valor al centre de la peça.
 
if __name__ == "__main__":
    main()