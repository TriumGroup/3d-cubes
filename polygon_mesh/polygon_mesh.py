import numpy as np
from math import sin, cos, trunc


class PolygonMesh:
    def __init__(self):
        self._vertices = []
        self._faces_point_indexes = []
        self.x_rotation_angle = 0.1
        self.y_rotation_angle = 0.1
        self.z_rotation_angle = 0
        self._x_translation = 300
        self._y_translation = 300
        self._z_translation = 100

    def faces(self):
        return map(self._face, self._faces_point_indexes)

    def rotate(self, x, y, z):
        self.x_rotation_angle += x
        self.y_rotation_angle += y
        self.z_rotation_angle += z

    def _face(self, face_point_indexes):
        face_points = map(self._face_point, face_point_indexes)
        return tuple(face_points)

    def _face_point(self, point_index):
        point = self._vertices[point_index]
        vector = np.append(point, 1)
        x, y, z, _ = self._translate_vector(self._rotate_vector(vector))
        return trunc(x), trunc(y), trunc(z)

    def _rotate_vector(self, vector):
        return vector.dot(self._x_rotation()).dot(self._y_rotation()).dot(self._z_rotation())

    def _translate_vector(self, vector):
        return vector.dot(self._translation())

    def _translation(self):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [self._x_translation,  self._y_translation,  self._z_translation, 1]
        ])

    def _x_rotation(self):
        sine, cosine = sin(self.x_rotation_angle), cos(self.x_rotation_angle)
        return np.array([
            [1, 0, 0, 0],
            [0, cosine, sine, 0],
            [0, -sine, cosine, 0],
            [0, 0, 0, 1]
        ])

    def _y_rotation(self):
        sine, cosine = sin(self.y_rotation_angle), cos(self.y_rotation_angle)
        return np.array([
            [cosine, 0, -sine, 0],
            [0, 1, 0, 0],
            [sine, 0, cosine, 0],
            [0, 0, 0, 1]
        ])

    def _z_rotation(self):
        sine, cosine = sin(self.z_rotation_angle), cos(self.z_rotation_angle)
        return np.array([
            [cosine, sine, 0, 0],
            [-sine, cosine, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])