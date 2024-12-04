from settings import *
import pygame as pg

class Display_Blocks():
    def __init__(self,app, background = "brown", text_color = "white"):
        self.font = pg.font.SysFont("rockwell", 20)
        self.background = background
        self.text_color = text_color
        self.app = app
    def display_voxel(self,show_block_type):
        voxel_handler = self.app.scene.world.voxel_handler
        block_type = self.font
        block_type = block_type.render("Your current block is:  " + voxel_handler.see_voxel(), True, self.text_color, self.background)
        block_type_rect = block_type.get_rect()
        block_type_rect.topleft = (0, 0)

        show_block_type.blit(block_type, block_type_rect)
    
