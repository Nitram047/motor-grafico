"""
Renderizador: recorre la escena y dibuja utilizando el engine.
"""

class Renderer:
    def __init__(self, engine):
        self.engine = engine

    def draw_scene(self, scene_root, camera, viewport_width, viewport_height):
        if scene_root is None:
            return

        view = camera.get_view_matrix()
        proj = camera.projection_matrix(viewport_width, viewport_height)

        scene_root.render(view, proj, self.engine.program)