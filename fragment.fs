#version 330
in vec3 ourColor;
in vec2 TexCoord;

out vec4 color;

uniform sampler2D woodTexture;
uniform sampler2D faceTexture;

void main()
{
    color = mix(texture(woodTexture, TexCoord), texture(faceTexture, TexCoord), 0.2);
}