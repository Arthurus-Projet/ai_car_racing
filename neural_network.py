import numpy as np
import matplotlib.pyplot as plt
import pygame

class NeuralNetwork:

    def __init__(self, input_neurons, hidden_neurons, output_neurons):
        # Initializing weights for the first and second layers
        self.first_layer_weights = np.array([[np.random.uniform(-0.1, 0.1) for _ in range(hidden_neurons)] for _ in range(input_neurons + 1)])
        self.second_layer_weights = np.array([[np.random.uniform(-0.1, 0.1)  for _ in range(output_neurons)] for _ in range(hidden_neurons + 1)])
        self.hidden_neurons = hidden_neurons
        self.first_layer_values = None
        self.second_layer_values = None

    def print_weights(self):
        # Display the weights of the first layer
        print("First layer weights:")
        print(self.first_layer_weights)

    def print_second_layer_weights(self):
        # Display the weights of the second layer
        print("Second layer weights:")
        print(self.second_layer_weights)

    def print_first_layer_values(self):
        # Display the output values of the first layer
        print(self.first_layer_values)

    def print_second_layer_values(self):
        # Display the output values of the second layer
        print(self.second_layer_values)

    def relu(self, x):
        # ReLU activation function
        return max(0, x)

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))

    def threshold(self, x):
        # Threshold activation function
        if x > 0:
            return 1
        return 0

    def calculate_first_layer_values(self, input_values):
        '''
        Matrix multiplication of input values by the weights of the first layer

        Args:
            input_values (list): List of input values
        '''
        input_values.append(1)  # Adding 1 for the bias
        self.first_layer_values = [self.relu(elem) for elem in np.dot(input_values, self.first_layer_weights)]
        self.first_layer_values.append(1)  # Bias for the output results of the output layer
        return self.first_layer_values

    def calculate_second_layer_values(self):
        # Matrix multiplication of hidden layer values by the weights of the second layer
        self.second_layer_values = [self.threshold(elem) for elem in np.dot(self.first_layer_values, self.second_layer_weights)]
        return self.second_layer_values

    def forward_propagation(self, input_values):
        '''
        Take input values and return a binary output, 1 for a jump or 0 for no jump

        Args:
            input_values (list): List of input values
        '''
        self.calculate_first_layer_values(input_values)
        return self.calculate_second_layer_values()

    def plot_neural_network_function(self):
        # Display the neural network function graph
        n = 500
        n2 = 200
        horizontal_distance = np.linspace(0, n, n + 1)
        vertical_distance = np.linspace(-n2, n2 * 4, (n2*5) + 1)

        Y = []
        print("< Graph being processed... >")
        for x in range(len(horizontal_distance)):
            l = []
            for y in range(len(vertical_distance)):
                l.append(self.forward_propagation([horizontal_distance[x], vertical_distance[y]]))
            Y.append(l)

        x_red, y_red, x_blue, y_blue = [], [], [], []

        for i in range(len(horizontal_distance)):
            for i2 in range(len(vertical_distance)):
                if Y[i][i2] == [1]:
                    x_red.append(-horizontal_distance[i])
                    y_red.append(-vertical_distance[i2])
                else:
                    x_blue.append(-horizontal_distance[i])
                    y_blue.append(-vertical_distance[i2])

        plt.scatter(x_red, y_red, marker="s", color='red')
        plt.scatter(x_blue, y_blue, color='blue')
        plt.show()

    def plot_neural_network_graph(self, screen, position, input_values):
        '''
        Visualization of the neural network

        Args:
            screen (pygame.display.set_mode): Graphic window for game display
            input_values (list): List of input values
        '''
        radius = 10
        width = 3
        distance_between_two_layers = 70

        hidden_layer_values = self.calculate_first_layer_values(input_values)[0:self.hidden_neurons]  # Remove the bias which is 1
        output_layer_values = self.calculate_second_layer_values()

        color_hidden_layer_values = []

        for i in range(len(hidden_layer_values)):
            if hidden_layer_values[i] > 1:
                color_hidden_layer_values.append((255, 255, 0))  # Yellow color
            else:
                color_hidden_layer_values.append((255, 255, 255 - int(hidden_layer_values[i]*255)))

        color_output_layer_values = (255, 255, 255 - int(output_layer_values[0]*255))  # Yellow if the bird jumps (255, 255, 0), white if it doesn't jump (255, 255, 255)

        if output_layer_values[0] == 1:
            color_output_layer_values = (255, 160, 122)
        else:
            color_output_layer_values = (255, 255, 255)

        if output_layer_values[1] == 1:
            color_output_layer_values_2 = (255, 160, 122)
        else:
            color_output_layer_values_2 = (255, 255, 255)

        # Connection for the first input
        pos = [-52.5, -17.5, 17.5, 52.5, 87.5, 122.5]
        for p in pos:
            pygame.draw.line(screen, (255, 255, 255), (position[0], position[1]), (position[0] + distance_between_two_layers, position[1] + p), width)

        # Connection for the second input
        for p in pos:
            pygame.draw.line(screen, (255, 255, 255), (position[0], position[1] + 35), (position[0] + distance_between_two_layers, position[1] + p), width)

        # Connection to the third input
        for p in pos:
            pygame.draw.line(screen, (255, 255, 255), (position[0], position[1] + 70), (position[0] + distance_between_two_layers, position[1] + p), width)

        # Connection to the output neuron
        for p in pos:
            pygame.draw.line(screen, (255, 255, 255), (position[0] + distance_between_two_layers, position[1] + p), (position[0] + distance_between_two_layers * 2, position[1] + 17.5 + 35), width)
            pygame.draw.line(screen, (255, 255, 255), (position[0] + distance_between_two_layers, position[1] + p), (position[0] + distance_between_two_layers * 2, position[1] + 17.5), width)

        # The 3 input neurons
        pygame.draw.circle(screen, (255, 255, 255), (position[0], position[1]), radius)
        pygame.draw.circle(screen, (255, 255, 255), (position[0], position[1] + 35), radius)
        pygame.draw.circle(screen, (255, 255, 255), (position[0], position[1]+ 70), radius)

        # Hidden neurons
        for i in range(len(pos)):
            pygame.draw.circle(screen, color_hidden_layer_values[i], (position[0] + distance_between_two_layers, position[1] + pos[i]), radius)

        # Output neuron
        pygame.draw.circle(screen, color_output_layer_values, (position[0] + distance_between_two_layers * 2, position[1] + 17.5), radius)
        pygame.draw.circle(screen, color_output_layer_values_2, (position[0] + distance_between_two_layers * 2, position[1] + 52.5), radius)
