# Loading Scene Class
import pygame
from menu_scene import MenuScene
FONT_SIZE = 50
FADE_SPEED = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
class LoadingScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.text = "Millions must confess the devil is now the lord, billions even."
        self.alpha = 0  # Initial alpha value for text transparency

    def run(self):
        fade_in_complete = False
        fade_out_complete = False

        # Fade in
        while not fade_in_complete:
            self.alpha = min(self.alpha + FADE_SPEED, 255)  # Increase alpha gradually
            self.render_text()
            pygame.display.flip()
            pygame.time.delay(10)
            handle_events()
            fade_in_complete = self.alpha >= 255

        # Stay for a few seconds
        pygame.time.delay(2000)

        # Fade out
        while not fade_out_complete:
            self.alpha = max(self.alpha - FADE_SPEED, 0)  # Decrease alpha gradually
            self.render_text()
            pygame.display.flip()
            pygame.time.delay(10)
            handle_events()
            fade_out_complete = self.alpha <= 0

        return MenuScene(self.screen)  # Transition to the menu scene

    def render_text(self):
        text_surf = self.font.render(self.text, True, WHITE)
        text_surf.set_alpha(self.alpha)
        text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.fill(BLACK)
        self.screen.blit(text_surf, text_rect)
