import pygame
from game_scene import GameScene
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
class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        button_gap = 30  

        self.play_button = Button("Play", (screen.get_width() // 2, screen.get_height() * 3 // 4))
        self.quit_button = Button("Quit", (screen.get_width() // 2, screen.get_height() * 3 // 4 + self.play_button.rect.height + button_gap))
        self.buttons = [self.play_button, self.quit_button]

        self.hovered_button = None 

    def run(self):
       
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return self.handle_mouse_click(event.pos)  # Return the new scene when a button is clicked
            self.redraw_scene()
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
                if button.text == "Play":
                    print("Play button clicked")
                    return GameScene(self.screen)  # Transition to the game scene
                elif button.text == "Quit":
                    print("Quit button clicked")
                    pygame.quit()
                    sys.exit()

    def redraw_scene(self):
        self.screen.fill(BLACK)
        for button in self.buttons:
            button.draw(self.screen)
