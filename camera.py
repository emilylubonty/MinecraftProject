# camera.py

from settings import *
from frustum import Frustum
import glm

class Camera:
    """
    Represents a camera in the 3D world, handling position, orientation, 
    and perspective projection. Supports movement and rotation in the scene.
    """
    def __init__(self, position, yaw, pitch):
        """
        Initializes the camera with a given position and orientation.
        """
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

        self.frustum = Frustum(self)

    def update(self):
        """
        Updates the camera's orientation vectors and view matrix. 
        Call this method every frame to ensure the camera's direction 
        and position are properly synchronized.
        """
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        """
        Sets the view matrix using the camera's position and forward direction.
        The matrix aligns the camera's coordinate system with the world.
        """
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        """
        Updates the camera's forward, right, and up vectors based on the yaw and pitch angles.
        Ensures the vectors are normalized for accurate movement and rotation.
        """
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        """
        Adjusts the camera's pitch (up/down rotation) within a clamped range.
        """
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        """
        Adjusts the camera's yaw (left/right rotation).
        """
        self.yaw += delta_x

    def move_left(self, velocity):
        """
        Moves the camera to the left along the x-z plane.
        """
        self.position -= self.right * velocity

    def move_right(self, velocity):
        """
        Moves the camera to the right along the x-z plane.
        """
        self.position += self.right * velocity

    def move_forward(self, velocity):
        """
        Moves the camera forward along the x-z plane.
        """
        self.position += self.forward * velocity

    def move_back(self, velocity):
        """
        Moves the camera backward along the x-z plane.
        """
        self.position -= self.forward * velocity