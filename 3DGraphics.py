import pygame, sys
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

def cube():
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

def jump():
    height = 0
    for i in range(1, FPS):
        height -= .1
        glTranslatef(0, height, 0)
        pygame.time.wait(200)

def main():
    pygame.init()
    window = (800, 600)
    pygame.display.set_mode(window, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Testing")

    gluPerspective(45, window[0] / window[1], .1, 50.0)
    glTranslatef(0.0, 0.0, -7)

    move_x = 0
    move_z = 0

    move_amt = .1

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
                elif event.key == K_SPACE:
                    jump()
                elif event.key == K_UP:
                    glTranslatef(0, -.5, 0)
            elif event.type == KEYUP:
                if event.key == K_a or K_d or K_w or K_s:
                    move_x = 0
                    move_z = 0






        glTranslatef(move_x, 0, move_z)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cube()
        pygame.display.flip()
        fps_clock.tick(FPS)

main()