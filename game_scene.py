import pygame
import sys
import math
import random
import json
from fog import Fog
from menu import MenuScene
from over import OverScene
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
class Target:
    def __init__(self, x, y,self2):
        self.screen = self2.screen
        self.rect = pygame.Rect(x, y,self2.CHARACTER_WIDTH/2, self2.CHARACTER_WIDTH/2)  # Adjust the size as needed
        self.health = 100  # Initial health
        self.hitforce = False
        self.pathdecided = False
        self.path = None
        self.bp_sound = "assets/src_audio/"
        self.whisperer = False
        self.whispering = False
        self.prayers = 0
        self.npcspeed=1
        if random.random() < self2.prayprob:
            self.whisper = pygame.mixer.Sound(self.bp_sound +"whisper.mp3")
            self.whisperer = True
    
        
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)  # Draw targets as red rectangles

    def move_randomly(self,self2):
        # Move the target randomly but only on the ground
            if not self.pathdecided:
                self.path = random.randint(0,self2.screen.get_width())  # Move horizontally randomly
                self.pathdecided = True
                
            if self.pathdecided and self.path > self.rect.x:
                self.rect.x +=self.npcspeed
            if self.pathdecided and self.path < self.rect.x:
                 self.rect.x -=self.npcspeed
            if abs(self.path - self.rect.x) < 10:
                self.pathdecided = False
                
    def receive_damage(self, damage,self2):
        self.health -= damage
        self.npcspeed=10
        self.hitheight = -15
        self.hitforce = True
        self.rect.y -= 12
        if self.health <= 0:
            # Remove the target from the list when health is zero
            self.kill(self2)

    def kill(self,self2):
        
        if self.whisperer:
            self.whisper.stop()
        else:
            GameScene.game_over(self2,"Well, he was NOT PRAYING!")
        # Remove the target from the list managed by the GameScene class
        GameScene.get_remove_target(self)
        '''
        self.generate_shattered_pieces(self.rect.x, self.rect.y,self2)
    def generate_shattered_pieces(self2,x, y,self):
        num_pieces = 10  # Number of shattered pieces
        piece_size = 109  # Size of each piece
        for _ in range(num_pieces):
            piece_x = random.randint(x, x + self2.rect.width)  # Random x position within the target's bounds
            piece_y = random.randint(y, y + self2.rect.height)  # Random y position within the target's bounds
            piece_rect = pygame.Rect(piece_x, piece_y, piece_size, piece_size)
            pygame.draw.rect(self.screen, WHITE, piece_rect)  # Draw smaller pieces
'''
targets = []

