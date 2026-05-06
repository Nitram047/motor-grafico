"""
Viewport – QOpenGLWidget que albergará el renderizado con ModernGL.

Por ahora limpia el fondo con un color gris oscuro y muestra un
mensaje "Viewport – Sin motor". Más adelante se conectará al
contexto OpenGL y al renderizador.
"""

import glm
import moderngl
import numpy as np
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt

from engine.core.engine import Engine
from engine.scene import Node, VoxelWorldNode
from engine.camera import Camera
from engine.renderer import Renderer
from engine.voxel_world import patterns


class Viewport(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)

        self.engine = None
        self.scene_root = None
        self.voxel_node = None
        self.camera = None
        self.renderer = None
        self.current_pattern = "checker"
        self._initialized = False
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def initializeGL(self):
        self.makeCurrent()
        # Envolver el contexto Qt (no necesita parámetros)
        self.ctx = moderngl.create_context()

        self.engine = Engine()
        self.engine.init(self.ctx)

        # Escena
        self.scene_root = Node("root")
        self.voxel_node = VoxelWorldNode(chunk_size=16)
        self.scene_root.add_child(self.voxel_node)

        self.camera = Camera(mode="orbit", world_center=glm.vec3(8, 8, 8))
        self.renderer = Renderer(self.engine)

        # Cargar patrón inicial
        self._load_pattern(self.current_pattern)

        print(f"ModernGL {self.ctx.version_code}, instancias={self.voxel_node.instance_count}")
        self._initialized = True
        self.update()
        self.setFocus()

    def _load_pattern(self, name):
        print(f"Cargando patrón {name}...")
        voxels = patterns[name]()
        # Liberar el VAO y buffers de instancia anteriores (si existen)
        if self.voxel_node.vao:
            self.voxel_node.vao.release()
            self.voxel_node.instance_pos_vbo.release()
            self.voxel_node.instance_color_vbo.release()
        self.voxel_node.load_voxel_data(voxels)
        self.voxel_node.setup_vao(self.engine)
        print(self.voxel_node._positions[:5])
        print(f"Nuevo número de instancias: {self.voxel_node.instance_count}")
        # Forzar un repintado inmediato
        self.update()

    def resizeGL(self, w, h):
        if self._initialized:
            # ModernGL necesita saber el tamaño del framebuffer activo
            fbo = self.ctx.detect_framebuffer()
            if fbo:
                fbo.use()
            self.ctx.viewport = (0, 0, w, h)

    def paintGL(self):
        if not self._initialized:
            return

        self.makeCurrent()

        # Activar depth test y escritura en buffer de profundidad
        #self.ctx.enable(moderngl.DEPTH_TEST)
        #self.ctx.depth_mask = True

        # Limpiar color y profundidad
        self.ctx.clear(0.15, 0.15, 0.15, 1.0, depth=1.0)

        # Desactivar face culling por si acaso (para ver todas las caras)
        self.ctx.disable(moderngl.CULL_FACE)

        # Dibujar la escena
        self.renderer.draw_scene(
            self.scene_root,
            self.camera,
            self.width(),
            self.height(),
        )

        self.ctx.finish()
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_1:
            print("I work")
            self.current_pattern = "solid"
            self._load_pattern("solid")
        elif key == Qt.Key.Key_2:
            self.current_pattern = "stairs"
            self._load_pattern("stairs")
        elif key == Qt.Key.Key_3:
            self.current_pattern = "pyramid"
            self._load_pattern("pyramid")
        elif key == Qt.Key.Key_4:
            self.current_pattern = "checker"
            self._load_pattern("checker")
        elif key == Qt.Key.Key_C:
            self.camera.toggle_mode()
        else:
            super().keyPressEvent(event)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()