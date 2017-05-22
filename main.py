import pygame
import sys
import numpy
import shader_loader

from pygame.locals import *
from OpenGL.GL import *
from PIL import Image

# vertices = (
#     #right
#     (.5, .5, .5,
#      .5, .5, -.5,
#      .5, -.5, .5,
#      .5, -.5, -.5),
#     #left
#     (-.5, .5, .5,
#      -.5, .5, -.5,
#      -.5, -.5, .5,
#      -.5, -.5, -.5),
#     #front
#     (.5, .5, .5,
#      -.5, .5, .5,
#      -.5, -.5, .5,
#      .5, -.5, .5),
#     #back
#     (.5, .5, -.5,
#      -.5, .5, -.5,
#      -.5, -.5, -.5,
#      .5, -.5, -.5),
#     #top
#     (.5, .5, .5,
#      -.5, .5, .5,
#      -.5, .5, -.5,
#      .5, .5, -.5),
#     #bottom
#     (.5, -.5, .5,
#      -.5, -.5, .5,
#      -.5, -.5, -.5,
#      .5, -.5, -.5)
# )

vertices = (
    # Vertex       Color          Texture Coords
    .5, .5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,  # top right
    .5, -.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,  # bottom right
    -.5, -.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # bottom left
    -.5, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,  # top left
)

indices = (
    0, 1, 3,  # top right triangle
    1, 2, 3  # bottom left triangle
)

vertices = numpy.array(vertices, dtype=numpy.float32)
indices = numpy.array(indices, dtype=numpy.uint32)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()

    window_width = 800
    window_height = 800
    aspect_ratio = window_width/window_height
    fps = 60
    clock = pygame.time.Clock()

    pygame.display.set_mode([window_width, window_height], DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Minecraft Clone")
    glViewport(0, 0, window_width, window_height)

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

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(indices), indices, GL_STATIC_DRAW)

    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)

    # Texture attribute
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
    glEnableVertexAttribArray(2)

    # Unbinding buffers
    glBindVertexArray(0)

    # Texturing
    wood = Image.open("resources/wood.jpg")
    wood.load()
    face = Image.open("resources/awesomeface.jpg")
    face.load()

    wood_data = list(wood.getdata())
    wood_data = numpy.array(wood_data, dtype=numpy.uint8)
    face_data = list(wood.getdata())
    face_data = numpy.array(face_data, dtype=numpy.uint8)

    # Wood texture
    texture1 = GLuint(0)
    glGenTextures(1, texture1)
    glBindTexture(GL_TEXTURE_2D, texture1)

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
    texture2 = GLuint(0)
    glGenTextures(1, texture2)
    glBindTexture(GL_TEXTURE_2D, texture2)

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

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        glClearColor(0.4667, 0.7373, 1., 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        shader.use()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture2)
        glUniform1i(glGetUniformLocation(shader.compile_shader("vertex.vs", "fragment.fs"), "faceTexture"), 0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, texture1)
        glUniform1i(glGetUniformLocation(shader.compile_shader("vertex.vs", "fragment.fs"), "woodTexture"), 1)

        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()