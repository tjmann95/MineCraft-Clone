import pygame, sys
from pygame.locals import *

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

FPS = 60
fps_clock = pygame.time.Clock()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

vertices = [
    [1, 1, 1],
    [-1, 1, 1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1]
]

edges = [
    [0, 1],
    [1, 6],
    [6, 5],
    [5, 0],
    [0, 3],
    [1, 2],
    [6, 7],
    [5, 4],
    [3, 2],
    [2, 7],
    [7, 4],
    [4, 3]
]

def draw_cube(x, y, z):
    new_vertices = []

    for each_vertex in vertices:
        new_vertices.append([each_vertex[0] + x*2, each_vertex[1] + y*2, each_vertex[2] + z*2])

    glBegin(GL_LINES)
    for each_edge in edges:
        for each_vertex in each_edge:
            glVertex3fv(new_vertices[each_vertex])
    glEnd()

def main():
    global WINDOW_WIDTH, WINDOW_HEIGHT

    pygame.init()
    window = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(window, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("MC Clone")

    gluPerspective(45, window[0] / window[1], .1, 100.0)
    glTranslatef(0, 0, -10)

    move_speed = .5
    move_x = 0
    move_z = 0

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    move_z = move_speed
                if event.key == K_a:
                    move_x = move_speed
                if event.key == K_s:
                    move_z = -move_speed
                if event.key == K_d:
                    move_x = -move_speed

            elif event.type == KEYUP:
                if event.key == K_w or event.key == K_s:
                    move_z = 0
                if event.key == K_a or event.key == K_d:
                    move_x = 0

        glTranslate(move_x, 0, move_z)

        x = glGetDoublev(GL_MODELVIEW_MATRIX)

        player_cam_x = x[3][0]
        player_cam_y = x[3][1]
        player_cam_z = x[3][2]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for x in range(-1, 2):
            for y in range(-1, 2):
                draw_cube(x, y, 0)

        pygame.display.flip()
        fps_clock.tick(FPS)



def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()