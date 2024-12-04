#Player

import pygame as pg
from camera import Camera
from settings import *
from terrain_gen import get_height  # Ensure get_height is accessible

class Player(Camera):
    """
    The Player class manages the player's movement, gravity, and interaction with the world. 
    It extends the Camera class to control the player's view and position.
    """
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        """
        Initializes the player with a given position, yaw, and pitch. 
        Adjusts the player's position to be above the terrain using the height offset.
        """
        self.app = app

        ground_y = get_height(position[0], position[1])
        start_position = (position[0], ground_y + PLAYER_HEIGHT_OFFSET, position[2])

        super().__init__(start_position, yaw, pitch)

        self.velocity_y = 0
        self.ground_level = ground_y
        self.gravity = 0.8

    def update(self):
        """
        Updates the player's movement, gravity, and orientation.
        This method is called each frame to update the player’s state based on input.
        """
        self.apply_gravity() 
        self.keyboard_control() 
        self.mouse_control()  
        super().update() 

    def apply_gravity(self):
        """
        Applies gravity to the player, ensuring smooth vertical movement and preventing the player from falling through the terrain.
        The player's position is adjusted based on the terrain height, maintaining the player at a constant height above the terrain.
        """
        terrain_y = get_height(self.position.x, self.position.z)
        target_height = terrain_y + PLAYER_HEIGHT_OFFSET

        if self.position.y > target_height:
            self.velocity_y += self.gravity * self.app.delta_time
            self.position.y -= self.velocity_y * self.app.delta_time

        elif self.position.y < target_height:
            self.velocity_y = 0  
            self.position.y = target_height  

        else:
            self.velocity_y = 0

    def check_ground_collision(self):
        """
        Prevents the player from sinking below the ground and ensures they stay above the terrain.
        This method corrects the player's position if it moves below the ground level.
        """
        terrain_y = get_height(self.position.x, self.position.z)
        target_height = terrain_y + PLAYER_HEIGHT_OFFSET

        if self.position.y < target_height:
            self.position.y = target_height

    def keyboard_control(self):
        """
        Handles player movement based on keyboard inputs (W, A, S, D).
        This method also removes the jumping functionality, as requested.
        """
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time

        if key_state[pg.K_w]:
            self.move_forward(vel)
        if key_state[pg.K_s]:
            self.move_back(vel)
        if key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_a]:
            self.move_left(vel)

    def mouse_control(self):
        """
        Rotates the camera based on mouse movement.

        This method allows the player to look around the world by moving the mouse.
        """
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def handle_event(self, event):
        """
        Handles mouse clicks for voxel interaction.
        This method handles the left and right mouse button presses to interact with the world.
        """
        voxel_handler = self.app.scene.world.voxel_handler
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()
        elif event.type == pg.MOUSEWHEEL:
            if event.y < 0 :
                voxel_handler.switch_voxel_down()
            elif event.y > 0 :
                voxel_handler.switch_voxel_up()
            print(voxel_handler.see_voxel())