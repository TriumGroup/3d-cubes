from polygon_mesh.polygon_mesh import PolygonMesh
from polygon_mesh.point import Point


class CubesMesh(PolygonMesh):
    EDGE_LENGTH = 40

    def __init__(self, renderer):
        super().__init__(renderer)
        self._init_cubes_vertices()
        self._init_faces_point_indexes()

    def _init_cubes_vertices(self):
        self._vertices = [
            Point(0, 0, 0),
            Point(self.EDGE_LENGTH, 0, 0),
            Point(self.EDGE_LENGTH, -self.EDGE_LENGTH, 0),
            Point(0, -self.EDGE_LENGTH, 0),
            Point(0, 0, -self.EDGE_LENGTH),
            Point(self.EDGE_LENGTH, 0, -self.EDGE_LENGTH),
            Point(self.EDGE_LENGTH, -self.EDGE_LENGTH, -self.EDGE_LENGTH),
            Point(0, -self.EDGE_LENGTH, -self.EDGE_LENGTH),
            Point(0, 0, self.EDGE_LENGTH),
            Point(0, -self.EDGE_LENGTH, self.EDGE_LENGTH),
            Point(-self.EDGE_LENGTH, -self.EDGE_LENGTH, self.EDGE_LENGTH),
            Point(-self.EDGE_LENGTH, 0, self.EDGE_LENGTH),
            Point(-self.EDGE_LENGTH, 0, 0),
            Point(-self.EDGE_LENGTH, -self.EDGE_LENGTH, 0),
            Point(-self.EDGE_LENGTH, self.EDGE_LENGTH, 0),
            Point(0, self.EDGE_LENGTH, 0),
            Point(-self.EDGE_LENGTH, 0, -self.EDGE_LENGTH),
            Point(-self.EDGE_LENGTH, self.EDGE_LENGTH, -self.EDGE_LENGTH),
            Point(0, self.EDGE_LENGTH, -self.EDGE_LENGTH)
        ]

    def _init_faces_point_indexes(self):
        self._faces_point_indexes = [
            [0, 1, 2, 3],
            [0, 1, 5, 4],
            [1, 2, 6, 5],
            [2, 3, 7, 6],
            [3, 0, 4, 7],
            [4, 5, 6, 7],
            [11, 8, 9, 10],
            [11, 8, 0, 12],
            [8, 9, 3, 0],
            [9, 10, 13, 3],
            [10, 11, 12, 13],
            [12, 0, 3, 13],
            [14, 15, 0, 12],
            [14, 15, 18, 17],
            [15, 0, 4, 18],
            [0, 12, 16, 4],
            [12, 14, 17, 16],
            [17, 18, 4, 16]
        ]



