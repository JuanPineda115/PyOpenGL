from OpenGL.raw.GL.VERSION.GL_1_0 import GL_GREEN
import pygame
from pygame.locals import *
import glm
from GraphLib import Renderer, Model
import shaders

#--------------------------------------Initial Data--------------------------------------#
width = 1600
height = 900
deltaTime = 0.0
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
clock = pygame.time.Clock()
titleFont = pygame.font.Font("src/fonts/pixfont.ttf", 90)

#--------------------------------------Components--------------------------------------#
def newButton(x, y, w, h, text, color, centerx, centery):
    btnTxt = pygame.font.Font('src/fonts/pixfont.ttf', 30)
    btn = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, btn)
    bs, br = newText(text, btnTxt)
    br.center = (centerx, centery)
    screen.blit(bs, br)
    return btn

def newText(text, font, colour=pygame.Color("Black")):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


#--------------------------------------menus and screens--------------------------------------#
def menu():
    flag = True
    while flag:
        # menu event loop
        click = False
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True
            elif ev.type == pygame.QUIT:
                flag = False
        # screen fill
        bg = pygame.image.load("src/images/titlescreen.jpg")
        bg = pygame.transform.scale(bg, (width, height))
        bgrect = bg.get_rect()
        screen.blit(bg, bgrect)
        # title text
        surface, tr = newText("PyOpenGL by Juan Pablo Pineda", titleFont)
        tr.center = ((width/2), (height/2)-100)
        screen.blit(surface, tr)
        # mouse position for buttons
        mx, my = pygame.mouse.get_pos()
        # Buttons
        gamebutton = newButton(725, 400, 150, 50, "Continue", pygame.Color("gray"), width/2, 420)
        quitbutton = newButton(725, 470, 150, 50, "Quit", pygame.Color("gray"), width/2, 490)
        # button listeners
        if gamebutton.collidepoint((mx, my)):
            if click:
                # breaks the menu loop
                flag = False
                # goes to map select menu
                gaem()
        elif quitbutton.collidepoint((mx, my)):
            if click:
                # breaks the menu loop
                flag = False
                # returns false to end the program
                pygame.quit()
                quit()
        pygame.display.update()
        clock.tick(100)

def gaem():
    glScreen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.OPENGL )
    rend = Renderer(glScreen)
    rend.setShaders(shaders.vertex_shader, shaders.fragment_shader)
    uniqueModel = Model('src/Objects/katana.obj', 'src/Textures/brighter.png')
    uniqueModel.position.z = -7
    uniqueModel.position.x = -5
    uniqueModel.rotation.x = -90
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
                    if rend.camPosition.z > -7:
                        rend.camPosition.z -= 3 * deltaTime
                if ev.button == 5:
                    if rend.camPosition.z < 5:
                        rend.camPosition.z += 3 * deltaTime
        deltaTime = clock.tick(60) / 1000
        rend.dTime += deltaTime
        rend.render()
        pygame.display.flip()

menu()
pygame.quit()