import pygame
import sys
import numpy as np
import shader_loader

from pygame.locals import *
from OpenGL.GL import *
from PIL import Image
from pyrr import Matrix44
from pyrr import Vector3
from pyrr import Quaternion
from math import radians
from Camera import Camera
from TerrainGen import HillGrid

vertices = (
    -0.5,   -0.5,   -0.5, 0.0, 0.0,
     0.5,   -0.5,   -0.5, 1.0, 0.0,
     0.5,    0.5,   -0.5, 1.0, 1.0,
     0.5,    0.5,   -0.5, 1.0, 1.0,
    -0.5,    0.5,   -0.5, 0.0, 1.0,
    -0.5,   -0.5,   -0.5, 0.0, 0.0,

    -0.5,   -0.5,    0.5, 0.0, 0.0,
     0.5,   -0.5,    0.5, 1.0, 0.0,
     0.5,    0.5,    0.5, 1.0, 1.0,
     0.5,    0.5,    0.5, 1.0, 1.0,
    -0.5,    0.5,    0.5, 0.0, 1.0,
    -0.5,   -0.5,    0.5, 0.0, 0.0,

    -0.5,    0.5,    0.5, 1.0, 0.0,
    -0.5,    0.5,   -0.5, 1.0, 1.0,
    -0.5,   -0.5,   -0.5, 0.0, 1.0,
    -0.5,   -0.5,   -0.5, 0.0, 1.0,
    -0.5,   -0.5,    0.5, 0.0, 0.0,
    -0.5,    0.5,    0.5, 1.0, 0.0,

     0.5,    0.5,    0.5, 1.0, 0.0,
     0.5,    0.5,   -0.5, 1.0, 1.0,
     0.5,   -0.5,   -0.5, 0.0, 1.0,
     0.5,   -0.5,   -0.5, 0.0, 1.0,
     0.5,   -0.5,    0.5, 0.0, 0.0,
     0.5,    0.5,    0.5, 1.0, 0.0,

    -0.5,   -0.5,   -0.5, 0.0, 1.0,
     0.5,   -0.5,   -0.5, 1.0, 1.0,
     0.5,   -0.5,    0.5, 1.0, 0.0,
     0.5,   -0.5,    0.5, 1.0, 0.0,
    -0.5,   -0.5,    0.5, 0.0, 0.0,
    -0.5,   -0.5,   -0.5, 0.0, 1.0,

    -0.5,    0.5,   -0.5, 0.0, 1.0,
     0.5,    0.5,   -0.5, 1.0, 1.0,
     0.5,    0.5,    0.5, 1.0, 0.0,
     0.5,    0.5,    0.5, 1.0, 0.0,
    -0.5,    0.5,    0.5, 0.0, 0.0,
    -0.5,    0.5,   -0.5, 0.0, 1.0
)

# indicies = [0,  1,  2,  2,  3,  0,
#             4,  5,  6,  6,  7,  4,
#             8,  9, 10, 10, 11,  8,
#             12, 13, 14, 14, 15, 12,
#             16, 17, 18, 18, 19, 16,
#             20, 21, 22, 22, 23, 20
#             ]

size = 40
terrain = HillGrid(ITER=50, SIZE=size).__getitem__()
flat_terrain = [x for sublist in terrain for x in sublist]
block_positions = []

for y in range(0, size):
    for x in range(0, size):
        block_positions.append([x, y, terrain[y][x]])

vertices = np.array(vertices, dtype=np.float32)


