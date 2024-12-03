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