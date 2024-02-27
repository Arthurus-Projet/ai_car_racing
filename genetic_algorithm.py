from neural_network import NeuralNetwork
from random import choice, randint
import numpy as np
import copy
from map import Map
from car import Car

class GeneticAlgorithm:

    def __init__(self, num_individuals, num_input_neurons, num_hidden_neurons, num_output_neurons, map_):
        """
        Initializes a Genetic Algorithm population for neuroevolution.

        Args:
            num_individuals (int): Number of individuals (neural networks) in the population.
            num_input_neurons (int): Number of input neurons in each neural network.
            num_hidden_neurons (int): Number of hidden neurons in each neural network.
            num_output_neurons (int): Number of output neurons in each neural network.
            map_ (Map): Instance of the map for car simulation.
        """
        self.individuals = [NeuralNetwork(num_input_neurons, num_hidden_neurons, num_output_neurons) for _ in range(num_individuals)]
        self.cars = [Car(map_) for _ in range(num_individuals)]
        self.fitness = [-1 for _ in range(num_individuals)]
        self.num_individuals = num_individuals

    def individual_action(self, i):
        """
        Determine the action for an individual car based on its neural network output.

        Args:
            i (int): Index of the individual car in the population.

        Returns:
            int: Action for the car :
                1 : left,
               -1 : right,
                0: straight ahead
        """
        action = self.individuals[i].forward_propagation([self.cars[i].line_length_1, self.cars[i].line_length_2, self.cars[i].line_length_3])
        if action[0] == 1 and action[1] == 0:
            return 1
        elif action[1] == 1 and action[0] == 0:
            return -1
        return 0

    def most_frequent_element(self, lst):
        '''
        Returns the most frequent element in a list

        Args:
            lst (list): List

        Returns:
            element (list): The most frequent element
        '''
        element = None
        max_occurrences = 0
        for x in lst:
            occurrences = lst.count(x)
            if occurrences > max_occurrences:
                element = x
                max_occurrences = occurrences
        return element

    def plot_best_individual(self, fitness):
        '''
        Display the neural network function graph of the best individual

        Args:
            fitness (list): List of fitness scores for each car
        '''
        individual_list = []
        for i in range(len(self.individuals)):
            for _ in range(fitness[i]):
                individual_list.append(copy.deepcopy(self.individuals[i]))

        best_individual = self.most_frequent_element(individual_list)
        best_individual.plot_neural_network_function()

    def reproduction(self):
        '''
        Each car has a probability of being selected for the next generation based on:
        Its score / Total score of all cars
        '''
        individual_list = []
        i_max_fitness = 0
        value_max_fitness = 0
        for i in range(len(self.individuals)):
            fitness = self.cars[i].fitness
            if fitness > value_max_fitness:
                value_max_fitness = fitness
                i_max_fitness = i
            for _ in range(fitness):
                individual_list.append(copy.deepcopy(self.individuals[i]))

        # The best individual is directly copied to the next generation
        self.individuals[0] = self.individuals[i_max_fitness]
        for i in range(1, self.num_individuals):
            self.individuals[i] = copy.deepcopy(self.individuals[i_max_fitness])  # Copy the best individual each time

    def mutation(self, prob, prob_0, prob_inverse, noise_value):
        """
        Each weight has a probability to mutate by adding a value between: lower_bound and upper_bound

        Args:
            prob (int): Probability that a weight mutates
            noise_value (float): Value defining the interval of noise added to a weight
        """
        lower_bound, upper_bound = -noise_value, noise_value

        for i in range(2, self.num_individuals, 2):
            for y in range(len(self.individuals[i].first_layer_weights)):
                for y2 in range(len(self.individuals[i].first_layer_weights[y])):
                    if randint(1, prob) == 1:
                        self.individuals[i].first_layer_weights[y][y2] += np.random.uniform(lower_bound, upper_bound)
                    elif randint(1, prob_0) == 1:
                        self.individuals[i].first_layer_weights[y][y2] = 0
                    elif randint(1, prob_inverse) == 1:
                        self.individuals[i].first_layer_weights[y][y2] = -self.individuals[i].first_layer_weights[y][y2]
                    if randint(1, prob) == 1:
                        self.individuals[i + 1].first_layer_weights[y][y2] += np.random.uniform(lower_bound, upper_bound)
                    elif randint(1, prob_0) == 1:
                        self.individuals[i + 1].first_layer_weights[y][y2] = 0
                    elif randint(1, prob_inverse) == 1:
                        self.individuals[i + 1].first_layer_weights[y][y2] = -self.individuals[i + 1].first_layer_weights[y][y2]
            for y in range(len(self.individuals[i].second_layer_weights)):
                for y2 in range(len(self.individuals[i].second_layer_weights[y])):
                    if randint(1, prob) == 1:
                        self.individuals[i].second_layer_weights[y][y2] += np.random.uniform(lower_bound, upper_bound)
                    elif randint(1, prob_0) == 1:
                        self.individuals[i].second_layer_weights[y][y2] = 0
                    elif randint(1, prob_inverse) == 1:
                        self.individuals[i].second_layer_weights[y][y2] = -self.individuals[i].second_layer_weights[y][y2]
                    if randint(1, prob) == 1:
                        self.individuals[i + 1].second_layer_weights[y][y2] += np.random.uniform(lower_bound, upper_bound)
                    elif randint(1, prob_0) == 1:
                        self.individuals[i + 1].second_layer_weights[y][y2] = 0
                    elif randint(1, prob_inverse) == 1:
                        self.individuals[i + 1].second_layer_weights[y][y2] = -self.individuals[i + 1].second_layer_weights[y][y2]
