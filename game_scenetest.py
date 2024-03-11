import pygame
from pygame import Color
import sys
import math
import random
import json

from fog import Fog

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT_SIZE = 50
FADE_SPEED = 1
bplevels = "levels/"
# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



class Star:
    def __init__(self, x, y, speed, radius, rocket=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.rocket = rocket
        self.radius = radius

    def move(self):
        if not self.rocket:
            self.y -= self.speed
        else:
            self.y += self.speed

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.GROUND_HEIGHT = self.screen.get_height()/21.6
        self.CHARACTER_WIDTH = 50
        self.CHARACTER_HEIGHT = 50
        self.JUMP_FORCE = -15
        self.GRAVITY = 0.9
        self.SPAWN_SPEED = 0.5
        self.LEG_LENGTH = 20
        self.LEG_ANGLE_RANGE = 30

        self.num_stars = 15
        self.star_speed_min = 1
        self.star_speed_max = 1
        self.stars = self.create_stars(self.num_stars, self.star_speed_min, self.star_speed_max)

        self.character_x = screen.get_width() // 2 - self.CHARACTER_WIDTH // 2
        self.character_y = screen.get_height() + self.CHARACTER_HEIGHT
        self.spawn_complete = False
        self.move_direction = 0
        self.character_dy = 0
        self.on_ground = True

        self.ground_rect = pygame.Rect(0, screen.get_height() - self.GROUND_HEIGHT, screen.get_width(), self.GROUND_HEIGHT)

        self.font = pygame.font.Font(None, 40)
        self.story_texts = [
            "In the world of Devils",
            "Death is the beggining",
            "Even you have been dragged out of your grave",
            "Just suffering everywhere",
            "Nothing is normal",
            "Find a way to revive the gods",
            "And",
            "Don't Pray."
        ]
        self.current_story_index = 0
        self.story_surface = self.font.render(self.story_texts[self.current_story_index], True, (255, 255, 255))
        self.story_rect = self.story_surface.get_rect(center=(screen.get_width() // 2, 100))
        self.show_next_text = pygame.time.get_ticks() + 5000

        self.lightning_surface = pygame.Surface((self.screen.get_width(),self.screen.get_height()), pygame.SRCALPHA)
        self.lightningtimes = 20

        self.lightning_generated = 0
        self.fog = Fog(self.screen)
        # Load images
        self.base_path = "assets/src/"  #imgs directory
        self.bp_sound = "assets/src_audio/"
        self.thunder = pygame.mixer.Sound(self.bp_sound +"thunder.wav")
        self.level="1"
        # Load images from JSON file
        self.images = self.load_images_from_json(bplevels+self.level+"images_list.json")
        self.collision_boxes = self.load_collision_boxes(bplevels + self.level + "collision_boxes.json")
        self.thunder.play()
    # Function to generate a single lightning strike from the middle to the bottom

    def generate_single_lightning(self):
        
        start_x = self.screen.get_width() // 2
        start_y = 0
        end_y = self.screen.get_height()
        segments = [(start_x, start_y)]
        current_y = start_y
        while current_y < end_y:
            new_x = segments[-1][0] + random.randint(-10, 10)
            new_y = segments[-1][1] + random.randint(10, 30)
            if new_y > end_y:
                new_y = end_y
            segments.append((new_x, new_y))
            current_y = new_y
            
        for i in range(len(segments) - 1):
            # Draw the lightning segment
            self.lightning_surface.fill((0, 0, 0, 0))

            pygame.draw.line(self.lightning_surface, (255, 255, 255, random.randint(200, 255)), segments[i], segments[i + 1], random.randint(3, 5))
    def load_collision_boxes(self, json_file):
        with open(json_file, "r") as f:
            collision_data = json.load(f)
        return [pygame.Rect(box["x"], box["y"], box["width"], box["height"]) for box in collision_data]

    def check_collision(self):
        player_rect = pygame.Rect(self.character_x, self.character_y, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT + self.LEG_LENGTH)
        for box in self.collision_boxes:
            
            if player_rect.colliderect(box):
                return True
        return False

    def load_images_from_json(self, json_file):
        with open(json_file, "r") as f:
            image_filenames = json.load(f)

        images = {}
        for filename in image_filenames:
            image_name = filename.split(".")[0]  # Extract image name from filename
            image_path = self.base_path + filename
            images[image_name] = pygame.image.load(image_path).convert_alpha()

        return images
 
    def blit_image(self, img_name, x, y, size):
        image = self.images.get(img_name)
        if image:
            scaled_image = pygame.transform.scale(image, size)
            self.screen.blit(scaled_image, (x, y))
        else:
            print(f"Image '{img_name}' not found.")

    def blit_from_json(self, json_file):
        with open(json_file, "r") as f:
            blit_data = json.load(f)

        for data in blit_data:
            image_name = data["image_name"]
            x = self.evaluate_value(data["x"])
            y = self.evaluate_value(data["y"])
            size = [self.evaluate_value(s) for s in data["size"]]

            self.blit_image(image_name, x, y, size)
        with open(bplevels + self.level + "collision_boxes.json", "r") as f:
            collision_data = json.load(f)

        for data in collision_data:
            rect = pygame.Rect(data["x"], data["y"], data["width"], data["height"])
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)  # Draw a red rectangle with a border   
          
    def evaluate_value(self, value):
        if isinstance(value, str) and "self" in value:
            return eval(value)
        return int(value)
   

    def create_stars(self, num_stars, min_speed, max_speed):
        stars = []
        for _ in range(num_stars):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            speed = random.randint(min_speed, max_speed)
            star_radius = 2
            stars.append(Star(x, y, speed, star_radius))
        return stars
  
    def move_stars(self):
        for star in self.stars:
            star.move()
            if star.y < -10:
                star.y = self.screen.get_height() + 10
                star.x = random.randint(0, self.screen.get_width())

    def draw_stars(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (star.x, star.y), star.radius)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.spawn_complete and self.on_ground:
                    self.character_dy = self.JUMP_FORCE
                elif event.key == pygame.K_a:
                    self.move_direction = -1
                elif event.key == pygame.K_d:
                    self.move_direction = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and self.move_direction == -1:
                    self.move_direction = 0
                elif event.key == pygame.K_d and self.move_direction == 1:
                    self.move_direction = 0

    def update_character(self):
        self.on_ground = False  # Assume not on the ground by default
        nowvaluex = self.character_x
        nowvaluey = self.character_y
        if not self.spawn_complete:
            # Check if lightning has been generated
            if self.lightning_generated <self.lightningtimes and self.character_y <= self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH + 90:
                self.lightning_generated+=1
                self.generate_single_lightning()  # Generate single lightning strike
            self.character_y -= self.SPAWN_SPEED
            if self.character_y <= self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH:
                self.character_y = self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH
                self.spawn_complete = True

        else:
            
            self.character_dy += self.GRAVITY
            
            self.character_y += self.character_dy
            
            collisioncheck = self.check_collision()
            if collisioncheck:
                self.character_y = nowvaluey
                self.on_ground = True
            # Check if the character collides with the ground
            if self.character_y >= self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH:
                self.character_y = self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH
                self.on_ground = True  # Set on_ground flag
                self.character_dy = 0  # Stop vertical movement

            # Check if the character collides with any collision box

            # Move character horizontally
            self.character_dx = self.move_direction * 5
            self.character_x += self.character_dx
            self.character_x = max(0, min(self.character_x, self.screen.get_width() - self.CHARACTER_WIDTH))
            collisioncheck = self.check_collision()
            if collisioncheck:
                self.character_x = nowvaluex
            


    def update_story_text(self):
        current_time = pygame.time.get_ticks()
        if current_time >= self.show_next_text:
            self.current_story_index += 1
            if self.current_story_index < len(self.story_texts):
                self.story_surface = self.font.render(self.story_texts[self.current_story_index], True, (255, 255, 255))
                self.story_rect = self.story_surface.get_rect(center=(self.screen.get_width() // 2, 100))
                self.show_next_text = current_time + 5000
            else:
                self.story_surface = None

    def draw_character_with_legs(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.character_x, self.character_y, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT))

        hip_x = self.character_x + self.CHARACTER_WIDTH // 2
        hip_y = self.character_y + self.CHARACTER_HEIGHT

        leg_length = self.LEG_LENGTH
        leg_width = 3
        hip_to_leg_top_distance = leg_length * 0.6

        if self.move_direction != 0:
            swing_angle = math.sin(pygame.time.get_ticks() / 100) * math.pi / 6
        else:
            swing_angle = 0

        leg1_angle = swing_angle
        leg2_angle = -swing_angle

        leg1_end_x = hip_x + leg_length * math.sin(leg1_angle)
        leg1_end_y = hip_y + leg_length * math.cos(leg1_angle)
        leg2_end_x = hip_x + leg_length * math.sin(leg2_angle)
        leg2_end_y = hip_y + leg_length * math.cos(leg2_angle)

        pygame.draw.line(self.screen, (255, 255, 255), (hip_x, hip_y), (leg1_end_x, leg1_end_y), leg_width)
        pygame.draw.line(self.screen, (255, 255, 255), (hip_x, hip_y), (leg2_end_x, leg2_end_y), leg_width)

    def draw_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"))
        self.screen.blit(fps_t,(0,0))

    def run(self):
        while True:
            self.handle_events()
            self.update_character()
            self.update_story_text()
            self.move_stars()

            self.screen.fill((0, 0, 0))
            self.draw_stars()
            self.blit_from_json(bplevels+self.level+"blit_instructions.json")
            self.draw_character_with_legs()

            self.fog.move()  # Call move method of the Fog object
            self.fog.draw()  # Call draw method of the Fog object
            pygame.draw.rect(self.screen, (255, 255, 255), self.ground_rect)
            if self.story_surface:
                self.screen.blit(self.story_surface, self.story_rect)
            if self.lightning_generated <self.lightningtimes:
                self.screen.blit(self.lightning_surface, (0, 0))
            self.draw_fps()
            
            pygame.display.flip()
            if self.lightning_generated <self.lightningtimes:
                self.lightning_surface.fill((0, 0, 0, 0)) 
            self.clock.tick(30)