def main():
    pygame.init()

    window_width = 1920
    window_height = 1080
    aspect_ratio = window_width/window_height
    fps = 60
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_mode([window_width, window_height], DOUBLEBUF | OPENGL | FULLSCREEN)
    pygame.display.set_caption("Minecraft Clone")
    window_width, window_height = pygame.display.get_surface().get_size()
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    glViewport(0, 0, window_width, window_height)
    glEnable(GL_DEPTH_TEST)

    # Shader
    shader = shader_loader.Shader("vertex.vs", "fragment.fs")
    shader.use()

    # Vertex Buffering
    vao = GLuint(0)
    vbo = GLuint(0)
    ebo = GLuint(0)

    glGenVertexArrays(1, vao)
    glGenBuffers(1, vbo)
    glGenBuffers(1, ebo)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 4 * len(vertices), vertices, GL_STATIC_DRAW)

    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(indices), indices, GL_STATIC_DRAW)

    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Texture attribute
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(2)

    # Unbinding buffers
    glBindVertexArray(0)

    # Instances
    instance_array = np.array(block_positions, np.float32)

    instance_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, instance_vbo)
    glBufferData(GL_ARRAY_BUFFER, instance_array.itemsize * len(instance_array), instance_array, GL_STATIC_DRAW)

    glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribDivisor(1, 1)

    # Texturing
    wood = Image.open("resources/wood.jpg")
    wood.load()

    wood_data = list(wood.getdata())
    wood_data = np.array(wood_data, dtype=np.uint8)

    wood_texture = glGenTextures(1)

    # Wood texture
    glBindTexture(GL_TEXTURE_2D, wood_texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGB,
                 wood.size[0], wood.size[1],
                 0,
                 GL_RGB,
                 GL_UNSIGNED_BYTE,
                 wood_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

    transform_location = glGetUniformLocation(shader.shader_program, "transform")
    model_location = glGetUniformLocation(shader.shader_program, "model")
    view_location = glGetUniformLocation(shader.shader_program, "view")
    projection_location = glGetUniformLocation(shader.shader_program, "projection")

    # Model Matrix
    model_orientation = Quaternion()
    model_matrix_base = Matrix44.from_scale(Vector3([1., 1., 1.]))

    rotation = Quaternion.from_x_rotation(-radians(-55))
    model_orientation = rotation * model_orientation

    model_matrix = model_matrix_base * model_orientation
    model_matrix = np.array(model_matrix, dtype=np.float32)

    # Projection Matrix
    projection_matrix = Matrix44.perspective_projection(45.0, aspect_ratio, .1, 100.)
    projection_matrix = np.array(projection_matrix, dtype=np.float32)

    # Camera
    camera = Camera(window_width, window_height, view_location)

    while running:

        keys_pressed = pygame.key.get_pressed()

        # Keyboard
        if keys_pressed[K_SPACE]:
            camera.move_camera("UP")
        if keys_pressed[K_LSHIFT]:
            camera.move_camera("DOWN")
        if keys_pressed[K_w]:
            camera.move_camera("FORWARD")
        if keys_pressed[K_s]:
            camera.move_camera("BACK")
        if keys_pressed[K_a]:
            camera.move_camera("LEFT")
        if keys_pressed[K_d]:
            camera.move_camera("RIGHT")

        # Mouse
        camera.point_camera()

        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        glClearColor(0.4667, 0.7373, 1., 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Texturing
        glBindTexture(GL_TEXTURE_2D, wood_texture)
        glUniform1i(glGetUniformLocation(shader.shader_program, "woodTexture"), 0)

        glBindVertexArray(vao)

        glUniformMatrix4fv(transform_location, 1, GL_FALSE, np.array(Matrix44.identity(), dtype=np.float32))

        # MP
        glUniformMatrix4fv(model_location, 1, GL_FALSE, model_matrix)
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection_matrix)

        for each_block in range(0, len(block_positions)):
            translation = Vector3()
            translation += block_positions[each_block]
            translation = Matrix44.from_translation(translation)
            block_translation_matrix = Matrix44.from_scale(Vector3([1., 1., 1.])) * translation
            block_translation_matrix = np.array(block_translation_matrix, dtype=np.float32)
            glUniformMatrix4fv(model_location, 1, GL_FALSE, block_translation_matrix)

            glDrawArraysInstanced(GL_TRIANGLES, 0, 36, len(block_positions))

        glBindVertexArray(0)

        pygame.display.flip()
        clock.tick(fps)

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteBuffers(1, ebo)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
