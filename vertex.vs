#version 330
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
layout (location = 2) in vec2 texCoords;

out vec3 ourColor;
out vec2 texCoordsOut;

uniform mat4 transform;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * transform * vec4(position, 1.0f);
    ourColor = color;
    texCoordsOut = vec2(texCoords);
}
