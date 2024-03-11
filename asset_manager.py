import pygame

class AssetManager:
    def __init__(self):
        self.assets = {}

    def load_image(self, filename):
        try:
            image = pygame.image.load(filename).convert_alpha()
            return image
        except pygame.error as e:
            print(f"Error loading image: {filename}")
            raise SystemExit(e)

    def add_asset(self, name, filename, position, size=None):
        image = self.load_image(filename)
        if size:
            image = pygame.transform.scale(image, size)
        self.assets[name] = {'image': image, 'position': position}

    def blit_assets(self, screen):
        for asset in self.assets.values():
            screen.blit(asset['image'], asset['position'])
