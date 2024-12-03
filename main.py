from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures
from settings import *

class DialogueBox:
    def __init__(self, screen, font_name="Monospace", font_size=20, box_color=(0, 0, 0, 180), text_color=(255, 255, 255)):
        self.screen = screen
        self.font = pg.font.SysFont(font_name, font_size)
        self.box_color = box_color
        self.text_color = text_color
        self.is_visible = False
        self.quest_text = ""

    def show(self, text):
        self.quest_text = text
        self.is_visible = True

    def hide(self):
        self.is_visible = False

    def render(self):
        if not self.is_visible:
            return
        
        box_width, box_height = 400, 100
        box_surface = pg.Surface((box_width, box_height), pg.SRCALPHA)
        box_surface.fill(self.box_color)
        
        text_surface = self.font.render(self.quest_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(box_width // 2, box_height // 2))
        box_surface.blit(text_surface, text_rect)

        screen_rect = self.screen.get_rect()
        box_rect = box_surface.get_rect(center=(screen_rect.centerx, screen_rect.centery))
        self.screen.blit(box_surface, box_rect)

class VoxelEngine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, DEPTH_SIZE)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)

        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.is_running = True
        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)
        self.dialogue_box = DialogueBox(self.screen)

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')

    def render(self):
        self.ctx.clear(color=BG_COLOR)
        self.dialogue_box.render()
        self.scene.render()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_q:
                self.quest_box.show("Find a water source!")
            elif event.type == pg.KEYDOWN and event.key == pg.K_h:
                self.quest_box.hide()
            self.player.handle_event(event=event)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    app = VoxelEngine()
    app.run()
