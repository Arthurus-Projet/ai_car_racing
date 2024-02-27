import pygame
import sys
import math
import numpy as np
from scipy.interpolate import CubicSpline
from map import Map
from car import Car
from time import sleep
import configs
from  genetic_algorithm import GeneticAlgorithm
from manager_save_load import load_class


pygame.init()
pygame.display.set_caption("AI Racing Car")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
myfont = pygame.font.SysFont('Berlin sans FB', 40)

map_ = load_class("circuit")

NUMBER_INDIVIDUALS = 100
generation_number = 1
individuals = GeneticAlgorithm(NUMBER_INDIVIDUALS, 3, 6, 2, map_)
fitness = 0

x_text, y_text = 590, 70
neural_network_position = (510, 600)

while True:
    in_game = True
    while in_game:
        for event in pygame.event.get():
            # Press the red cross if you want the new generation :
            if event.type == pygame.QUIT:
                in_game = False

        screen.fill(configs.BLUE)

        num_alive_cars = 0
        for i in range(NUMBER_INDIVIDUALS):
            if individuals.cars[i].alive:
                num_alive_cars += 1
                individuals.cars[i].draw_car_with_lines(screen, individuals, i)  # Dessiner la voiture
                action = individuals.individual_action(i)
                individuals.cars[i].angle = (individuals.cars[i].angle + (action) * 10)  % 360
                individuals.cars[i].x -= individuals.cars[i].speed * math.cos(math.radians((individuals.cars[i].angle) % 360))
                individuals.cars[i].y += individuals.cars[i].speed * math.sin(math.radians((individuals.cars[i].angle) % 360))

        # Displays the neural network of a living car
        for i in range(NUMBER_INDIVIDUALS):
            if individuals.cars[i].alive:
                individuals.individuals[i].plot_neural_network_graph(screen, neural_network_position, [individuals.cars[i].line_length_1, individuals.cars[i].line_length_2, individuals.cars[i].line_length_3])
                fitness = individuals.cars[i].fitness
                break

        for curve in map_.curves:
            pygame.draw.lines(screen, configs.LIGHT_BLUE, False, curve.T, 5)

        # The number of current generations, the number of living cars and the fitness level are displayed.
        generation_display = myfont.render('Generation : ' + str(generation_number), 0, configs.WHITE)
        voitures_display = myfont.render('Cars : ' + str(num_alive_cars), 0, configs.WHITE)
        fitness_display = myfont.render('fitness : ' + str(fitness), 0, configs.WHITE)

        screen.blit(generation_display, (x_text, y_text))
        screen.blit(voitures_display, (x_text, y_text + 40))
        screen.blit(fitness_display, (x_text, y_text + 80))


        pygame.display.flip()
        clock.tick(30)

        if num_alive_cars == 0:
            in_game = False

    individuals.reproduction()
    individuals.mutation(32, 32, 32, 0.01)
    individuals.cars = [Car(map_) for _ in range(NUMBER_INDIVIDUALS)]
    generation_number += 1

pygame.quit()
sys.exit()
