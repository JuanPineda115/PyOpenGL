import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from pygame import image
from numpy import array, float32

import obj


class Model(object):
    def __init__(self, objName, textureName):
        self.model = obj.Obj(objName)
        self.createVertexBuffer()
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)
        self.textureSurface = image.load(textureName)
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)

    def getModelMatrix(self):
        identity = glm.mat4(1)
        translateMatrix = glm.translate(identity, self.position)
        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        rotationMatrix = pitch * yaw * roll
        scaleMatrix = glm.scale(identity, self.scale)
        return translateMatrix * rotationMatrix * scaleMatrix

    def createVertexBuffer(self):
        buffer = []
        for face in self.model.faces:
            for i in range(3):
                # positions
                pos = self.model.vertices[face[i][0] - 1]
                self.appendToBuffer(buffer, pos)
                # normals
                norm = self.model.normals[face[i][2] - 1]
                self.appendToBuffer(buffer, norm)
                # texCoords
                uvs = self.model.texcoords[face[i][1] - 1]
                buffer.append(uvs[0])
                buffer.append(uvs[1])
        self.vertBuffer = array(buffer, dtype=float32)
        self.VBO = glGenBuffers(1)  # Vertex Buffer Object
        self.VAO = glGenVertexArrays(1)  # Vertex Array Object

    # def lookAt(self, eye: glm.vec3, camposition = glm.vec3(0,0,0)):
    #     front = camposition - eye
    #     front = front / glm.fastNormalize(front)
    #     right = 
    #     right =

    def appendToBuffer(self, buffer, arg1):
        buffer.append(arg1[0])
        buffer.append(arg1[1])
        buffer.append(arg1[2])

    def renderInScene(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        # Los vertices
        glBufferData(
            GL_ARRAY_BUFFER,
            self.vertBuffer.nbytes,
            self.vertBuffer,
            GL_STATIC_DRAW)
        # Atributo de posicion
        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE,
            4 * 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # Atributo de normales
        glVertexAttribPointer(
            1, 3, GL_FLOAT, GL_FALSE,
            4 * 8,  ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)
        # Atributo de coordenadas de textura
        glVertexAttribPointer(
            2, 2, GL_FLOAT, GL_FALSE,
            4 * 8, ctypes.c_void_p(4 * 6))
        glEnableVertexAttribArray(2)
        # Dar textura
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB, self.textureSurface.get_width(),
            self.textureSurface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE,
            self.textureData)
        glGenerateMipmap(GL_TEXTURE_2D)
        # Dibujar
        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces)
                     * 3)  # Para dibujar vertices en orden


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)
        self.scene = []
        self.pointLight = glm.vec3(-10, 0, -5)
        self.tiempo = 0
        self.valor = 0
        # View Matrix
        self.camPosition = glm.vec3(0, 0, 0)
        self.camRotation = glm.vec3(0, 0, 0)  # pitch, yaw, roll
        # Projection Matrix
        self.projectionMatrix = glm.perspective(
            glm.radians(60), self.width / self.height,
            0.1, 1000)

    def LookAt(self, eye, camPosition = glm.vec3(0,0,0)):

        pass

    def getViewMatrix(self):
        identity = glm.mat4(1)
        translateMatrix = glm.translate(identity, self.camPosition)
        pitch = glm.rotate(identity, glm.radians(
            self.camRotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(identity, glm.radians(
            self.camRotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(identity, glm.radians(
            self.camRotation.z), glm.vec3(0, 0, 1))
        rotationMatrix = pitch * yaw * roll
        camMatrix = translateMatrix * rotationMatrix
        return glm.inverse(camMatrix)

    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def setShaders(self, vertexShader, fragShader):
        if vertexShader is not None and fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.active_shader)
        if self.active_shader:
            glUniformMatrix4fv(
                glGetUniformLocation(self.active_shader, "viewMatrix"),
                1, GL_FALSE, glm.value_ptr(self.getViewMatrix()))
            glUniformMatrix4fv(
                glGetUniformLocation(self.active_shader, "projectionMatrix"),
                1, GL_FALSE, glm.value_ptr(self.projectionMatrix))
            glUniform1f(glGetUniformLocation(
                self.active_shader, "tiempo"), self.tiempo)
            glUniform1f(glGetUniformLocation(
                self.active_shader, "valor"), self.valor)
            glUniform3f(glGetUniformLocation(self.active_shader, "pointLight"),
                        self.pointLight.x, self.pointLight.y, self.pointLight.z)
        for model in self.scene:
            if self.active_shader:
                glUniformMatrix4fv(
                    glGetUniformLocation(self.active_shader, "modelMatrix"),
                    1, GL_FALSE, glm.value_ptr(model.getModelMatrix()))
            model.renderInScene()
