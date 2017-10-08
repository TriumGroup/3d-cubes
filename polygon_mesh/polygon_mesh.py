import numpy as np
from math import sin, cos, tan, trunc
from camera import Camera


class PolygonMesh:
    def __init__(self):
        self.camera = Camera()
        self._vertices = []
        self._faces_point_indexes = []
        self._x_rotation_angle = 1.2
        self._y_rotation_angle = 2.0
        self._z_rotation_angle = -0.3
        # self._x_translation = 200
        # self._y_translation = 200
        # self._z_translation = 100
        self._x_translation = -80
        self._y_translation = 80
        self._z_translation = 0
        self._world_matrix = None

    def faces(self):
        return map(self._face, self._faces_point_indexes)

    def rotate(self, x, y, z):
        self._x_rotation_angle += x
        self._y_rotation_angle += y
        self._z_rotation_angle += z
        self._world_matrix = None

    def rotate_camera(self, distance=0, etha=0, phi=0):
        self.camera.observation_point_distance += distance
        self.camera.x_axis_angle += etha
        self.camera.z_axis_angle += phi
        print(
            self.camera.observation_point_distance,
            self.camera.x_axis_angle,
            self.camera.z_axis_angle
        )
        self._world_matrix = None

    def _face(self, face_point_indexes):
        face_points = map(self._face_point, face_point_indexes)
        return tuple(face_points)

    def _face_point(self, point_index):
        point = self._vertices[point_index]
        vector = np.append(point, 1)
        x, y, z, _ = vector.dot(self._world_vector())
        return trunc(x), trunc(y), trunc(z)

    def _world_vector(self):
        if self._world_matrix is None:
            rotation = self._x_rotation().dot(self._y_rotation()).dot(self._z_rotation())
            camera_view = self._look_at_lh().dot(self._perspective_fov_lh())
            self._world_matrix = rotation.dot(self._translation()).dot(camera_view)
        return self._world_matrix

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

    def _perspective_fov_lh(self, aspect=1, fov=0.78, z_near=1, z_far=100):
        tangent = 1 / tan(fov * 0.5)
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