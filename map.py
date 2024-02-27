import pygame
import sys
import numpy as np
import math
from random import randint
from scipy.interpolate import CubicSpline
import pickle
import configs


class Map:

    def __init__(self):
        """
        Initializes the Map object with default values and generates the initial curve.
        """
        self.liste_points = [np.array([[200, 100], [100, 300], [300, 50], [300, 350]])]
        self.curves = [None]
        self.curves_with_more_points = [None]
        self.curve(0)
        self.current_index = 0
        self.len_seq = 1
        self.curves_binary = {}

    def curve_points(self, number_points, i):
        """
        Generates points for a curve using CubicSpline.

        Args:
            number_of_points (int): Number of points to generate.
            i (int): Index of the curve.

        Returns:
            numpy.ndarray: Array of generated points for the curve.
        """
        t = np.linspace(0, 1, number_points)
        return CubicSpline(range(4), self.liste_points[i].T, axis=1)(t)

    def curve(self, i):
        """
        Generates curves with different point counts.
        The more points there are, the more precise the curve is.

        Args:
            i (int): Index of the curve.
        """
        self.curves[i] = self.curve_points(50, i)
        self.curves_with_more_points[i] = self.curve_points(1500, i)

    def create_new_curve(self):
        """
        Creates a new curve with random starting points and appends it to the list.
        """
        new_starting_points = self.liste_points[self.current_index][1]
        new_starting_points_2 = [(randint(0, configs.SCREEN_WIDTH), randint(0, configs.SCREEN_HEIGHT)) for i in range(3)]

        self.liste_points.append(np.array([new_starting_points, new_starting_points_2[0], new_starting_points_2[1], new_starting_points_2[2]]))
        self.current_index += 1
        self.curves.append(None)
        self.curves_with_more_points.append(None)

    def end_of_loop(self):
        """
        Completes the loop by adjusting the last point of the current curve.
        """
        self.lenght = len(self.liste_points)
        self.liste_points[self.lenght - 1][1] = self.liste_points[0][0] # permet de faire une boucle
        self.curve(self.lenght - 1)
        self.create_new_curve()

    def end_of_second_loop(self):
        """
        Closes the second loop by adjusting the last point of the current curve.
        Create a dictionary indicating, for each key, whether a point of a curve is included in it

        Returns:
            Map: The Map object.
        """
        curve_number_second_loop = len(self.liste_points) - self.lenght
        self.liste_points[len(self.liste_points) - 1][1] = self.liste_points[len(self.liste_points) - curve_number_second_loop][0] # permet de cloturer la seconde boucle
        self.curve(len(self.liste_points) - 1)
        self.save_curves()
        return self

    def save_curves(self):
        '''
        Create a dictionary indicating, for each key, whether a point of a curve is included in it
        '''
        self.len_seq = 8
        for x in range(0, configs.SCREEN_WIDTH + self.len_seq, self.len_seq):
            for y in range(0, configs.SCREEN_HEIGHT + self.len_seq, self.len_seq):
                key = str(x) + ' ' + str(y)
                self.curves_binary[key] = False

        for curve in self.curves_with_more_points:
            for i in range(len(curve[0])):
                modulo_rest_x = curve[0][i] % self.len_seq

                # Getting the key value in the dictionary created just above:
                key_x = int(curve[0][i] - modulo_rest_x)

                modulo_rest_y = curve[1][i] % self.len_seq
                key_y = int(curve[1][i] - modulo_rest_y)

                key = str(key_x) + ' ' + str(key_y)
                key2 = str(key_x) + ' ' + str(key_y + self.len_seq)
                self.curves_binary[key] = True
                self.curves_binary[key2] = True
