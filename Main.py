from OpenGL.raw.GL.VERSION.GL_1_0 import GL_GREEN
import pygame
from pygame.locals import *
import glm
from GraphLib import Renderer, Model
import shaders

width = 1600
height = 900
deltaTime = 0.0
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.OPENGL )
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(shaders.vertex_shader, shaders.fragment_shader)
uniqueModel = Model('src/Objects/katana.obj', 'src/Textures/brighter.png')
uniqueModel.position.z = -7
uniqueModel.position.x = -5
uniqueModel.rotation.x = -90
# uniqueModel.position.y = -6
uniqueModel.scale = glm.vec3(0.2, 0.2, 0.2)
rend.scene.append( uniqueModel )
pygame.mixer.music.load('src/sounds/Retro.mp3')
#otherwise its too loud
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

isRunning = True
while isRunning:
    pygame.mixer.music.fadeout(99999)
    pygame.display.set_caption("Python OpenGL by Juan Pablo Pineda")
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse2 = pygame.MOUSEBUTTONDOWN;
    # Traslacion de camara
    if keys[K_d]:
        rend.camPosition.x += 1 * deltaTime
    if keys[K_a]:
        rend.camPosition.x -= 1 * deltaTime
    if keys[K_s]:
        rend.camPosition.y -= 1 * deltaTime
    if keys[K_w]:
        rend.camPosition.y += 1 * deltaTime
    if keys[K_UP]:
        if rend.normals > 0:
            rend.normals -= 0.1 * deltaTime
    if keys[K_DOWN]:
        if rend.normals < 0.2:
            rend.normals += 0.1 * deltaTime

    # Rotacion de camara
    if keys[K_q]:
        rend.camRotation.y += 15 * deltaTime
        rend.camPosition.x += 1.5 * deltaTime
    if keys[K_e]:
        rend.camRotation.y -= 15 * deltaTime
        rend.camPosition.x -= 1.5 * deltaTime
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            if ev.key == K_1:
                rend.filledMode()
            if ev.key == K_2:
                rend.wireframeMode()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 4:
                rend.camPosition.z -= 3 * deltaTime
            if ev.button == 5:
                rend.camPosition.z += 3 * deltaTime

    rend.dTime += deltaTime
    deltaTime = clock.tick(60) / 1000

    rend.render()

    pygame.display.flip()

pygame.quit()