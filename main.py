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

block_positions = (
    Vector3([0., 0., 0.]),
    Vector3([2., 5., -15.]),
    Vector3([-1.5, -2.2, -2.5]),
    Vector3([-3.8, -2., -12.3]),
    Vector3([2.4, -.4, -3.5]),
    Vector3([-1.7, 3., -7.5]),
    Vector3([1.3, -2., -2.5]),
    Vector3([1.5, 2., -2.5]),
    Vector3([1.5, .2, -1.5]),
    Vector3([-1.3, 1., -1.5])
)

# vertices = (
#     # Vertex       Color          Texture Coords
#     .5, .5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,  # top right
#     .5, -.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,  # bottom right
#     -.5, -.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # bottom left
#     -.5, .5, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0,  # top left
# )
#
# indices = (
#     0, 1, 3,  # top right triangle
#     1, 2, 3  # bottom left triangle
# )

vertices = np.array(vertices, dtype=np.float32)
# indices = np.array(indices, dtype=np.uint32)


def main():
    pygame.init()

    window_width = 800
    window_height = 800
    aspect_ratio = window_width/window_height
    fps = 60
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_mode([window_width, window_height], DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Minecraft Clone")
    glViewport(0, 0, window_width, window_height)
    glEnable(GL_DEPTH_TEST)

    # Shader
    shader = shader_loader.Shader("vertex.vs", "fragment.fs")

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

    # Color attribute
    # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
    # glEnableVertexAttribArray(1)

    # Texture attribute
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(2)

    # Unbinding buffers
    glBindVertexArray(0)

    # Texturing
    wood = Image.open("resources/wood.jpg")
    wood.load()
    face = Image.open("resources/awesomeface.jpg")
    face.load()

    shader.use()

    wood_data = list(wood.getdata())
    wood_data = np.array(wood_data, dtype=np.uint8)
    face_data = list(face.transpose(Image.FLIP_TOP_BOTTOM).getdata())
    face_data = np.array(face_data, dtype=np.uint8)

    wood_texture, face_texture = glGenTextures(2)

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

    # Face texture
    glBindTexture(GL_TEXTURE_2D, face_texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGB,
                 face.size[0], face.size[1],
                 0,
                 GL_RGB,
                 GL_UNSIGNED_BYTE,
                 face_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

    # Building transformation matrix
    scale = Vector3([1., 1., 1.])
    translation1 = Vector3()
    orientation_base = Quaternion()
    matrix_base = Matrix44.from_scale(scale)

    translation1 += [0.0, 0.0, 0.0]
    translation1 = Matrix44.from_translation(translation1)

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

    # View Matrix
    view_translation = Vector3()
    view_matrix_base = Matrix44.from_scale(Vector3([1., 1., 1.]))

    view_translation += [0., 0., -3.0]
    view_translation = Matrix44.from_translation(view_translation)

    view_matrix = view_matrix_base * view_translation
    view_matrix = np.array(view_matrix, dtype=np.float32)

    # Projection Matrix
    projection_matrix = Matrix44.perspective_projection(45.0, aspect_ratio, .1, 100.)
    projection_matrix = np.array(projection_matrix, dtype=np.float32)

    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        glClearColor(0.4667, 0.7373, 1., 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Texture units
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, wood_texture)
        glUniform1i(glGetUniformLocation(shader.shader_program, "woodTexture"), 0)
        # glActiveTexture(GL_TEXTURE1)
        # glBindTexture(GL_TEXTURE_2D, face_texture)
        # glUniform1i(glGetUniformLocation(shader.shader_program, "faceTexture"), 1)

        glBindVertexArray(vao)

        # Transformations and drawing
        rotation_x = Quaternion.from_x_rotation(.001 * pygame.time.get_ticks())
        rotation_y = Quaternion.from_y_rotation(.001 * pygame.time.get_ticks())
        rotation = rotation_x * rotation_y
        orientation = rotation * orientation_base

        matrix = matrix_base * orientation
        matrix = matrix * translation1
        matrix = np.array(matrix, dtype=np.float32)

        glUniformMatrix4fv(transform_location, 1, GL_FALSE, matrix)

        # MVP
        glUniformMatrix4fv(model_location, 1, GL_FALSE, model_matrix)
        glUniformMatrix4fv(view_location, 1, GL_FALSE, view_matrix)
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection_matrix)

        glDrawArrays(GL_TRIANGLES, 0, 36)

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
