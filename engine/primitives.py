"""
Geometrías básicas compartidas.

Proporciona los datos del cubo unidad (1×1×1) centrado en el origen.
La función devuelve (vértices, normales, índices) como arrays numpy.
"""

import numpy as np

def create_unit_cube():
    """Devuelve (vertices, indices) con 24 vértices (3 floats cada uno) y 36 índices."""
    h = 0.5
    # Definición cuidadosa: cada cara en CCW visto desde fuera
    # Formato: cara normal, luego 4 vértices en orden CCW
    faces = [
        # Front (+Z) : mirando hacia +Z, el orden CCW es (-,-) -> (+,-) -> (+,+) -> (-,+)
        ((0,0,1), (-h, -h,  h), ( h, -h,  h), ( h,  h,  h), (-h,  h,  h)),
        # Back (-Z) : mirando hacia -Z, el orden CCW es (+,-) -> (-,-) -> (-,+) -> (+,+)
        ((0,0,-1), ( h, -h, -h), (-h, -h, -h), (-h,  h, -h), ( h,  h, -h)),
        # Up (+Z) -> aquí Z es arriba, pero en nuestro sistema Z up, "up" es +Z
        # La cara superior en Z = +h, mirando hacia +Z, ya está cubierta en Front?
        # En realidad, si Z es arriba, la cara "top" es la que tiene normal +Z, ya la tenemos como Front.
        # Pero necesitamos las seis caras: derecha (+X), izquierda (-X), superior (+Z), inferior (-Z), frontal? 
        # Ajustemos: Usaremos normales consistentes con ejes:
        # X right, Y front, Z up.
        # Caras: Right (+X), Left (-X), Top (+Z), Bottom (-Z), Front (+Y), Back (-Y)
        # ------------------------------------------------------------
        # Derecha (+X)
        ((1,0,0), ( h, -h, -h), ( h,  h, -h), ( h,  h,  h), ( h, -h,  h)),
        # Izquierda (-X)
        ((-1,0,0), (-h, -h,  h), (-h,  h,  h), (-h,  h, -h), (-h, -h, -h)),
        # Superior (+Z)
        ((0,0,1), (-h, -h,  h), ( h, -h,  h), ( h,  h,  h), (-h,  h,  h)),
        # Inferior (-Z)
        ((0,0,-1), (-h, -h, -h), (-h,  h, -h), ( h,  h, -h), ( h, -h, -h)),
        # Frontal (+Y)
        ((0,1,0), (-h,  h, -h), ( h,  h, -h), ( h,  h,  h), (-h,  h,  h)),
        # Trasera (-Y)
        ((0,-1,0), (-h, -h,  h), ( h, -h,  h), ( h, -h, -h), (-h, -h, -h)),
    ]

    vertices = []
    indices = []
    v_offset = 0
    for normal, v0, v1, v2, v3 in faces:
        for v in (v0, v1, v2, v3):
            vertices.extend(v)
        indices.extend([v_offset, v_offset+1, v_offset+2,
                        v_offset, v_offset+2, v_offset+3])
        v_offset += 4

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)