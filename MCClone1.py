import pygame, sys
from pygame.locals import *

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

FPS = 60
fps_clock = pygame.time.Clock()

BLACK = (1, 1, 1)
WHITE = (0, 0, 0)

vertices = (
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1)
)

edges = (
    (0, 1),
    (1, 6),
    (6, 5),
    (5, 0),
    (0, 3),
    (1, 2),
    (6, 7),
    (5, 4),
    (3, 2),
    (2, 7),
    (7, 4),
    (4, 3)
)

surfaces = (
    (0, 1, 2, 3),
    (1, 2, 6, 7),
    (5, 6, 7, 4),
    (0, 3, 4, 5),
    (0, 1, 6, 5),
    (2, 3, 4, 7)
)

def draw_block():
    glBegin(GL_LINES)
    glColor(WHITE)
    for each_edge in edges:
        for each_vertex in each_edge:
            glVertex3fv(vertices[each_vertex])

def terminate():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    window = (800, 600)
    pygame.display.set_mode(window, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("MC Clone")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_block()

        pygame.display.flip()
        fps_clock.tick(FPS)

if __name__ == "__main__":
    main()
