import textwrap
import pygame as pg

class DialogueBox:
    def __init__(self, engine, font_name="Monospace", font_size=20, box_color=(0, 0, 0, 180), text_color=(255, 255, 255)):
        self.engine = engine
        self.font = pg.font.SysFont(font_name, font_size)
        self.box_color = box_color
        self.text_color = text_color
        self.is_visible = False
        self.quest_text = ""
        self.auto_hide = False
        self.hide_time = 0

    def show(self, text, duration=None):
        self.quest_text = text
        self.is_visible = True
        if duration:
            self.auto_hide = True
            self.hide_time = pg.time.get_ticks() + duration * 1000

    def hide(self):
        self.is_visible = False
        self.auto_hide = False

    def render(self, display_surface):
        if not self.is_visible:
            return
        
        if self.auto_hide and pg.time.get_ticks() > self.hide_time:
            self.hide()
            return

        screen_width, screen_height = display_surface.get_size()

        box_width, box_height = screen_width // 2, screen_height // 7
        box_surface = pg.Surface((box_width, box_height), pg.SRCALPHA)
        box_surface.fill(self.box_color)

        wrapped_text = textwrap.fill(self.quest_text, width=35)
        lines = wrapped_text.splitlines()
        
        y_offset = (box_height - len(lines) * self.font.get_height()) // 2

        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(box_width // 2, box_height // 2 + y_offset))
            box_surface.blit(text_surface, text_rect)
            y_offset += self.font.get_height()

        screen_rect = display_surface.get_rect()
        box_rect = box_surface.get_rect(center=(screen_rect.centerx, screen_rect.centery))
        display_surface.blit(box_surface, box_rect)