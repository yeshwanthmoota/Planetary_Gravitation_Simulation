# Physics Gravitation simulation

import pygame
import os
import sys
from constants import *
from physics import *

pygame.init()

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planetary Gravitation Simulation")

def draw_display(planets):
    gameDisplay.fill(BLACK)
    for planet in planets:
        pygame.draw.circle(gameDisplay, planet.color, (planet.x, planet.y), planet.radius, 3)
    pygame.display.update()


PLANET_RADIUS = 20
PLANET_COLOR = WHITE
vel_x, vel_y = 0, 0
CHOICE = False
# frame_counter = 0

def main():
    clock = pygame.time.Clock()
    running = True
    planets = []
    global PLANET_RADIUS
    global PLANET_COLOR
    global CHOICE
    global vel_x, vel_y
    # global frame_counter


    new_planet = Planet(WIDTH/2, HEIGHT/2, 100, YELLOW, CHOICE, planets)
    planets.append(new_planet)

    while running:
        clock.tick(FPS)
        # frame_counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                    planet_pos = pygame.mouse.get_pos()
                    new_planet = Planet(planet_pos[0], planet_pos[1], PLANET_RADIUS, PLANET_COLOR, CHOICE, planets)
                    planets.append(new_planet)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    PLANET_RADIUS = 20
                    PLANET_COLOR = WHITE
                    CHOICE = False
                if event.key == pygame.K_2:
                    PLANET_RADIUS = 40
                    PLANET_COLOR = RED
                    CHOICE = False
                if event.key == pygame.K_3:
                    PLANET_RADIUS = 60
                    PLANET_COLOR = GREEN
                    CHOICE = False
                if event.key == pygame.K_4:
                    PLANET_RADIUS = 80
                    PLANET_COLOR = BLUE
                    CHOICE = False
                if event.key == pygame.K_5:
                    PLANET_RADIUS = 100
                    PLANET_COLOR = YELLOW
                    CHOICE = False
                if event.key == pygame.K_6: # Orbital velocity
                    PLANET_RADIUS = 20
                    PLANET_COLOR = WHITE
                    CHOICE = 1
                if event.key == pygame.K_7: # escape velocity
                    PLANET_RADIUS = 20
                    PLANET_COLOR = RED
                    CHOICE = 2
                if event.key == pygame.K_8: # elliptical launch
                    PLANET_RADIUS = 20
                    PLANET_COLOR = GREEN
                    CHOICE = 3
                if event.key == pygame.K_9: # High Speed Bullet launch
                    PLANET_RADIUS = 20
                    PLANET_COLOR = BLUE
                    CHOICE = 4        



        Planet.motion(planets)
        Planet.planetCollision(planets)
        draw_display(planets)
    pygame.quit()


if __name__=='__main__':
    main()
