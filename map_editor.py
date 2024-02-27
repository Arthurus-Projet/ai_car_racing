import pygame
from map import Map
from manager_save_load import save_class
import configs
import numpy as np
from time import sleep

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
name_new_map = "new_map"
map = Map()

selected_point = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, point in enumerate(map.liste_points[map.current_index]):
                distance = np.linalg.norm(np.array(point) - mouse_pos)
                if distance < 10:  # Suitable distance for selection
                    selected_point = i

    # Use the arrows or ZQSD keys to move the selected point.
    keys = pygame.key.get_pressed()
    if map.liste_points[map.current_index] is not None:
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            map.liste_points[map.current_index][selected_point][1] -= 10
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            map.liste_points[map.current_index][selected_point][1] += 10
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            map.liste_points[map.current_index][selected_point][0] -= 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            map.liste_points[map.current_index][selected_point][0] += 10
        # Add a new curve
        if keys[pygame.K_n]:
            map.create_new_curve()
            sleep(0.3)
        # End of loop
        if keys[pygame.K_e]:
            map.end_of_loop()
            sleep(0.3)
        # End of circuit creation
        if keys[pygame.K_r]:
            map.end_of_second_loop()
            save_class(name_new_map, map)
            running = False
            sleep(0.3)

    screen.fill(configs.BLUE)

    # update the curve of the current index
    map.curve(map.current_index)

    # Displays all curves
    for curve in map.curves:
        pygame.draw.lines(screen, configs.LIGHT_BLUE, False, curve.T, 5)

    # Displays points
    for point in map.liste_points[map.current_index]:
        pygame.draw.circle(screen, configs.RED, point, 4)

    # Marking control points
    for i, point in enumerate(map.liste_points[map.current_index]):
        color = configs.RED if i == selected_point else configs.WHITE
        pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), 5)

    pygame.display.flip()
    clock.tick(30)
