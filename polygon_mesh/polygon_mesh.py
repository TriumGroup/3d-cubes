import numpy as np
from math import sin, cos, tan, trunc
from camera import Camera


class PolygonMesh:
    def __init__(self, size):
        self.camera = Camera()
        self._vertices = []
        self._translated_vertices = []
        self._faces_point_indexes = []
        self._width = size
        self._height = size
        self._x_rotation_angle = 0.1
        self._y_rotation_angle = 2.5
        self._z_rotation_angle = -1
        self._x_translation = 0
        self._y_translation = 0
        self._z_translation = 0
        self._perspective = 0
        self._world_matrix = np.array([])

    def rotate(self, x, y, z):
        self._x_rotation_angle += x
        self._y_rotation_angle += y
        self._z_rotation_angle += z
        self._translated_vertices = []

    def rotate_camera(self, distance=0, etha=0, phi=0):
        self.camera.observation_point_distance += distance
        self.camera.x_axis_angle += etha
        self.camera.z_axis_angle += phi
        self._translated_vertices = []

    def change_perspective(self, perspective):
        self._perspective += perspective
        self._translated_vertices = []

    def faces(self):
        if len(self._translated_vertices) == 0:
            self._translate_vertices()
        return map(self._face, self._faces_point_indexes)

    def _translate_vertices(self):
        self._world_matrix = self._prepare_world_matrix()
        self._translated_vertices = list(map(self._translate_vertex, self._vertices))

    def _translate_vertex(self, vertex):
        x, y, z, w = vertex.vector.dot(self._world_matrix)
        x, y, z = x / w, y / w, z
        x = x * self._width + self._width / 2
        y = -y * self._height + self._height / 2
        return trunc(x), trunc(y), trunc(z)

    def _face(self, face_point_indexes):
        face_points = map(self._face_point, face_point_indexes)
        return tuple(face_points)

    def _face_point(self, point_index):
        return self._translated_vertices[point_index]

    def _prepare_world_matrix(self):
        view_matrix = self._look_at_lh()
        projection_matrix = self._perspective_fov_lh()
        pitch_roll = self._z_rotation().dot(self._x_rotation()).dot(self._y_rotation())
        world_matrix = pitch_roll.dot(self._translation())
        transform_matrix = world_matrix.dot(view_matrix).dot(projection_matrix).dot(self._perspective_matrix())
        return transform_matrix

    def _perspective_matrix(self):
        return np.array([
            [1, 0, 0, self._perspective],
            [0, 1, 0, self._perspective],
            [0, 0, 0, -self._perspective],
            [0, 0, 0, 1]
        ])

    def _look_at_lh(self):
        up_vect = np.array([0, 1, 0])
        eye = self.camera.position()
        z_axis = (self.camera.target - eye)
        norm_z = np.linalg.norm(z_axis)
        z_axis = z_axis / norm_z if norm_z != 0 else 1

        x_axis = np.cross(up_vect, z_axis)
        norm_x = np.linalg.norm(x_axis)
        x_axis = x_axis / norm_x if norm_x != 0 else 1

        y_axis = np.cross(z_axis, x_axis)
        norm_y = np.linalg.norm(y_axis)
        y_axis = y_axis / norm_y if norm_y != 0 else 1

        ex = -x_axis.dot(eye)
        ey = -y_axis.dot(eye)
        ez = -z_axis.dot(eye)

        return np.array([
            [x_axis[0], y_axis[0], z_axis[0], 0],
            [x_axis[1], y_axis[1], z_axis[1], 0],
            [x_axis[2], y_axis[2], z_axis[2], 0],
            [ex, ey, ez, 1]
        ])

    def _perspective_fov_lh(self, fov=0.78, z_near=1, z_far=100):
        tangent = 1 / tan(fov * 0.5)
        aspect = self._width / self._height
        return np.array([
            [tangent / aspect, 0, 0, 0],
            [0, tangent, 0, 0],
            [0, 0, -z_far / (z_near - z_far), 1],
            [0, 0, z_near * z_far / (z_near - z_far), 0]
        ])

    def _translation(self):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [self._x_translation,  self._y_translation,  self._z_translation, 1]
        ])

    def _x_rotation(self):
        sine, cosine = sin(self._x_rotation_angle), cos(self._x_rotation_angle)
        return np.array([
            [1, 0, 0, 0],
            [0, cosine, sine, 0],
            [0, -sine, cosine, 0],
            [0, 0, 0, 1]
        ])

    def _y_rotation(self):
        sine, cosine = sin(self._y_rotation_angle), cos(self._y_rotation_angle)
        return np.array([
            [cosine, 0, -sine, 0],
            [0, 1, 0, 0],
            [sine, 0, cosine, 0],
            [0, 0, 0, 1]
        ])

    def _z_rotation(self):
        sine, cosine = sin(self._z_rotation_angle), cos(self._z_rotation_angle)
        return np.array([
            [cosine, sine, 0, 0],
            [-sine, cosine, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])