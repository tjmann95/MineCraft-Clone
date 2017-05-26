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
from pyrr import vector
from pyrr import vector3
from math import radians, sin, cos
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
    [0., 0., 0.],
    [2., 5., -15.],
    [-1.5, -2.2, -2.5],
    [-3.8, -2., -12.3],
    [2.4, -.4, -3.5],
    [-1.7, 3., -7.5],
    [1.3, -2., -2.5],
    [1.5, 2., -2.5],
    [1.5, .2, -1.5],
    [-1.3, 1., -1.5]
]

vertices = np.array(vertices, dtype=np.float32)


# def lookAt(position, target, up=Vector3([0., 1., 0.])):
#     direction = vector.normalise(position - target)
#     direction = np.array(direction, dtype=np.float32)
#     up = np.array(up, dtype=np.float32)
#     camera_right = vector.normalise(vector3.cross(up, direction))
#     camera_up = vector.normalise(vector3.cross(direction, camera_right))
#
#     translation = Matrix44.identity()
#     translation[3][0] = -position[0]
#     translation[3][1] = -position[1]
#     translation[3][2] = -position[2]
#
#     rotation = Matrix44.identity()
#     rotation[0][0] = camera_right[0]
#     rotation[1][0] = camera_right[1]
#     rotation[2][0] = camera_right[2]
#     rotation[0][1] = camera_up[0]
#     rotation[1][1] = camera_up[1]
#     rotation[2][1] = camera_up[2]
#     rotation[0][2] = direction[0]
#     rotation[1][2] = direction[1]
#     rotation[2][2] = direction[2]
#
#     return np.array(translation * rotation, dtype=np.float32)


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

    camera = Camera(window_width, window_height, view_location)

    # Camera
    # camera_position = Vector3([0., 0., 6.])
    # camera_front = Vector3([0., 0., -1.])
    #
    # last_frame = 0.0
    # mouse_sensitivity = .5
    # pitch = 0
    # yaw = 0

    while running:
        # current_frame = pygame.time.get_ticks()
        # delta_time = current_frame - last_frame
        # last_frame = current_frame
        # last_cam_y = camera_position[1]
        #
        # camera_speed = .01 * delta_time

        keys_pressed = pygame.key.get_pressed()

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

        camera.point_camera()

        # Keyboard
        # if keys_pressed[K_SPACE]:
        #     camera_position[1] += camera_speed
        #     last_cam_y = camera_position[1]
        # if keys_pressed[K_LSHIFT]:
        #     camera_position[1] -= camera_speed
        #     last_cam_y = camera_position[1]
        # if keys_pressed[K_w]:
        #     camera_position += camera_speed * camera_front
        # if keys_pressed[K_s]:
        #     camera_position -= camera_speed * camera_front
        # if keys_pressed[K_a]:
        #     camera_position -= vector.normalise(vector3.cross(np.array(camera_front, dtype=np.float32), np.array([0., 1., 0.], dtype=np.float32))) * camera_speed
        # if keys_pressed[K_d]:
        #     camera_position += vector.normalise(vector3.cross(np.array(camera_front, dtype=np.float32), np.array([0., 1., 0.], dtype=np.float32))) * camera_speed
        # camera_position[1] = last_cam_y

        # Mouse
        # mouse = pygame.mouse.get_rel()
        # x_offset = mouse[0]
        # y_offset = mouse[1]
        #
        # x_offset *= mouse_sensitivity
        # y_offset *= mouse_sensitivity

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # yaw += x_offset * mouse_sensitivity
        # pitch += -y_offset * mouse_sensitivity
        #
        # if pitch > 89.0:
        #     pitch = 89.0
        # if pitch < -89.0:
        #     pitch = -89.0
        #
        # direction_x = cos(radians(pitch)) * cos(radians(yaw))
        # direction_y = sin(radians(pitch))
        # direction_z = cos(radians(pitch)) * sin(radians(yaw))
        # camera_front = vector.normalise(np.array([direction_x, direction_y, direction_z], dtype=np.float32))
        # camera_front = Vector3(camera_front)

        glClearColor(0.4667, 0.7373, 1., 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Texturing
        glBindTexture(GL_TEXTURE_2D, wood_texture)
        glUniform1i(glGetUniformLocation(shader.shader_program, "woodTexture"), 0)

        glBindVertexArray(vao)

        glUniformMatrix4fv(transform_location, 1, GL_FALSE, np.array(Matrix44.identity(), dtype=np.float32))

        # Camera
        # view_matrix = lookAt(camera_position, camera_position + camera_front)

        # MVP
        glUniformMatrix4fv(model_location, 1, GL_FALSE, model_matrix)
        # glUniformMatrix4fv(view_location, 1, GL_FALSE, view_matrix)
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection_matrix)

        for each_block in range(0, len(block_positions)):
            translation = Vector3()
            translation += block_positions[each_block]
            translation = Matrix44.from_translation(translation)
            block_translation_matrix = Matrix44.from_scale(Vector3([1., 1., 1.])) * translation
            block_translation_matrix = np.array(block_translation_matrix, dtype=np.float32)
            glUniformMatrix4fv(model_location, 1, GL_FALSE, block_translation_matrix)

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