class GameScene:
    def __init__(self, screen):
        self.level="1"
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.base_path = "assets/src/"  #imgs directory
        self.bp_sound = "assets/src_audio/"

        self.font = pygame.font.Font(None, 40)
        self.menuon = False
        self.levelchange()
    def target_audio(self):
        
        for target in targets:
            if target.whisperer:
                target.prayers+=0.1
                distance = math.sqrt((self.character_x - target.rect.x)**2 + (self.character_y - target.rect.y)**2)
                if target.prayers >self.totalprayers/self.totalprayerswhite:
                    
                    overlay_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
                    overlay_surface.fill((255, 255,255, target.prayers - self.totalprayerswhitecalac))  # Fill with semi-transparent red color (R, G, B, Alpha)
                    self.screen.blit(overlay_surface, (0, 0))
                    if not self.godscoming:
                        self.intensemusic.play()
                        self.intensemusic.set_volume(0.3)
                        self.godscoming = True
                else:
                    self.godscoming = False
                if target.prayers > self.totalprayers:
                    self.game_over("Too late, the gods have heard the prayers.")
                if abs(distance) < self.screen.get_width()/2:
                 if not target.whispering:
                    target.whisper.play(-1)
                    target.whispering = True
                else:
                    target.whisper.stop()
                    target.whispering = False
                if target.whispering:
                    
                    target.whisper.set_volume(1 - (distance/1000))
                       
    def game_over(self,deathtext):
        
                self.handle_events()
                self.screen.fill((0,0,0))
                OverScene(self.screen,deathtext).run()
                self.levelchange()
    def get_remove_target(target):
        # Remove the target from the targets list
        if target in targets:
            targets.remove(target)     
    def levelchange(self):
        self.display_text = True
        pygame.mixer.stop()
        self.playing_footsteps = False
        self.move_direction = 0
        self.character_dy = 0
        self.on_ground = False
        with open(bplevels+self.level+"levelinfo.json", "r") as file:
            level_data = json.load(file)
        self.godscoming = False

        # Extract information
        background_image = level_data["background_image"]
        self.CHARACTER_WIDTH = self.evaluate_value(level_data["player"]["characterwidth"])
        self.CHARACTER_HEIGHT = self.evaluate_value(level_data["player"]["characterheight"])
        self.character_x = self.evaluate_value(level_data["player"]["x"])
        self.character_y = self.evaluate_value(level_data["player"]["y"])
        self.nowvaluex = self.character_x
        self.totalprayers = level_data["player"]["totalprayers"]
        self.totalprayerswhite = level_data["player"]["totalprayerswhite"]
        self.totalprayerswhitecalac = level_data["player"]["totalprayerswhitecalc"]

        self.prayprob = level_data["player"]["prayprob"]
        self.GRAVITY = level_data["player"]["gravity"]
        self.GROUND_HEIGHT = level_data["player"]["groundheight"]
        self.JUMP_FORCE = level_data["player"]["jmpforce"]
        self.LEG_LENGTH = level_data["player"]["leglength"]
        self.LEG_ANGLE_RANGE = level_data["player"]["legangle"]
        self.levelendx = self.evaluate_value(level_data["player"]["levelendx"])
        self.levelendy = self.evaluate_value(level_data["player"]["levelendy"])
        self.intensemusic = pygame.mixer.Sound(self.bp_sound +"gods.mp3")

        self.bgimg = pygame.image.load(self.base_path +background_image).convert()
        self.bgimg = pygame.transform.scale(self.bgimg,(self.screen.get_width(),self.screen.get_height()))
        self.collision_boxes = self.load_collision_boxes(bplevels + self.level + "collision_boxes.json")
        self.images = self.load_images_from_json(bplevels+self.level+"images_list.json")
        self.ground_rect = pygame.Rect(0, self.screen.get_height() - self.GROUND_HEIGHT, self.screen.get_width(), self.GROUND_HEIGHT)
        self.story_texts = level_data.get("story_texts", [])
        self.text_index = 0  # Index for the current text to display
        self.spawn_complete = False
        self.SPAWN_SPEED = 1
        self.lightning_surface = pygame.Surface((self.screen.get_width(),self.screen.get_height()), pygame.SRCALPHA)
        self.thunder = pygame.mixer.Sound(self.bp_sound +"thunder.wav")
        self.footsteps = pygame.mixer.Sound(self.bp_sound +"foot.mp3")
        self.footsteps.set_volume(0.6)
        self.fog = Fog(self.screen)
        self.last_lighting = 0
        targets.clear()
        for _ in range(level_data["player"]["notargets"]):  # Adjust the number of targets as needed
                x = random.randint(self.CHARACTER_WIDTH, self.screen.get_width() - int((self.CHARACTER_WIDTH/2)))  # Adjust the range as needed
                y = self.screen.get_height() - self.GROUND_HEIGHT - (self.CHARACTER_WIDTH/2)  # Adjust the range as needed
                targets.append(Target(x, y,self))
    def generate_single_lightning(self):

        self.lightning_surface.fill((0, 0, 0, 0))
        self.thunder.play()
        start_x = self.character_x
        start_y = 0
        end_y = self.screen.get_height()
        segments = [(start_x, start_y)]
        current_y = start_y
        while current_y < end_y:
            new_x = segments[-1][0] + random.randint(-5, 5)
            new_y = segments[-1][1] + random.randint(10, 20)
            if new_y > end_y:
                new_y = end_y
            segments.append((new_x, new_y))
            current_y = new_y

        for i in range(len(segments) - 1):
            # Draw the lightning segment
            pygame.draw.line(self.lightning_surface, (255, 255, 255, random.randint(200, 255)), segments[i], segments[i + 1], random.randint(3, 5))
        for target in targets:
            distance = math.sqrt((self.character_x+(self.CHARACTER_WIDTH/2) - target.rect.centerx)**2 + (self.character_y - target.rect.centery)**2)
            if abs(distance) <= 200:  # Adjust the radius as needed
                target.receive_damage(50,self)  # Adjust the damage amount as needed
        self.last_lighting = pygame.time.get_ticks()
    def animations(self):
        if self.level == "1":
            if not self.spawn_complete:

                

                # Check if lightning has been generated
                '''
                if self.lightning_generated <self.lightningtimes and self.character_y <= self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH + 90:
                    self.lightning_generated+=1
                    self.generate_single_lightning()  # Generate single lightning strike
                '''
                
                self.character_y -= self.SPAWN_SPEED
                if self.character_y <= self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH:
                    self.character_y = self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH
                    self.spawn_complete = True
                    self.generate_single_lightning()
        if self.level == "2":
            self.spawn_complete = True
    def sound_control(self):
        #Runs after all text shown
        self.music = pygame.mixer.Sound(self.bp_sound +self.level+"theme.mp3")
        self.music.set_volume(0.1)
        self.music.play(-1)
    def render_text(self):
        if self.text_index < len(self.story_texts):
            text = self.story_texts[self.text_index]
            text_surface = self.font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 20))
            self.screen.blit(text_surface, text_rect)   
    def load_collision_boxes(self, json_file):
        with open(json_file, "r") as f:
            collision_data = json.load(f)
            
        return [pygame.Rect(self.evaluate_value(box["x"]), self.evaluate_value(box["y"]), self.evaluate_value(box["width"]), self.evaluate_value(box["height"])) for box in collision_data]

    def check_collision(self):
        player_rect = pygame.Rect(self.character_x, self.character_y, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT + self.LEG_LENGTH)
        for box in self.collision_boxes:
            
            if player_rect.colliderect(box):
                
                if box.left == self.levelendx and box.top == self.levelendy:
                    if not targets:
                        
                        self.level = str(int(self.level) + 1)
                        if int(self.level) == 5:
                            self.level = "1"
                            self.game_over("A game by Naitik Mundra. Thanks for playing")
                            
                        self.levelchange()
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
    def damage(self):
        pass
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
        '''
        for data in collision_data:
            rect = pygame.Rect(self.evaluate_value(data["x"]), self.evaluate_value(data["y"]), self.evaluate_value(data["width"]),self.evaluate_value( data["height"]))
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)  # Draw a red rectangle with a border  
        '''   
    def evaluate_value(self, value):
        if isinstance(value, str) and "self" in value:
            return eval(value)
      
        return int(value)
    def handle_events(self):
        if self.spawn_complete and self.on_ground and self.move_direction != 0 and not self.playing_footsteps:
            self.playing_footsteps = True
            self.footsteps.play(-1)
       
        if not self.on_ground or self.move_direction ==0:
           
            self.playing_footsteps = False
            self.footsteps.stop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.generate_single_lightning()
                if event.key == pygame.K_ESCAPE:
                    self.menuon = not self.menuon
                if event.key == pygame.K_SPACE  and self.on_ground:
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
            #UPDATE ENEMY
            for target in targets:
                if target.hitforce:
                    
                    target.hitheight += self.GRAVITY
                    target.rect.y += target.hitheight
                    if target.rect.y >= self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_WIDTH/2:
                        target.rect.y = self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_WIDTH/2
                        target.hitforce = False
            self.on_ground = False
              # not on the ground by default
            self.nowvaluex = self.character_x
            self.nowvaluey = self.character_y
            if self.spawn_complete and not self.on_ground:
                self.character_dy += self.GRAVITY
            
            self.character_y += self.character_dy
            
            collisioncheck = self.check_collision()
            if collisioncheck:
                self.character_y = self.nowvaluey
                self.on_ground = True
            # Check if the character collides with the ground
            if self.character_y >= self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH and self.spawn_complete:
                self.character_y = self.screen.get_height() - self.GROUND_HEIGHT - self.CHARACTER_HEIGHT - self.LEG_LENGTH
                self.on_ground = True  # Set on_ground flag
                self.character_dy = 0  # Stop vertical movement

            # Check if the character collides with any collision box
            if self.spawn_complete:
                # Move character horizontally
                self.character_dx = self.move_direction * 5
                self.character_x += self.character_dx
                #self.character_x = max(0, min(self.character_x, self.screen.get_width() - self.CHARACTER_WIDTH))
                collisioncheck = self.check_collision()
                if collisioncheck:
                    self.character_x = self.nowvaluex

    def draw_character_with_legs(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.character_x, self.character_y, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT))

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

        pygame.draw.line(self.screen, (255, 0, 0), (hip_x, hip_y), (leg1_end_x, leg1_end_y), leg_width)
        pygame.draw.line(self.screen, (255, 0,0), (hip_x, hip_y), (leg2_end_x, leg2_end_y), leg_width)
    def draw_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"))
        self.screen.blit(fps_t,(0,0))
 
    def run(self):
        text_timer = pygame.time.get_ticks()  # Timer to control text display duration
    
        while True:
            if not self.menuon:
                self.handle_events()
                self.update_character()
                self.screen.blit(self.bgimg, (0,0))
                self.blit_from_json(bplevels+self.level+"blit_instructions.json")
                pygame.draw.rect(self.screen, (0,0,0), self.ground_rect)

                self.draw_character_with_legs()
                self.fog.move()  
                self.fog.draw()  
                self.draw_fps()
                self.animations()
                self.screen.blit(self.lightning_surface, (0, 0))
                # Draw and update targets
                self.target_audio()
                for target in targets:
                    
                    target.move_randomly(self)
                    target.draw(self.screen)
                if self.display_text:
                    
                    self.render_text()

                    # next text
                    if pygame.time.get_ticks() - text_timer >= 3000:  
                        self.text_index += 1
                        text_timer = pygame.time.get_ticks()

                        # Reset text
                        if self.text_index >= len(self.story_texts):
                            self.sound_control()
                            self.display_text = False
                            
                pygame.display.flip()
                self.clock.tick(30)
                if (pygame.time.get_ticks() - self.last_lighting) >=100:
                    self.lightning_surface.fill((0, 0, 0, 0))

            else:
                self.handle_events()
                self.screen.fill((0,0,0))
                MenuScene(self.screen).run()
                self.menuon = False




            
            
