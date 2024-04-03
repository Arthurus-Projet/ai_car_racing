To create the circuit editor, I used Béziers curves, with 4 points to create a curve.

This python project simulates cars that have access to 3 distances: straight ahead, to the right and to the left : 

![image](https://github.com/Arthurus-Projet/ai_car_racing/assets/133526137/f408a68d-78fb-44e1-91f4-1aae8f6c9b2c)

Then we give these 3 inputs to a neural network, and at the output there are 2 binary output neurons:
1 0 : The car goes to the right
0 1 : Car goes left
00 or 11 : the car goes straight on

Then I use a genetic algorithm to optimize the weights of the neural network

In the simplest circuit, cars just have to turn left and go straight ahead :

![image](https://github.com/Arthurus-Projet/ai_car_racing/assets/133526137/ee3692d7-00de-4182-bf5b-e6dfc065782b)

100 cars are created per generation, as soon as a car touches the circuit it dies, the fitness score is defined by the time a car remains alive.

Here's a more challenging circuit :

![image](https://github.com/Arthurus-Projet/ai_car_racing/assets/133526137/f2a38939-7140-43b1-9002-aef48ce43b9c)

generation 34 a car that survives indefinitely :

![image](https://github.com/Arthurus-Projet/ai_car_racing/assets/133526137/400ba9ca-ccf3-44a4-9e5a-a178dff837e2)

