#version 330
in vec3 ourColor;
in vec2 texCoordsOut;

out vec4 color;

uniform sampler2D woodTexture;
uniform sampler2D faceTexture;

void main()
{
    color = mix(texture(woodTexture, texCoordsOut), texture(faceTexture, texCoordsOut), 0.2);
}
