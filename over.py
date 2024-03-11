import pygame
import sys

FONT_SIZE = 50
FADE_SPEED = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
# Button Class
class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.default_color = WHITE
        self.hover_color = (200, 200, 200)  # Color when button is hovered
        self.surface = self.font.render(text, True, self.default_color)
        self.rect = self.surface.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def set_hovered(self, hovered):
        if hovered:
            self.surface = self.font.render(self.text, True, self.hover_color)
        else:
            self.surface = self.font.render(self.text, True, self.default_color)

# Menu Scene Class
class OverScene:
    def __init__(self, screen,textdeath):
        self.screen = screen
        button_gap = 30  

        self.play_button = Button("Retry?", (screen.get_width() // 2, screen.get_height() * 3 // 4))
        self.quit_button = Button("Quit", (screen.get_width() // 2, screen.get_height() * 3 // 4 + self.play_button.rect.height + button_gap))
        self.buttons = [self.play_button, self.quit_button]

        self.hovered_button = None 
        self.title_font = pygame.font.Font(None, FONT_SIZE)
        self.title_text = self.title_font.render(textdeath, True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        
    def run(self):
        pygame.mixer.stop()
        while True:
            self.redraw_scene()
            self.screen.blit(self.title_text, self.title_rect)  # Adding title text

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                
                    if event.key == pygame.K_ESCAPE:
                        return None 
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                   for button in self.buttons:
                    if button.is_hovered(event.pos):
                        if button.text == "Retry?":
                            return None                
                    
                   self.handle_mouse_click(event.pos)  # Return the new scene when a button is clicked
            pygame.display.flip()         

    def handle_mouse_motion(self, pos):
       
        for button in self.buttons:
            if button.is_hovered(pos):
                if button != self.hovered_button:
                    self.hovered_button = button
                    button.set_hovered(True)
            else:
                if button == self.hovered_button:
                    self.hovered_button = None
                    button.set_hovered(False)

    def handle_mouse_click(self, pos):
       
        for button in self.buttons:
            if button.is_hovered(pos):
                if button.text == "Continue":
                    pass  # Transition to the game scene
                elif button.text == "Quit":
                    pygame.quit()
                    sys.exit()

    def redraw_scene(self):
        self.screen.fill(BLACK)
        for button in self.buttons:
            button.draw(self.screen)
