from math import sin, cos
import numpy as np


class Camera:
    def __init__(self, observation_point_distance=400, x_axis_angle=0.7, z_axis_angle=0.001):
        self.observation_point_distance = observation_point_distance
        self.x_axis_angle = x_axis_angle
        self.z_axis_angle = z_axis_angle
        self.target = np.array([0, 0, 0])

    def position(self):
        x = self.observation_point_distance * sin(self.x_axis_angle) * cos(self.z_axis_angle)
        y = self.observation_point_distance * sin(self.x_axis_angle) * sin(self.z_axis_angle)
        z = self.observation_point_distance * cos(self.x_axis_angle)
        # x = self.observation_point_distance * sin(self.z_axis_angle) * cos(self.x_axis_angle)
        # y = self.observation_point_distance * sin(self.z_axis_angle) * sin(self.x_axis_angle)
        # z = self.observation_point_distance * cos(self.z_axis_angle)
        return np.array([x, y, z])
