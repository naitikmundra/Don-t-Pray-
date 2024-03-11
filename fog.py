import pygame
import random

class Fog:
    def __init__(self, screen):
        self.screen = screen
        self.MIN_SPEED = -2
        self.MAX_SPEED = 2
        self.MIN_SPEED_Y = 0
        self.MAX_SPEED_Y = 0
        self.MIN_SIZE = 50
        self.MAX_SIZE = 50
        self.NUM_PARTICLES = 600
        self.fog_intensity = 3

        self.heightlimit = int(self.screen.get_height()/5)
        self.particles = []
        self.generate_particles()
        self.fog_surfaces = []
        self.generate_fog_surfaces()
    def generate_particles(self):
        for _ in range(self.NUM_PARTICLES):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(self.screen.get_height() - self.heightlimit, self.screen.get_height()-int(self.screen.get_width()/21.6))
            width = random.randint(self.MIN_SIZE, self.MAX_SIZE)
            height = random.randint(self.MIN_SIZE, self.MAX_SIZE)
            speed_x = random.uniform(self.MIN_SPEED, self.MAX_SPEED)
            speed_y = random.uniform(self.MIN_SPEED_Y, self.MAX_SPEED_Y)
            self.particles.append((x, y, width, height, speed_x, speed_y))

    def generate_fog_surfaces(self):
        for _ in range(self.NUM_PARTICLES):
            fog_surface = pygame.Surface((300, 50), pygame.SRCALPHA)
            fog_surface.fill((100, 100, 100, self.fog_intensity))
            self.fog_surfaces.append(fog_surface)

    def move(self):
        for i in range(len(self.particles)):
            x, y, width, height, speed_x, speed_y = self.particles[i]
            x += speed_x
            y += speed_y

  
            if x > self.screen.get_width() + self.MAX_SIZE:
                x = -self.MAX_SIZE
            elif x < -self.MAX_SIZE:
                x = self.screen.get_width() + self.MAX_SIZE

            self.particles[i] = (x, y, width, height, speed_x, speed_y)

    def draw(self):
        for x, y, _, _, _, _ in self.particles:
            fog_surface = random.choice(self.fog_surfaces)
            self.screen.blit(fog_surface, (x, y))
