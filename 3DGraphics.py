import pygame, sys, random
from pygame.locals import *

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

FPS = 60
fps_clock = pygame.time.Clock()

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (1, 0, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (1, 0, 1)
)
def set_vertices(max_distance, min_distance = -20):
    x_value_change = random.randrange(-10, 10)
    y_value_change = random.randrange(-10, 10)
    z_value_change = random.randrange(-1*max_distance, min_distance)

    new_vertices = []

    for vert in vertices:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices

def cube(vertices):
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3fv((0, 0, 0))
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    window = (800, 600)
    pygame.display.set_mode(window, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Testing")

    max_distance = 100

    gluPerspective(45, window[0] / window[1], .1, max_distance)
    glTranslatef(0.0, 0.0, -7)

    move_x = 0
    move_z = 0

    move_amt = .2

    cube_dict = {}

    for x in range(20):
        cube_dict[x] = set_vertices(max_distance)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_a and not event.key == K_d:
                    move_x = move_amt
                elif event.key == K_d and not event.key == K_a:
                    move_x = -move_amt
                elif event.key == K_w and not event.key == K_s:
                    move_z = move_amt
                elif event.key == K_s and not event.key == K_w:
                    move_z = -move_amt
                # elif event.key == K_SPACE:
                #     jump()
            elif event.type == KEYUP:
                if event.key == K_a or K_d:
                    move_x = 0
                if event.key == K_w or K_s:
                    move_z = 0

        x = glGetDoublev(GL_MODELVIEW_MATRIX)

        player_cam_x = x[3][0]
        player_cam_y = x[3][1]
        player_cam_z = x[3][2]

        glTranslatef(move_x, 0, move_z)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for each_cube in cube_dict:
            cube(cube_dict[each_cube])

        for each_cube in cube_dict:
            if player_cam_z <= cube_dict[each_cube][0][2]:
                print("passed a cube")
                new_max = int(-(player_cam_z - max_distance))
                cube_dict[each_cube] = set_vertices(new_max, int(player_cam_z))

        pygame.display.flip()
        fps_clock.tick(FPS)

if __name__ == "__main__":
    main()