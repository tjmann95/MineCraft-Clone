import sys
import numpy as np
import shader_loader
import random
import glfw
import TextureLoader

from OpenGL.GL import *
from pyrr import Matrix44
from pyrr import Vector3
from pyrr import matrix44
from pyrr import Quaternion
from math import radians
from Camera import Camera

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

block_positions = [
    [0, 0, 0],
    [1, 0, 0],
    [-1, 0, 0],
    [0, 0, 1],
    [1, 0, 1],
    [-1, 0, 1],
    [0, 0, -1],
    [1, 0, -1],
    [-1, 0, -1],
]

indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           8, 9, 10, 10, 11, 8,
           12, 13, 14, 14, 15, 12,
           16, 17, 18, 18, 19, 16,
           20, 21, 22, 22, 23, 20]

# for i in range(250):
#     x = random.randrange(-100, 100)
#     y = random.randrange(-100, 100)
#     z = random.randrange(-100, 100)
#     block_positions.append([x, y, z])

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.float32)

cam = Camera()
keys = [False] * 1024

window_width = 800
window_height = 800
aspect_ratio = window_width / window_height

last_mouse_x = window_width / 2
last_mouse_y = window_height / 2
first_mouse = True


def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            keys[key] = True
        elif action == glfw.RELEASE:
            keys[key] = False


def mouse_callback(window, mouse_x, mouse_y):
    global first_mouse, last_mouse_x, last_mouse_y

    if first_mouse:
        last_mouse_x = mouse_x
        last_mouse_y = mouse_y
        first_mouse = False

    x_offset = mouse_x - last_mouse_x
    y_offset = last_mouse_y - mouse_y
    last_mouse_x = mouse_x
    last_mouse_y = mouse_y

    cam.mouse_move(x_offset, y_offset)


def move():
    if keys[glfw.KEY_W]:
        cam.keyboard_presses("forward", .05)
    if keys[glfw.KEY_S]:
        cam.keyboard_presses("back", .05)
    if keys[glfw.KEY_A]:
        cam.keyboard_presses("left", .05)
    if keys[glfw.KEY_D]:
        cam.keyboard_presses("right", .05)
    if keys[glfw.KEY_SPACE]:
        cam.keyboard_presses("up", .05)
    if keys[glfw.KEY_LEFT_SHIFT]:
        cam.keyboard_presses("down", .05)


def resize_window(window, width, height):
    glViewport(0, 0, width, height)


def main():

    running = True

    if not glfw.init():
        return

    window = glfw.create_window(window_width, window_height, "Minecraft Clone", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, resize_window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # glViewport(0, 0, window_width, window_height)
    glEnable(GL_DEPTH_TEST)

    # Shader
    shader = shader_loader.Shader("vertex.vs", "fragment.fs")
    shader.use()

    # Vertex Buffering
    vao = GLuint(0)
    vbo = GLuint(0)
    ebo = GLuint(0)

    glGenVertexArrays(1, vao)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 4 * len(vertices), vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(indices), indices, GL_STATIC_DRAW)

    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Texture attribute
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(2)

    # Unbinding buffers
    glBindVertexArray(0)

    # Texturing
    wood = TextureLoader.load_texture("resources/wood.jpg")

    # MVP Location
    model_location = glGetUniformLocation(shader.shader_program, "model")
    view_location = glGetUniformLocation(shader.shader_program, "view")
    projection_location = glGetUniformLocation(shader.shader_program, "projection")

    # Model Matrix
    # model_orientation = Quaternion()
    # model_matrix_base = Matrix44.from_scale(Vector3([1., 1., 1.]))
    #
    # rotation = Quaternion.from_x_rotation(-radians(-55))
    # model_orientation = rotation * model_orientation
    #
    # model_matrix = model_matrix_base * model_orientation
    # model_matrix = np.array(model_matrix, dtype=np.float32)
    model_matrix = matrix44.create_from_translation(Vector3([-14.0, -8.0, 0.0]))

    # Projection Matrix
    # projection_matrix = Matrix44.perspective_projection(45.0, aspect_ratio, .1, 100.)
    # projection_matrix = np.array(projection_matrix, dtype=np.float32)
    projection_matrix = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    glUniformMatrix4fv(model_location, 1, GL_FALSE, model_matrix)
    glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection_matrix)

    glClearColor(0.4667, 0.7373, 1., 1.0)

    while running:
        glfw.poll_events()
        move()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBindVertexArray(vao)

        view_matrix = cam.get_view_matrix()
        glUniformMatrix4fv(view_location, 1, GL_FALSE, view_matrix)

        for each_block in range(0, len(block_positions)):
            translation = Vector3()
            translation += block_positions[each_block]
            translation = Matrix44.from_translation(translation)
            block_translation_matrix = Matrix44.from_scale(Vector3([1., 1., 1.])) * translation
            block_translation_matrix = np.array(block_translation_matrix, dtype=np.float32)
            glUniformMatrix4fv(model_location, 1, GL_FALSE, block_translation_matrix)

            glDrawArrays(GL_TRIANGLES, 0, 36)

        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteBuffers(1, ebo)

    glfw.terminate()
    sys.exit()

if __name__ == "__main__":
    main()
