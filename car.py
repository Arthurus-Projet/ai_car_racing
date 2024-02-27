import pygame
import math
import numpy as np
from random import randint
import configs

class Car:
    def __init__(self, map_):
        """
        Initialize a Car object.

        Args:
        - map_ (object): An instance of the Map class.
        """
        self.map_ = map_
        self.width = 50
        self.height = 30
        self.cpt = 0
        self.alive = True
        self.x = 180
        self.y = 180
        self.speed = 10
        self.angle = 90
        self.fitness = -1
        self.line_length = 400
        color_variation = 10
        self.BLUE_LIGHT = (
            randint(172 - color_variation, 202 + color_variation),
            randint(183 - color_variation, 213 + color_variation),
            randint(203 - color_variation, 233 + color_variation)
        )

    def collision(self, positions):
        """
        Check for collisions with curves.

        Args:
        - positions (list): List of points representing the car's position.

        Returns:
        - bool: True if collision detected, False otherwise.
        """
        if self.line_length_1 < 3 and self.line_length_2 < 3 and self.line_length_3 < 3:
            self.alive = False
            return True

        for pos in positions:
            modulo_rest_x = pos[0] % self.map_.len_seq
            key_x = int(pos[0] - modulo_rest_x)

            modulo_rest_y = pos[1] % self.map_.len_seq
            key_y = int(pos[1] - modulo_rest_y)

            key = str(key_x) + ' ' + str(key_y)

            try:
                if self.map_.curves_binary[key]:
                    self.alive = False
                    return True
            except:
                self.alive = False
                return True

        return False

    def get_car_points(self, opp, opp2, adj, adj2, point):
        """
        Calculate the positions of the car.

        Args:
        - opp (float): Opposite side length.
        - opp2 (float): Second opposite side length.
        - adj (float): Adjacent side length.
        - adj2 (float): Second adjacent side length.
        - point (tuple): Starting point coordinates.

        Returns:
        - list: Points on the car, where we'll test whether they touch a curve.
        """
        if 0 <= self.angle <= 90 or 180 <= self.angle <= 270:
            p1 = (self.x + opp + adj2, self.y + opp2)
            p2 = (self.x + adj2, self.y + opp2 + adj)
            p3 = (self.x + opp, self.y)
            p4 = (self.x, self.y + adj)
            return [p1, p2, p3, p4, point]

        p1 = (self.x + adj + opp2, self.y + opp)
        p2 = (self.x + opp2, self.y)
        p3 = (self.x, self.y + adj2)
        p4 = (self.x + adj, self.y + opp + adj2)
        return [p1, p2, p3, p4, point]

    def point_end_x(self, angle, point_start_x):
        """
        Calculate the x-coordinate of the end point.

        Args:
        - angle (float): Angle of rotation.
        - point_start_x (float): Starting x-coordinate.

        Returns:
        - float: Calculated x-coordinate of the end point.
        """
        return point_start_x - self.line_length * math.cos(math.radians(angle))

    def point_end_y(self, angle, point_start_y):
        """
        Calculate the y-coordinate of the end point.

        Args:
        - angle (float): Angle of rotation.
        - point_start_y (float): Starting y-coordinate.

        Returns:
        - float: Calculated y-coordinate of the end point.
        """
        return point_start_y + self.line_length * math.sin(math.radians(angle))

    def calculate_line_length(self, point_start_x, point_start_y, angle):
        """
        Calculate the end point coordinates.

        Args:
        - point_start_x (float): Starting x-coordinate.
        - point_start_y (float): Starting y-coordinate.
        - angle (float): Angle of rotation.

        Returns:
        - tuple: Coordinates of the end point.
        """
        points_x = np.linspace(point_start_x, self.point_end_x(angle, point_start_x), 90)
        points_y = np.linspace(point_start_y, self.point_end_y(angle, point_start_y), 90)

        for i in range(len(points_x)):
            modulo_rest_x = points_x[i] % self.map_.len_seq
            key_x = int(points_x[i] - modulo_rest_x)

            modulo_rest_y = points_y[i] % self.map_.len_seq
            key_y = int(points_y[i] - modulo_rest_y)

            key = str(key_x) + ' ' + str(key_y)

            try:
                if self.map_.curves_binary[key]:
                    return (points_x[i], points_y[i], i)
            except:
                return (points_x[i], points_y[i], i)

        return (points_x[len(points_x) - 1], points_y[len(points_x) - 1], i)

    def calculate_start_point(self, adj, opp, adj2, opp2):

        if 180 <= self.angle < 270:
            return self.x + opp2/2 + adj, self.y + adj2/2
        elif 90 <= self.angle < 180:
            return self.x + opp + adj2/2, self.y + opp2/2 + adj
        elif 0 <= self.angle < 90:
            return self.x + opp2/2, self.y + adj2/2 + opp
        return self.x + adj2/2, self.y + opp2/2

    def display_car(self, screen, individus, index_car, points_cars):
        action = individus.individual_action(index_car)
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.collision(self.get_car_points(points_cars[0], points_cars[1], points_cars[2], points_cars[3], points_cars[4])):
            pygame.draw.rect(car_surface, configs.RED, (0, 0, self.width, self.height))
        else:
            pygame.draw.rect(car_surface, self.BLUE_LIGHT, (0, 0, self.width, self.height))

        rotated_surface = pygame.transform.rotate(car_surface, self.angle)
        # Display the car
        screen.blit(rotated_surface, (self.x, self.y))

    def display_lines(self, screen, point_start_x, point_start_y):
        if self.alive:
            pygame.draw.line(screen, configs.WHITE, (point_start_x, point_start_y), self.point_end_1[:2], 3)
            pygame.draw.line(screen, self.BLUE_LIGHT, (point_start_x, point_start_y), self.point_end_2[:2], 3)
            pygame.draw.line(screen, self.BLUE_LIGHT, (point_start_x, point_start_y), self.point_end_3[:2], 3)

    def draw_car_with_lines(self, screen, individus, index_car):
        """
        Draw the car on the screen with lines.

        Args:
        - screen (object): Pygame screen object.
        - individus (object): Instance of the Individus class.
        - index_car (int): Index of the car.
        """
        angle_remainder = self.angle % 90
        adj = math.cos(math.radians(angle_remainder)) * self.width
        opp = math.sqrt(self.width**2 - adj**2)

        adj2 = math.cos(math.radians(angle_remainder)) * self.height
        opp2 = math.sqrt(self.height**2 - adj2**2)

        point_start_x, point_start_y = self.calculate_start_point(adj, opp, adj2, opp2)

        self.point_end_1 = self.calculate_line_length(point_start_x, point_start_y, self.angle)
        self.point_end_2 = self.calculate_line_length(point_start_x, point_start_y, self.angle + 30)
        self.point_end_3 = self.calculate_line_length(point_start_x, point_start_y, self.angle - 30)

        self.line_length_1, self.line_length_2, self.line_length_3 = self.point_end_1[2], self.point_end_2[2], self.point_end_3[2]

        self.display_lines(screen, point_start_x, point_start_y)

        points_cars = (opp, opp2, adj, adj2, (point_start_x, point_start_y))
        self.display_car(screen, individus, index_car, points_cars)

        self.fitness += 1
